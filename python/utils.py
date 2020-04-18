import vim  # pylint: disable=import-error
import shlex
import os
import clang.cindex as cindex

LOG_FILENAME = "grayout.log"

# Maps filepath to CompilationDatabase
DB_CACHE = {}

# Maps filepath to a tuple (args , cwd)
ARGS_CACHE = {}

DEBUG = False
DEBUG_FILE = False


def printdebug(*args, info=False):
    text = " ".join(map(str, args))

    if DEBUG:
        print(text)
    elif info:
        print("grayout.vim:", text)

    if DEBUG_FILE:
        with open(LOG_FILENAME, "a") as f:
            f.write(text + "\n")


def find_config_file(path, searchname):
    rootpath = os.path.abspath(os.sep)  # should work this way on windows, too
    fullpath = ""

    while True:
        fullpath = os.path.join(path, searchname)
        printdebug("Searching", fullpath)
        if os.path.isfile(fullpath):
            printdebug("Found config file", fullpath)
            return fullpath
        if path == rootpath:
            break
        path = os.path.dirname(path)

    printdebug("No config file found")
    return None


def get_current_args():
    """Returns a tuple (filename, compiler args)."""
    filename = os.path.realpath(vim.current.buffer.name)
    dirname = os.path.dirname(filename)
    cwd = ""

    printdebug("Querying arguments for", filename)

    args, cwd = ARGS_CACHE.get(filename, (None, None))

    if args is not None:
        printdebug("Found file in cache")
        return filename, args

    args, cwd = load_compilation_database(filename, dirname)

    if args is None:
        args, cwd = load_grayout_conf(dirname)

        if args is not None:
            printdebug("Using .grayout.conf", info=True)
        else:
            args = list(vim.eval("g:grayout_default_args"))
            printdebug("Falling back to `g:grayout_default_args`", info=True)

    args = prepare_args(args)
    ARGS_CACHE[filename] = (args, cwd)
    return filename, args


def load_compilation_database(filename, dirname):
    """Returns a tuple (args, cwd)."""
    global DB_CACHE

    cfg = find_config_file(dirname, "compile_commands.json")

    if cfg:
        db: cindex.CompilationDatabase = DB_CACHE.get(cfg, None)

        if db is None:
            cfgdir = os.path.dirname(cfg)
            db: cindex.CompilationDatabase = cindex.CompilationDatabase.fromDirectory(cfgdir)
            DB_CACHE[cfg] = db
            printdebug("CompilationDatabase loaded and stored in cache")
        else:
            printdebug("CompilationDatabase found in cache")

        cmd: cindex.CompileCommand = db.getCompileCommands(filename)[0]
        printdebug(cmd.directory, cmd.filename)

        if cmd:
            # Strip last argument because it's the source filename
            return list(cmd.arguments)[:-1], cmd.directory
        printdebug("No command found in database")

    return None, None


def load_grayout_conf(dirname):
    """Returns a tuple (args, cwd)."""
    cfg = find_config_file(dirname, ".grayout.conf")
    if cfg:
        with open(cfg, "r") as f:
            return shlex.split(f.read()), os.path.dirname(cfg)
    return None, None


def prepare_args(args):
    """Strip output arguments."""
    strip_arg(args, "-o", True)
    strip_arg(args, "-c", False)
    strip_arg(args, "-S", False)
    strip_arg(args, "-v", False)

    return args


def strip_arg(args, name, stripnext):
    try:
        pos = args.index(name)
    except ValueError:
        return

    del args[pos]
    if stripnext and pos < len(args):
        del args[pos]
