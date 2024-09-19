" ---------------------------------------------------------------------
" A simple vimrc
" ---------------------------------------------------------------------

" Allow multiple pastes of the last yanked text
set clipboard+=unnamedplus
set paste

" Enable relative line numbers and toggle between relative and absolute
set number
set relativenumber
nnoremap tr :set relativenumber!<CR>

" Map space + h/j/k/l to navigate between tabs
nnoremap <space>n :tabnew<CR>
nnoremap <space>h :tabfirst<CR>
nnoremap <space>j :tabprev<CR>
nnoremap <space>k :tabnext<CR>
nnoremap <space>l :tablast<CR>

" Map Ctrl + h/j/k/l to move between panel splits
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" Shortcuts to increase/decrease panel sizes
nnoremap <C-Left> :vertical resize -2<CR>
nnoremap <C-Right> :vertical resize +2<CR>
nnoremap <C-Up> :resize +2<CR>
nnoremap <C-Down> :resize -2<CR>

