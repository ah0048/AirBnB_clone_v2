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
for dir in /data /data/web_static /data/web_static/releases /data/web_static/shared/ /data/web_static/releases/test; do
    if ! [ -d "$dir" ]; then
        sudo mkdir -p "$dir"
    fi
done
echo "Hello World!, I'm deploying static content." | sudo tee /data/web_static/releases/test/index.html > /dev/null
if [ -L '/data/web_static/current' ]; then
    sudo rm '/data/web_static/current'
fi
sudo ln -s '/data/web_static/releases/test/' '/data/web_static/current'


sudo chown -R "$USER":"$GROUP" /data/
sudo sed -i '/^server {/a\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

sudo service nginx restart
