#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   MyDomus - Polling Service
#   Copyright (c) 2016 Salvatore Cavallero (salvatoe.cavallero@gmail.com)
#   https://github.com/scavallero/mydomus
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import time
import json
import hashlib
import logging
import httpapp
import os

#########################################################################
# Module setup
########################################################################

logger = logging.getLogger("Mydomus")

user = {}

def load():
    global user
    logger.info("Start loading user authorization")
    CWD = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(CWD,"user.conf")) as data_file:
            try:
                user = json.load(data_file)
            except ValueError:  # includes simplejson.decoder.JSONDecodeError
                logger.error('json decoding failure user.conf')

    for item in user.keys():
        h = hashlib.sha224(item+user[item]['password']).hexdigest()
        p = hashlib.md5(user[item]['password']).hexdigest()
        user[item]['token'] = h
        user[item]['password'] = p
        logger.info('User: %s - %s' % (item,h))

    ### ADDED API ###

    @httpapp.addurl('/verify/')
    def root(p,m):
        
        global user

        fields = p.split('/')
        if len(fields) == 4:
            if fields[2] in user.keys():
                if fields[3] == user[fields[2]]['password']:
                    return '{"status":"ok","token":"%s"}' % user[fields[2]]['token']
                else:
                    return '{"status":"error","reason":"wrong password"}'        
            else:
                return '{"status":"error","reason":"user unknown"}'  
        else:
            return '{"status":"error","reason":"missing user or password"}'
        

    logger.info("User authorization loaded")
                

def verifyUser(usr,pswd):

    res = False
    
    if usr in user.keys():
        if user[usr]['password'] == pswd:
            res = True

    return res
    
def verifyToken(token):

    res = False
    usr = ""
    
    for item in user.keys():
        if 'token' in user[item].keys():
            if user[item]['token'] == token:
                res = True
                usr = item

    return res,usr

def decodeUrlToken(url):

    fields = url.split('/')
    token = fields[-1]
    del fields[-1]

    new_url = ''
    for item in fields:
        if item != '':
            new_url = new_url + '/'+item

    if new_url == '':
        new_url = '/'
        
    res,usr = verifyToken(token)
    
    if res:
        return new_url
    else:
        return None

