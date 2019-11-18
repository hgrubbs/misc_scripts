#!/bin/sh -x

echo "installing pathogen"
mkdir -p ~/.vim/autoload ~/.vim/bundle && \
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim

echo "installing jedi-vim"
git clone --recursive https://github.com/davidhalter/jedi-vim.git ~/.vim/bundle/jedi-vim

echo "updating jedi-vim"
PWD=$(pwd)
cd ~/.vim/bundle/jedi-vim
git submodule update --init --recursive
cd ${PWD}
