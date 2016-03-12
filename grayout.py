#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
from subprocess import Popen, PIPE
import uuid
import vim

# TODO: find a better solution for sign ids
debug = int(vim.eval("g:grayout_debug"))
debug_file = int(vim.eval("g:grayout_debug_logfile"))
bufnr = int(vim.eval("bufnr('%')"))
basesignid = (1 + bufnr) * 25397
numgrayouts = int(vim.eval("b:num_grayout_lines"))
cmdline = vim.eval("g:grayout_cmd_line")


class LineInfo(object):
    def __init__(self, n, linebegin = -1, lineend = -1):
        self.linebegin = linebegin
        self.lineend = lineend
        self.active = False

    def __str__(self):
        return "begin={} end={}".format(self.linebegin, self.lineend)


class Parser(object):
    regex = re.compile(r"\s*#\s*(if|else|endif).*")
    cmdline = ["g++", "-w", "-x", "c++", "-E", "-"]

    def __init__(self):
        self._blocks = []
        self.lines = []
        self._uuid = None

    def getBlocks(self):
        return self._blocks

    def getActiveBlocks(self):
        for i in self._blocks:
            if i.active:
                yield i

    def getInactiveBlocks(self):
        for i in self._blocks:
            if not i.active:
                yield i

    def parsestring(self, text):
        self.lines = text.splitlines(True)
        self._parse()

    def parsefile(self, fname):
        with open(fname, "r") as f:
            self.lines = f.readlines()
        self._parse()

    def parselines(self, lines):
        self.lines = [i for i in lines]
        self._parse()

    def compile(self, cmdline = ""):
        cmd = cmdline.split() if cmdline else Parser.cmdline
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        code = self._injectTags()
        printdebug("\nUsing cmd line:", " ".join(cmd))
        printdebug("\nCompiler input:\n" + code)
        out = p.communicate(code)[0]
        printdebug("\nCompiler output:\n" + out)
        self._parseTags(out)

    def _injectTags(self):
        self._uuid = uuid.uuid1()
        for n,i in enumerate(self._blocks[::-1], 1):
            i.active = False # Reset
            if i.linebegin != i.lineend:
                self.lines.insert(i.linebegin, "{} n={} {}".format(self._uuid, str(len(self._blocks) - n), str(i)))
        return "\n".join(self.lines)

    def _parseTags(self, text):
        r = re.compile(str(self._uuid) + r" n=(\d+) begin=(\d+) end=(\d+)")
        for i in text.splitlines():
            m = r.match(i.strip())
            if m:
                self._blocks[int(m.group(1))].active = True

    def _parse(self):
        self._tags = []
        self._parseblock(enumerate(self.lines, 1))

    def _parseblock(self, enum):
        for n,l in enum:
            m = Parser.regex.match(l)
            if m:
                if m.group(1) == "if" or m.group(1) == "else":
                    self._addtag(n, enum)
                if m.group(1) == "else" or m.group(1) == "endif":
                    return n

    def _addtag(self, n, enum):
        # Keep the blocks in ascending order
        self._blocks.append(LineInfo(len(self._blocks), n))
        tmp = self._blocks[-1]
        tmp.lineend = self._parseblock(enum)

def printdebug(*args):
    text = " ".join([ str(i) for i in args ])
    if debug:
        print(text)
    if debug_file:
        with open("grayout-log.txt", "a") as f:
            f.write(text + "\n")

def grayout():
    global debug, debug_file, bufnr, basesignid, numgrayouts, cmdline

    printdebug("bufnr:", bufnr)
    printdebug("basesignid:", basesignid)
    printdebug("numgrayouts:", numgrayouts)

    printdebug("\nClearing existing grayouts...")
    for i in range(numgrayouts):
        printdebug("Removing sign", basesignid + i)
        vim.command("sign unplace {} buffer={}".format(basesignid + i, bufnr))

    parser = Parser()
    parser.parselines(vim.current.buffer)
    parser.compile(cmdline)

    if debug:
        printdebug("\nInactive blocks:")
        for i in parser.getInactiveBlocks():
            printdebug(i)

        printdebug("\nActive blocks:")
        for i in parser.getActiveBlocks():
            printdebug(i)


    printdebug("\nApplying new grayouts...")
    numgrayouts = 0
    lastblock = None
    for b in parser.getInactiveBlocks():
        # Skip nested blocks if the parent block is inactive
        if lastblock and b.lineend < lastblock.lineend:
            printdebug("Skipping nested block", b)
            continue

        for i in range(b.linebegin + 1, b.lineend):
            signid = basesignid + numgrayouts
            printdebug("Creating grayout {} in line {}".format(signid, i))
            vim.command("sign place {} line={} name=PreprocessorGrayout file={}".format(
                signid, i, vim.current.buffer.name))
            numgrayouts += 1
        lastblock = b

    printdebug("new numgrayouts: {}\n-----------------------------------------------\n".format(str(numgrayouts)))
    vim.command("let b:num_grayout_lines = " + str(numgrayouts))


if __name__ == "__main__":
    grayout()
