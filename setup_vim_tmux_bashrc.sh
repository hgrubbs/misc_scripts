#!/bin/sh

echo "adding vimrc"
cp vim/vimrc ~/.vimrc

echo "adding tmux.conf"
cp tmux/tmux.conf ~/.tmux.conf

echo "adding bashrc template to .bashrc"
cat bash/bashrc >> ~/.bashrc
