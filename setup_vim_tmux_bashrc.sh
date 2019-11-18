#!/bin/sh

echo "adding vimrc"
cp vim/vimrc ~/.vimrc

echo "adding tmux.conf"
cp tmux/tmux.conf ~/.tmux.conf

echo "adding bashrc template to .bashrc"
echo '# ---BEGIN misc_scripts bashrc---' >> ~/.bashrc
cat bash/bashrc >> ~/.bashrc
echo "# ---END misc_scripts bashrc---" >> ~/.bashrc
