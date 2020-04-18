if exists('g:vim_grayout_initialized_autoload')
    finish
endif

let g:vim_grayout_initialized_autoload = 1

if !has('python3')
    echoerr 'This plugin requires Python 3'
    finish
endif

py3 << EOF
import sys
import os
import vim
scriptdir = vim.eval('expand("<sfile>:p:h")')
sys.path.insert(0, os.path.join(scriptdir, "..", "python"))
import grayout
grayout.init()
EOF


function! grayout#UpdateGrayout()
    py3 grayout.grayout()
endfunction

function! grayout#ClearGrayout()
    " TOOD: textprops, nvim_buf_add_highlight, or sign-group feature
    call s:ClearHighlightSigns()
endfunction

function! grayout#ClearCache()
    py3 grayout.clear_cache()
endfunction

function! grayout#ShowArgs()
    py3 grayout.show_compile_command()
endfunction


function! s:HighlightLines(lines)
    call grayout#ClearGrayout()
    " TOOD: textprops, nvim_buf_add_highlight, or sign-group feature
    call s:HighlightLinesSign(a:lines)
endfunction


" Sign based highlighting {{{
function! s:GetBaseSignID()
    return (1 + bufnr('%')) * 2537
endfunction

function! s:HighlightLinesSign(lines)
    let l:basesignid = s:GetBaseSignID()

    for l:i in a:lines
        let l:signid = l:basesignid + b:_num_grayout_lines
        exec 'sign place ' . l:signid . ' line=' . l:i . ' name=PreprocessorGrayout buffer=' . bufnr('%')
        let b:_num_grayout_lines += 1
    endfor
endfunction

function! s:ClearHighlightSigns()
    if exists('b:_num_grayout_lines')
        let l:basesignid = s:GetBaseSignID()

        for l:i in range(b:_num_grayout_lines)
            exec 'sign unplace ' . (l:basesignid + l:i) . ' buffer=' . bufnr('%')
        endfor
    endif

    let b:_num_grayout_lines = 0
endfunction
" }}}
