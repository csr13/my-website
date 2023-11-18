#!/bin/bash


root_loc="/var/www/html/"

echo "Copying index to $root_loc"

cp index.html /var/www/html/index.html

echo "Copying keybase.txt to $root_loc"

cp keybase.txt /var/www/html/keybase.txt

echo "Copying pages dir to $root_loc"

cp -r pages /var/www/html/

echo "Copying static dir to $root_loc"

cp -r static /var/www/html/

echo "Coping media dir to $root_loc"

cp -r media /var/www/html/

is_active=$(systemctl is-active nginx)

if [ $is_active = active ]; then
    echo "Server active";
else
    echo "Starting reverse proxy .."
    systemctl restart nginx.service
    if [ $(systemctl is-active nginx) = active ]; then
        echo "Reverse proxy running ..."
    else
        echo "Check reverse proxy settings .."
    fi
fi

echo "Changing $root_loc ownsership to www-data:www-data"

chown www-data:www-data -R /var/www/html

