#!/bin/sh -x

mkdir -p ~/.vim/bundle
echo "installing vundle"
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim

PWD=$(pwd)
cd ${PWD}
