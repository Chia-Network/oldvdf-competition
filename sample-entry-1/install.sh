#!/bin/sh
sudo apt-get install libgmp3-dev
g++ -O3 vdf.cpp -lgmpxx -lgmp
