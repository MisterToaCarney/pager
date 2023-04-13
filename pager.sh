#!/bin/sh


python3 zmq_listen.py $1 | multimon-ng -c -a POCSAG512 -a POCSAG1200 -a POCSAG2400 -a FLEX -

# play -t raw -r 22050 -es -b 16 -c 1 -V1 -