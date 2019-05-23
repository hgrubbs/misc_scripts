#!/bin/bash
mkdir -p ~/local/{bin,log}
echo 'set -o vi' >> ~/.bashrc
echo "alias rm='rm -i'" >> ~/.bashrc
echo "alias cp='cp -i'" >> ~/.bashrc
cp ../vim/vimrc ~/.vimrc
cp ../tmux/tmux.conf ~/.tmux.conf
cp ubuntu_tweaks.sh ~/local/bin/
cat bashrc >> ~/.bashrc
