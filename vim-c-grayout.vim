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
    let g:grayout_cmd_line = ''

    highlight PreprocessorGrayout cterm=italic gui=italic ctermfg=DarkGray guifg=DarkGray
    sign define PreprocessorGrayout linehl=PreprocessorGrayout
endif

function! UpdateGrayout()
    if !exists("b:num_grayout_lines")
        let b:num_grayout_lines = 0
    endif
    pyfile grayout.py
endfunction
