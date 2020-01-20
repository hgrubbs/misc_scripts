FROM ubuntu:bionic

#packages
RUN apt-get update && apt-get install -y git tmux build-essential npm htop openssh-client vim python3.8 python3.8-dev python3.8-venv python3-distutils wget curl tree rsync

#python3.8 pip
RUN cd /root && wget https://bootstrap.pypa.io/get-pip.py && python3.8 get-pip.py

#ipython
RUN python3.8 -m pip install ipython

#misc_scripts
RUN cd /root && git clone https://github.com/hgrubbs/misc_scripts
RUN cd /root/misc_scripts && ./setup_vim_tmux_bashrc.sh && ./install_pathogen_and_jedi.sh

#ttystudio
RUN npm install -g ttystudio

CMD cd /root && /bin/bash
