filetype plugin indent on
" show existing tab with 4 spaces width
set tabstop=4
" when indenting with '>', use 4 spaces width
set shiftwidth=4
" On pressing tab, insert 4 spaces
set expandtab

:set number
:set ruler
:set showcmd
:set cursorline
:set background=dark
:set hlsearch
:syntax enable
:colorscheme gruvbox

" Configure cursor line to suit Pro profile theme of terminal
hi cursorline cterm=underline ctermbg=black

" turn off search highlight
let mapleader=","       " leader is comma
nnoremap <leader><space> :nohlsearch<CR>

" move vertically by visual line
nnoremap j gj
nnoremap k gk

" Allow backward compatibility for latest version of vim in insert mode
set backspace=indent,eol,start

" Powerline
" Note: Update python directory if version is more later
set rtp+=/usr/local/lib/python3.7/site-packages/powerline/bindings/vim
set laststatus=2
set t_Co=256
