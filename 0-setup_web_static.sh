#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static
USER='ubuntu'
GROUP='ubuntu'
if ! nginx -v > /dev/null 2>&1; then
    sudo apt-get -y update
    sudo apt-get -y upgrade
    sudo apt-get -y install nginx
    sudo ufw allow 'Nginx HTTP'
    sudo service nginx start
fi
if ! [ -d '/data/' ]; then
    mkdir -p '/data/'
fi
if ! [ -d '/data/web_static/' ]; then
    mkdir -p '/data/web_static/'
fi
if ! [ -d '/data/web_static/releases/' ]; then
    mkdir -p '/data/web_static/releases/'
fi
if ! [ -d '/data/web_static/shared/' ]; then
    mkdir -p '/data/web_static/shared/'
fi
if ! [ -d '/data/web_static/releases/test/' ]; then
    mkdir -p '/data/web_static/releases/test/'
fi
echo "Hello World!, I'm deploying static content." > /data/web_static/releases/test/index.html
if [ -L '/data/web_static/current' ]; then
    rm '/data/web_static/current'
    ln -s '/data/web_static/releases/test/' '/data/web_static/current'
else
    ln -s '/data/web_static/releases/test/' '/data/web_static/current'
fi
sudo chown -R "$USER":"$GROUP" /data/
sudo sed -i '/listen [::]:80 default_server;/a\\tlocation /hbnb_static { alias /data/web_static/current/; }' /etc/nginx/sites-available/default
sudo service nginx restart
