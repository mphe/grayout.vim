#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import utils
import vim  # pylint: disable=import-error
import clang.cindex as cindex

INDEX: cindex.Index = None
LAST_TU = ("", None)

# def timeit(method):
#     import time
#
#     def timed(*args, **kw):
#         ts = time.time()
#         result = method(*args, **kw)
#         te = time.time()
#         if 'log_time' in kw:
#             name = kw.get('log_name', method.__name__.upper())
#             kw['log_time'][name] = int((te - ts) * 1000)
#         else:
#             print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
#         return result
#     return timed


# @timeit
def grayout():
    global LAST_TU

    # Unnamed buffer
    if not vim.current.buffer.name:
        return

    filename, args = utils.get_current_args()
    src = "\n".join(vim.current.buffer)

    options = cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD | \
        cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES | \
        cindex.TranslationUnit.PARSE_INCOMPLETE | \
        cindex.TranslationUnit.PARSE_KEEP_GOING | \
        cindex.TranslationUnit.PARSE_PRECOMPILED_PREAMBLE

    utils.printdebug("Compile flags:", args)

    try:
        if LAST_TU[0] == filename:
            tu = LAST_TU[1]
            tu.reparse(options=options, unsaved_files=[(filename, src)])
        else:
            tu = INDEX.parse(
                filename, args=args, options=options, unsaved_files=[(filename, src)])
            LAST_TU = (filename, tu)
    except cindex.TranslationUnitLoadError as e:
        utils.printdebug(e, info=True)
        return

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
    global LAST_TU
    utils.DB_CACHE.clear()
    utils.ARGS_CACHE.clear()
    LAST_TU = ("", None)


def init():
    utils.DEBUG = int(vim.eval("g:grayout_debug"))
    utils.DEBUG_FILE = int(vim.eval("g:grayout_debug_logfile"))

    if os.path.isfile(utils.LOG_FILENAME):
        utils.printdebug("--------------------------")

    clangpath = vim.eval("g:grayout_libclang_path")
    if clangpath:
        cindex.Config.set_library_path(clangpath)

    global INDEX
    INDEX = cindex.Index.create()

    utils.printdebug("Initialized")
