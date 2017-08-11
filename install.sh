#!/bin/bash

service mydomus stop
rm -rf /usr/local/mydomus
cp -r $HOME/mydomus /usr/local
ln -s /usr/local/mydomus/mydomus.conf /usr/local/mydomus/html/mydomus.conf
chown -R www-data /usr/local/mydomus/html
