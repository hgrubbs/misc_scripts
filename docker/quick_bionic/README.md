# quick_bionic ephemeral docker container

This Dockerfile builds a container off ubuntu/bionic, which contains:

1. tmux
2. tmate
3. openssh-client with keys generated when container is built
4. vim (with jedi and my .vimrc)
5. python3.8, pip3.8, ipython
6. bind-mount to share files from host's `$HOME/mnt/quick_bionic` to containers `/mnt/quick_bionic`

Some additional convenience like locale (with en_US.UTF-8 configured) are also included.

## Requirements to run

1. pwgen (used to generate short semi-pronouncable container names)
2. docker

## Quickstart (assuming Ubuntu/Debian)

1. `sudo apt install pwgen docker-ce docker-ce-cli containerd.io`

   Need docker repos? see https://docs.docker.com/install/linux/docker-ce/ubuntu/

2. `cat bashrc >> $HOME/.bashrc` (this adds the `quick_bionic` alias)
3. `docker build -t local:bionic-latest .`
4. `mkdir -p $HOME/mnt/quick_bionic` (create the shared mount point)

All done! Test it out by sourcing `.bashrc` (or opening a new shell), and typing `quick_bionic`
