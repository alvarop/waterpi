#!/bin/bash

echo "Updating nginx config setup"
sudo rm -f /etc/nginx/sites-enabled/default
sudo cp support/nginx_web_ctl /etc/nginx/sites-enabled/web_ctl

sudo rm -f /etc/nginx/nginx.conf
sudo cp support/nginx.conf /etc/nginx/nginx.conf

echo "Updating supervisor config setup"
sudo rm -f /etc/supervisor/conf.d/web_ctl.conf
sudo cp support/web_ctl.conf /etc/supervisor/conf.d/web_ctl.conf

sudo rm -f /etc/supervisor/conf.d/water.conf
sudo cp support/water.conf /etc/supervisor/conf.d/water.conf

echo "restart nginx"
sudo systemctl restart nginx

echo "restart supervisor"
sudo systemctl restart supervisor

