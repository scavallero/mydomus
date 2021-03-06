#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   MyDomus
#   Home Domotic Service
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

import sys
import argparse  
import json
import threading
import httpapp
import sensor
import scheduler
import logging
import logging.handlers
import dbutil
import auth

## Self defined summary log handler ##

class SummaryHandler(logging.Handler):

    def __init__(self,bufferlen=100):
        logging.Handler.__init__(self)
        self.bufferlen = bufferlen
        self.buffered_entry = []
        
    def emit(self, record):
        log_entry = self.format(record)
        self.buffered_entry.append(log_entry)
        if len(self.buffered_entry) > self.bufferlen:
            del self.buffered_entry[0]
        
## SETUP DEFAULTS AND LOGGER ##

CONFIG_DIR = "."
LOG_LEVEL = logging.DEBUG
VERSION = "1.0"


parser = argparse.ArgumentParser(description="Mydomus")
parser.add_argument("-c", "--confdir", help="config directory (default '" + CONFIG_DIR + "')")

args = parser.parse_args()
if args.confdir:
    CONFIG_DIR = args.confdir

# Reads Config
with open(CONFIG_DIR+'/mydomus.conf') as data_file:    
    config = json.load(data_file)

LOG_FILENAME = config["LogFileName"]
SERVER_ADDR = config["ServerAddress"]
SERVER_PORT = config["ServerPort"]
        
logger = logging.getLogger("Mydomus")
logger.setLevel(LOG_LEVEL)
handler_logfile = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=30)
handler_stream = logging.StreamHandler()
handler_summary = SummaryHandler()
handler_summary.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(module)-10s %(message)s')
handler_logfile.setFormatter(formatter)
handler_stream.setFormatter(formatter)
handler_summary.setFormatter(formatter)
logger.addHandler(handler_logfile)
logger.addHandler(handler_stream)
logger.addHandler(handler_summary)

if "RedirectOutput" in config.keys():
    if config["RedirectOutput"]:
        sys.stderr = open('/var/log/mydomus/stderr.log', 'w')
        sys.stdouy = open('/var/log/mydomus/stdout.log', 'w')
        
### ADDED API ###

@httpapp.addurl('/')
def root(p,m):
    msg = {}
    msg["status"]="ok",
    msg["version"]=VERSION
    msg["log"] = handler_summary.buffered_entry

    return json.dumps(msg, sort_keys=True, indent=4)



if __name__ == "__main__":
    logger.info("Mydomus service started")
    auth.load()
    db = dbutil.dbutil(config)
    db.InitDB()
    t1 = threading.Thread(target=sensor.run,args=(config,))
    t1.start()
    t2 = threading.Thread(target=scheduler.run,args=(config,))
    t2.start()    
    httpapp.run(port=SERVER_PORT,log_handler=logger)
    logger.info("*** EXIT ***")




