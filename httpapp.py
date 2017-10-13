#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   httpd
#   HTTP Daemon 
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


import BaseHTTPServer
import inspect
import logging
import logging.handlers

# Callback dicrionary

urlf={}
errorf=None

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler_stream = logging.StreamHandler()
formatter = logging.Formatter('*** %(asctime)s %(levelname)-8s %(message)s')
handler_stream.setFormatter(formatter)
logger.addHandler(handler_stream)

def addurl(path):
    def decorator(f):
        global urlf
        urlf[path]=f
        if path[-1] == '/' and path != '/':
            urlf[path[:-1]]=f
        return f
    return decorator

def error_default(path,command):
    return '{"status":"error","value":"undefined url %s","methd":"%s"}' % (path,command)

def log_default(format, *args):
    logger.info(format % args)

class handler_class(BaseHTTPServer.BaseHTTPRequestHandler):
    def _set_headers(self,value):
        self.send_response(value)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def log_message(self, format, *args):
        log_default(format,*args)
        
    def do_GET(self):
        global urlf
        global errorf
        
        if self.path in urlf.keys():
            self._set_headers(200)
            self.wfile.write(urlf[self.path](self.path,self.command))
            return
        else:
            k = self.path.rfind('/')
            subpath = self.path[:k+1]
            while subpath != '/':
                if subpath in urlf.keys():
                    self._set_headers(200)
                    a = len(inspect.getargspec(urlf[subpath]).args)
                    if a == 1:
                        self.wfile.write(urlf[subpath](self.path))
                    elif a == 2:
                        self.wfile.write(urlf[subpath](self.path,self.command))
                    elif a == 3:
                        self.wfile.write(urlf[subpath](self.path,self.command,None))
                    return
                else:
                    k = subpath[:-1].rfind('/')
                    subpath = subpath[:k+1]

        self._set_headers(400)
        self.wfile.write(errorf(self.path,self.command))
        
    def do_POST(self):
        global urlf
        global errorf

        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)

        if self.path in urlf.keys():
            self._set_headers(200)
            self.wfile.write(urlf[self.path](self.path,self.command),post_body)
            return
        else:
            k = self.path.rfind('/')
            subpath = self.path[:k+1]
            while subpath != '/':
                if subpath in urlf.keys():
                    self._set_headers(200)
                    a = len(inspect.getargspec(urlf[subpath]).args)
                    if a == 1:
                        self.wfile.write(urlf[subpath](self.path))
                    elif a == 2:
                        self.wfile.write(urlf[subpath](self.path,self.command))
                    elif a == 3:
                        self.wfile.write(urlf[subpath](self.path,self.command,post_body))
                    return
                else:
                    k = subpath[:-1].rfind('/')
                    subpath = subpath[:k+1]

        self._set_headers(400)
        self.wfile.write(errorf(self.path,self.command))
        
def run(port=80,error_handler=error_default,log_handler=None):
    global errorf
    global logger
    errorf = error_handler
    server_address = ('', port)
    if log_handler is not None:
        logger = log_handler
    httpd = BaseHTTPServer.HTTPServer(server_address, handler_class)
    logger.info("Httpapp service started on port %d" % port)
    httpd.serve_forever()






