#!/bin/bash

export CONFIG=/home/pi/config.yml
gunicorn --workers 2 --bind unix:web_ctl.sock -m 007 src:app
