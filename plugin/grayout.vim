if exists('g:vim_grayout_loaded')
    finish
else
    let g:vim_grayout_loaded = 1

    if !has('python3')
        echoerr 'This plugin requires Python 3'
        finish
    endif

    let s:scriptdir = expand('<sfile>:p:h')

    let g:grayout_debug = get(g:, 'grayout_debug', 0)
    let g:grayout_debug_logfile = get(g:, 'grayout_debug_logfile', 0)
    let g:grayout_default_args = get(g:, 'grayout_default_args', [])
    let g:grayout_libclang_path = get(g:, 'grayout_libclang_path', '')

    highlight link PreprocessorGrayout Comment
    sign define PreprocessorGrayout linehl=PreprocessorGrayout

    command! GrayoutUpdate call s:UpdateGrayout()
    command! GrayoutClear call s:ClearGrayout()
    command! GrayoutClearCache call s:ClearCache()
    command! GrayoutShowArgs call s:ShowArgs()

    augroup grayout_vim_initialize
        autocmd!
        autocmd VimEnter * call s:init()
    augroup END
endif


function! s:init()
    py3 << EOF
import sys
import vim
sys.path.insert(0, vim.eval('s:scriptdir'))
import grayout
grayout.init()
EOF
endfunction


function! s:UpdateGrayout()
    py3 grayout.grayout()
endfunction

function! s:ClearGrayout()
    " TOOD: textprops, nvim_buf_add_highlight, or sign-group feature
    call s:ClearHighlightSigns()
endfunction

function! s:ClearCache()
    py3 grayout.clear_cache()
endfunction

function! s:ShowArgs()
    py3 grayout.show_compile_command()
endfunction


function! s:HighlightLines(lines)
    call s:ClearGrayout()
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
