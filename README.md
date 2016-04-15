# grayout.vim

**grayout.vim** is a simple plugin that grays out inactive preprocessor blocks.

Instead of manually parsing the source file (like [ifdef highlighting](http://www.vim.org/scripts/script.php?script_id=7)), this plugin invokes the compiler (clang by default) on the source file and parses its output. See "[How it works](#how-it-works)" for further information.

Although it's intended to be used for C/C++/Obj-C, it should also work for every language with C-style preprocessor commands.

The plugin was only tested on Linux but should work on other platforms, too (with custom command lines).

## Installation

1. Make sure your vim version is compiled with python support
2. Install the plugin
    * Using a plugin manager like vundle or pathogen
    * Alternatively copy the `plugin` directory into your .vim folder
3. Configure it as you like (see "[Configuration](#configuration)")
4. ...
5. Profit


## Usage

* Run `:GrayoutUpdate` to update the grayout.
* Run `:GrayoutClear` to clear all grayouts.
* Run `:GrayoutReloadConfig` to reload the config file.

All these commands only affect the current buffer.

## How it works

When calling `:GrayoutUpdate` the source file is parsed for `#if`-`#elif`-`#else`-`#endif` blocks and their line start and end positions are stored in a list.

Then a special "tag", containing a random UUID followed by the ID and line information for the current block, is inserted at the start of every block. The modified source is then sent over stdin to the compiler (only to the preprocessor to be precise) using the specified command line (`clang -x c++ -w -P -E -` by default).

The comiler output is parsed again for tag-lines. If a tag was found it means that the block it was injected in is active. The script can then grayout certain lines depending on which tags were found and which tags weren't, since tags inside a inactive block don't show up in the compiler output.


## Configuration

### Key mappings

The plugin comes with no default keymappings, it only provides the commands listed above.

To map `:GrayoutUpdate` to e.g. `<F5>` you can add this to your .vimrc:
```vim
nnoremap <F5> :GrayoutUpdate<CR>
```

### Options

* Set the command to invoke the compiler
    ```vim
    let g:grayout_cmd_line = 'clang -x c++ -w -P -E -'
    ```

    If you set a custom command, remember to pass the flags for only invoking the preprocessor and reading the source from stdin (`-E` and `-` for gcc and clang), otherwise it won't work. The language needs to be specified using the `-x` flag, too.

    For example, if you want to use gcc instead of clang you can write:
    ```vim
    let g:grayout_cmd_line = 'gcc -x c++ -w -P -E -'
    ```

* Ask for confirmation when loading a config file.
    ```vim
    let g:grayout_confirm = 1
    ```
    By default the user is asked for confirmation when a config file is found. This might be desirable because config files could potentially contain malicious code. See also "[Config files](#config-files)".

    To disable confirmations:
    ```vim
    let g:grayout_confirm = 0
    ```

* Enable debug messages inside vim
    ```vim
    let g:grayout_debug = 0
    ```
* Enable writing debug messages to grayout-log.txt
    ```vim
    let g:grayout_debug_logfile = 0
    ```
* Log compiler in- and output
    ```vim
    let g:grayout_debug_compiler_inout = 0
    ```
    If `g:grayout_debug` or `g:grayout_debug_logfile` is enabled, this option will also log the compiler in- and output. **Default is 0.**


### Config files

For project specific configuration you can create a `.grayout.conf` file containing the compiler command. This basically works like `g:grayout_cmd_line`.

The script searches the parent directories until it finds a config file. If no config file was found, the command in `g:grayout_cmd_line` is used.

To reload the config file run `:GrayoutReloadConfig`. Be aware that this only reloads the config for the current buffer. Other buffers won't get updated this way, even if they share the same file.

The syntax is pretty straight forward. The file only contains the command to invoke the compiler. Linebreaks are ignored.
Remember to pass the flags for only invoking the preprocessor and reading the source from stdin (`-E` and `-` for gcc and clang).

For example, for a C project you might write:
```
gcc -x c -w -P -E
    -nostdinc
    -
```

### Useful Compiler flags

Every flag that reduces compiler output speeds up the grayout process because less lines have to be processed (see "[How it works](#how-it-works)").

Since you usually don't need to check macros from standard libraries, it's a good idea to add `-nostdinc` and/or `-nostdinc++` to your cmd line to tell the compiler to ignore system includes. This could give a significant speed boost as it greatly reduces the compiler output.

**-nostdinc**
> Do not search the standard system directories for header files. Only the directories you have specified with -I options (and the directory of the current file, if appropriate) are searched.

**-nostdinc++**
> Do not search for header files in the standard directories specific to C++, but do still search the other standard directories.

**-P**
> Inhibit generation of linemarkers in the output from the preprocessor. This might be useful when running the preprocessor on something that is not C code, and will be sent to a program which might be confused by the linemarkers.

**-w**
> Inhibit all warning messages.

The `-P` and `-w` flags are set by default.

### Colors

If you don't like the default colors for grayouts you can change them by altering the `PreprocessorGrayout` style.

The default is:
```vim
highlight PreprocessorGrayout cterm=italic gui=italic ctermfg=DarkGray guifg=DarkGray
```


## Todo

* Write vim doc
* Maybe rewrite the core functionality in vimscript to get rid of the python dependency
* Add support for Makefiles
