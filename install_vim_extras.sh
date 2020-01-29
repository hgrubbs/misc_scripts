#!/bin/sh -x
BASEDIR=$(pwd)

echo "installing pathogen"
mkdir -p ~/.vim/autoload ~/.vim/bundle && \
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim

echo "installing jedi-vim"
git clone --recursive https://github.com/davidhalter/jedi-vim.git ~/.vim/bundle/jedi-vim

echo "updating jedi-vim"
cd ~/.vim/bundle/jedi-vim
git submodule update --init --recursive
cd ${BASEDIR}

echo "installing logstash.vim"
cd ~/.vim/bundle
git clone https://github.com/prettier/vim-prettier
cd ${BASEDIR}

echo "installing vundle"
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim

cat vim/vimrc vim/vundle_vimrc > $HOME/.vimrc

echo "installing vundle plugin(s)"
vim +PluginInstall +qall
