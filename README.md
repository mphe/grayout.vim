# grayout.vim

## This plugin is no longer maintained

This plugin was developed before LSP became popular.
Common C/C++ language servers like [clangd] or [ccls] provide full semantic highlighting including skipped preprocessor regions in addition to code completion, syntax checking, code actions, etc.
They can be integrated into Vim/Neovim using LSP plugins like [coc.nvim], [nvim-lspconfig] or [vim-lsp].

Since this plugin is pretty much obsolete nowadays, I don't see much value in further supporting it.<br/>
It will likely still work as expected in most scenarios, though.


## Overview

**grayout.vim** is a vim plugin that grays out inactive C/C++/Obj-C preprocessor regions using libclang.<br/>
In addition to custom config files, it also supports `compile_commands.json` compilation databases, allowing quick and easy project setup.<br/>
Even though it is intended to be used with C/C++/Obj-C, it should work with all filetypes, as long as the `-x <language>` compile flag is set.

It was only tested on Linux but should *theoretically* work on other platforms, too.


## Related Work
There are some other plugins providing similar functionality, but in different ways.

* [ifdef highlighting] adds static vim syntax rules for each *manually* defined macro. It does not make use of a compiler and requires the user to manually specify which macros are defined, thus being rather unflexible and often fails to properly detect skipped regions.

* [DyeVim] integrates with (a custom fork of) [YouCompleteMe] to retrieve extended syntax information for semantic highlighting, including skipped preprocessor regions.
However, it only works with YCM's libclang completer, not the newer and more advanced clangd completer.

* [vim-lsp-inactive-regions] integrates with [vim-lsp] and uses the [cquery] or [ccls] language server to retrieve skipped preprocessor regions.

* [vim-lsp-cxx-highlight] integrates with various LSP plugins and uses the [cquery] or [ccls] language server to provide full semantic highlighting, including skipped preprocessor regions.

* Common C/C++ language servers like [clangd] and [ccls] support full semantic highlighting including skipped preprocessor regions.
  They can be integrated into Vim/Neovim using LSP plugins like [coc.nvim], [nvim-lspconfig] or [vim-lsp].

  See also the [maintenance note](#this-plugin-is-no-longer-maintained).

## Installation

1. Requirements
    * Vim 8.1+ or Neovim
    * Python 3
    * Clang
2. Install the plugin
    * Using a plugin manager
    * Alternatively, copy the contents of this repository to your vim directory
3. Read the docs
4. ...
5. Profit


## Commands

* Run `:GrayoutUpdate` to parse the current file and apply highlighting.
* Run `:GrayoutClear` to clear all grayout highlights from current buffer
* Run `:GrayoutClearCache` to clear the compile command cache, forcing to reload all config files when needed.
* Run `:GrayoutShowCommand` to print the current file's compile flags.


## Configuration

### Example Configuration

```vim
" Bind :GrayoutUpdate to F5
nnoremap <F5> :GrayoutUpdate<CR>

" Run GrayoutUpdate when opening and saving a buffer
autocmd BufReadPost,BufWritePost * if &ft == 'c' || &ft == 'cpp' || &ft == 'objc' | exec 'GrayoutUpdate' | endif

" Run GrayoutUpdate when cursor stands still. This can cause lag in more complex files.
autocmd CursorHold,CursorHoldI * if &ft == 'c' || &ft == 'cpp' || &ft == 'objc' | exec 'GrayoutUpdate' | endif
```

### Variables

```vim
" Set default compile flags.
" These are used, when no `compile_commands.json` or `.grayout.conf` file was found.
let g:grayout_default_args = [ '-x', 'c++', '-std=c++11' ]

" Set libclang searchpath. This should point to the directory containing `libclang.so`.
" Leave empty to auto-detect.
let g:grayout_libclang_path = ''

" Enable to print debug messages inside vim.
let g:grayout_debug = 0

" Enable to write debug messages to `grayout.log`.
let g:grayout_debug_logfile = 0
```

### Compile Flags

As with every compiler, clang needs to know your project's compile flags to compile your code.<br/>
There are three ways of defining compile flags, that are prioritized in the respective order.<br/>
**Note:** If you make any changes related to compile flags at runtime, you will need to run `:GrayoutClearCache` in order to reload those configs.

* Compilation Database (**recommended**)

    Instruct your build system to generate a `compile_commands.json` and symlink or move it to your project root.

    A [compilation database][clangdatabase] contains information on how to compile each translation unit. It can be auto-generated by build systems like cmake, or tools like [Bear][bear] or [compdb][compdb].

    For example, using cmake, add this line to your `CMakeLists.txt`:

    ```cmake
    set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
    ```

* `.grayout.conf`

    Create a `.grayout.conf` file in your project root containing the compile flags. Linebreaks are ignored.<br/>
    It is recommended to specify `-x <language>` in order to avoid ambiguity, especially with header files.

    Example:

    ```text
    -x c
    -DENABLE_FEATURE_X
    -DANOTHER_FLAG
    -DSOME_CONSTANT=42
    ```

* `g:grayout_default_args`

    The global `g:grayout_default_args` variable holds a list of compile flags and is used when no other configs were found.
    It is recommended to specify `-x <language>` in order to avoid ambiguity, especially with header files.

    Example:

    ```vim
    let g:grayout_default_args = [ '-x', 'c++', '-std=c++11', '-DFOOBAR_MACRO' ]
    ```

### Colors

If you don't like the default colors for grayouts, you can change them by altering the `PreprocessorGrayout` style.
By default it links to the `Comment` style.

Example:

```vim
highlight PreprocessorGrayout cterm=italic ctermfg=DarkGray gui=italic guifg=#6c6c6c
```

## Contributing

If you encounter any bugs or problems, please make sure to read the docs. If the problem persists, open a new issue on Github. Remember to add `let g:grayout_debug_logfile = 1` to your vimrc and attach the `grayout.log` logfile to your issue.

Pull requests are welcome.

## Todo

* Support `textprops` or `nvim_buf_add_highlight`
* Fix edge case where consecutive active if/elif/else lines are grayed out when their contents are inactive


[ifdef highlighting]: http://www.vim.org/scripts/script.php?script_id=7
[DyeVim]: https://github.com/davits/DyeVim
[YouCompleteMe]: https://github.com/ycm-core/YouCompleteMe
[vim-lsp-inactive-regions]: https://github.com/krzbe/vim-lsp-inactive-regions
[vim-lsp]: https://github.com/prabirshrestha/vim-lsp
[vim-lsp-cxx-highlight]: https://github.com/jackguo380/vim-lsp-cxx-highlight
[compdb]: https://github.com/Sarcasm/compdb
[clangdatabase]: http://clang.llvm.org/docs/JSONCompilationDatabase.html
[bear]: https://github.com/rizsotto/Bear
[cquery]: https://github.com/cquery-project/cquery
[ccls]: https://github.com/MaskRay/ccls
[coc.nvim]: https://github.com/neoclide/coc.nvim
[nvim-lspconfig]: https://github.com/neovim/nvim-lspconfig
[clangd]: https://clangd.llvm.org/
