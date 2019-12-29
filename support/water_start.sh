#!/bin/bash

# Make sure we're in the right directory
cd `git rev-parse --show-toplevel`

python3 water.py /home/pi/config.yml --sleep 5

