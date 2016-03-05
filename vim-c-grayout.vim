if !has('python')
    finish
endif

highlight PreprocessorGrayout ctermbg=gray guibg=gray
sign define PreprocessorGrayout linehl=PreprocessorGrayout

let g:grayout_debug = 1

function! UpdateGrayout()
    if !exists("b:num_grayout_lines")
        let b:num_grayout_lines = 0
    endif
    pyfile grayout.py
endfunction
