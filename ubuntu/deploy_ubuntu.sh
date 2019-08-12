#!/bin/bash
mkdir -p ~/local/{bin,log}
cp ../vim/vimrc ~/.vimrc
cp ../tmux/tmux.conf ~/.tmux.conf
cp ubuntu_tweaks.sh ~/local/bin/
cat ../bash/bashrc >> ~/.bashrc
cat bashrc >> ~/.bashrc
