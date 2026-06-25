#!/bin/bash
set -e

# install everything necessary
sudo apt update
yes | sudo apt install libboost-all-dev libantlr3c-dev build-essential libglib2.0-dev docker.io python3-pip
yes | sudo apt install texlive texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra dvipng cm-super
pip install matplotlib

# install rust (stable; the artifact's Cargo.lock resolves dependencies that
# require a current edition2024-capable toolchain, so don't pin to an old version)
yes | sudo apt remove rustc cargo
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
echo 'export PATH=$HOME/.cargo/bin:$PATH' >> $HOME/.bashrc
source $HOME/.cargo/env
rustup install stable
rustup default stable

# move files around to the blockstore with enough room...
sudo chmod ugo+rw -R /data
sudo rm -rf /data/repository
git clone https://github.com/MaryAyobami/edna.git /data/repository
cd /data/repository
git checkout cloudlab-repro-fixes
yes | ./config_mysql.sh
cd related_systems/qapla
make; cd examples; make

# done with setup, run everything via ./run_all.sh
