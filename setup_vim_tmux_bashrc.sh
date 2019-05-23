#!/bin/sh

echo "adding vimrc"
cp vim/vimrc ~/.vimrc

echo "adding tmux.conf"
cp tmux/tmux.conf ~/.tmux.conf

echo "adding set -o vi to .bashrc"
echo "set -o vi" >> ~/.bashrc
