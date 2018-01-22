if !has('python')
    echoerr 'This plugin requires python.'
    finish
endif

if exists('vim_grayout_loaded')
    finish
else
    let g:vim_grayout_loaded = 1
    let g:grayout_debug = get(g:, 'grayout_debug', 0)
    let g:grayout_debug_logfile = get(g:, 'grayout_debug_logfile', 0)
    let g:grayout_debug_compiler_inout = get(g:, 'grayout_debug_compiler_inout', 0)
    let g:grayout_cmd_line = get(g:, 'grayout_cmd_line', 'clang -x c++ -w -P -E -')
    let g:grayout_confirm = get(g:, 'grayout_confirm', 1)
    let g:grayout_workingdir = get(g:, 'grayout_workingdir', 0)

    let s:pyscript = expand('<sfile>:p:h').'/grayout.py'

    highlight PreprocessorGrayout cterm=italic gui=italic ctermfg=DarkGray guifg=DarkGray
    sign define PreprocessorGrayout linehl=PreprocessorGrayout

    command! GrayoutUpdate call s:UpdateGrayout()
    command! GrayoutClear call s:ClearGrayout()
    command! GrayoutReloadConfig call s:ReloadGrayoutConfig()

    python import sys
endif

function! s:UpdateGrayout()
    if !exists('b:num_grayout_lines')
        let b:num_grayout_lines = 0
    endif

    if !exists('b:_grayout_workingdir')
        let b:_grayout_workingdir = ''
    endif

    if !exists('b:grayout_cmd_line')
        call s:ReloadGrayoutConfig()
    endif

    python sys.argv = ["grayout"]
    execute 'pyfile'.s:pyscript
endfunction

function! s:ClearGrayout()
    python sys.argv = ["clear"]
    execute 'pyfile'.s:pyscript
endfunction

function! s:ReloadGrayoutConfig()
    python sys.argv = ["config"]
    execute 'pyfile'.s:pyscript
endfunction
