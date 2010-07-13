set nocompatible

filetype on
filetype plugin on
filetype indent on
syntax on
colorscheme torte

set tabstop=4 softtabstop=4 shiftwidth=4 noexpandtab

set autoindent
set backspace=indent,eol,start
set backupdir=./.backup,.,/tmp
set directory=.,./.backup,/tmp
set fillchars=""
set helpheight=100
set history=100
set hlsearch
set incsearch
set laststatus=2
set number
set ruler
set scrolloff=8
set showcmd
set showmode
set splitbelow
set splitright
set stl=%f\ %m\ %r\ Line:%l/%L[%p%%]\ Col:%c\ Buf:%n\ [%b][0x%B]
set tabpagemax=50
set textwidth=120
set wildmode=list:longest
set wrapscan

map <buffer> <S-e> :w<CR>:!/usr/bin/env python % <CR>
map <F1> gT
map <F2> gt
imap <F1> <c-c>gT
imap <F2> <c-c>gt
map <silent> <F3> :match ErrorMsg '\%>79v.\+'<CR>
imap <F4> <c-c>:NERDTreeToggle<Cr>
map <F4> :NERDTreeToggle<CR>
map Q gq
map <c-s> :update<CR>
imap <c-s> <c-c>:update<CR>
map ,v :tabnew ~/.vimrc<CR><C-W>
map <silent> ,V :source ~/.vimrc<CR>:filetype detect<CR>:exe ":echo 'vimrc reloaded'"<CR>

inoremap <expr> <C-Space> pumvisible() \|\| &omnifunc == '' ?
\ "\<lt>C-n>" :
\ "\<lt>C-x>\<lt>C-o><c-r>=pumvisible() ?" .
\ "\"\\<lt>c-n>\\<lt>c-p>\\<lt>c-n>\" :" .
\ "\" \\<lt>bs>\\<lt>C-n>\"\<CR>"
imap <C-@> <C-Space>

if has("vms")
  set nobackup		" do not keep a backup file, use versions instead
else
  set backup		" keep a backup file
endif

augroup vimrcEx
au!

  autocmd FileType text setlocal textwidth=78
  autocmd FileType python compiler pyunit
  autocmd FileType python setlocal makeprg=python
  autocmd FileType python set omnifunc=pythoncomplete#Complete
  autocmd FileType python set complete+=k~/.vim/syntax/python.vim
  autocmd FileType python set isk+=.
  autocmd FileType python set textwidth=79

augroup END
