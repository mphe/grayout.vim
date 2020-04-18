if exists('g:vim_grayout_loaded')
    finish
endif

let g:vim_grayout_loaded = 1

let g:grayout_debug = get(g:, 'grayout_debug', 0)
let g:grayout_debug_logfile = get(g:, 'grayout_debug_logfile', 0)
let g:grayout_default_args = get(g:, 'grayout_default_args', [])
let g:grayout_libclang_path = get(g:, 'grayout_libclang_path', '')

highlight link PreprocessorGrayout Comment
sign define PreprocessorGrayout linehl=PreprocessorGrayout

command! GrayoutUpdate call grayout#UpdateGrayout()
command! GrayoutClear call grayout#ClearGrayout()
command! GrayoutClearCache call grayout#ClearCache()
command! GrayoutShowArgs call grayout#ShowArgs()
