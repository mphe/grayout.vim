#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import utils
import vim  # pylint: disable=import-error
import clang.cindex as cindex

INDEX = cindex.Index.create()


def grayout():
    filename, args = utils.get_current_args()
    utils.printdebug("Compile flags:", args)

    options = cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD | cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES

    src = "\n".join(vim.current.buffer)
    tu = INDEX.parse(
        filename, args=args, options=options, unsaved_files=[(filename, src)])

    for i in tu.diagnostics:
        utils.printdebug(i)

    utils.printdebug("Applying new grayouts...")

    lines = []

    i: cindex.SourceRange
    for i in tu.get_skipped_ranges(filename):
        utils.printdebug(i)
        for r in range(i.start.line + 1, i.end.line):
            lines.append(r)

    utils.printdebug("lines:", lines)
    vim.eval("s:HighlightLines({})".format(repr(lines)))


def show_compile_command():
    print(utils.get_current_args()[1])


def clear_cache():
    utils.DB_CACHE.clear()
    utils.ARGS_CACHE.clear()


def init():
    utils.DEBUG = int(vim.eval("g:grayout_debug"))
    utils.DEBUG_FILE = int(vim.eval("g:grayout_debug_logfile"))

    if os.path.isfile(utils.LOG_FILENAME):
        utils.printdebug("--------------------------")
