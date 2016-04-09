if !has('python')
    echoerr "This plugin requires python."
    finish
endif

if exists('vim_c_grayout_loaded')
    finish
else
    let g:vim_c_grayout_loaded = 1
    let g:grayout_debug = 0
    let g:grayout_debug_logfile = 0
    let g:grayout_debug_compiler_inout = 0
    let g:grayout_cmd_line = 'clang -x c++ -w -P -E -'
    let g:grayout_confirm = 1

    highlight PreprocessorGrayout cterm=italic gui=italic ctermfg=DarkGray guifg=DarkGray
    sign define PreprocessorGrayout linehl=PreprocessorGrayout

    command! GrayoutUpdate call s:UpdateGrayout()
    command! GrayoutClear call s:ClearGrayout()
    command! GrayoutReloadConfig call s:ReloadGrayoutConfig()

    python import sys
endif

function! s:UpdateGrayout()
    if !exists("b:num_grayout_lines")
        let b:num_grayout_lines = 0
    endif

    if !exists('b:grayout_cmd_line')
        call s:ReloadGrayoutConfig()
    endif

    python sys.argv = ["grayout"]
    pyfile grayout.py
endfunction

function! s:ClearGrayout()
    python sys.argv = ["clear"]
    pyfile grayout.py
endfunction

function! s:ReloadGrayoutConfig()
    python sys.argv = ["config"]
    pyfile grayout.py
endfunction
