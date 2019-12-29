#!/bin/bash

sudo apt-get install -y python3 python3-pip supervisor nginx git
sudo pip3 install flask gunicorn pyyaml

# Make sure www-data can read db file created by pi user
sudo usermod -a -G www-data pi

echo "Please reboot or log out/in for changes to take effect"
echo "Don't forget to run raspi-config to change timezone to correct one"

