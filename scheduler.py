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
import datetime
import sensor
import logging
import dbutil

#########################################################################
# Module setup
########################################################################

logger = logging.getLogger("Mydomus")
activity = [True]*4

def doActivity(a,config):

    global activity

    h = ((int(time.time())/3600))*3600
    db = dbutil.dbutil(config)
    
    if activity[a]:
        logger.info("Begin daily activity")
        activity[a] = False
        # Add measure average for the last 6 hours
        db.AddMeasureAverage(h-6*3600,h)
        logger.info("Average Window: %f %f" % (h-6*3600,h))
        if a == 0:
            activity[3] = True
            db.ClearSensorDaily()
        else:
            activity[a-1] = True
        logger.info("End daily activity")
    
def run(config):

    # Wait for sensor setup completed
    time.sleep(10)
    
    db = dbutil.dbutil(config)
    while(True):
        logger.info("Begin scheduler tasks")
        now = datetime.datetime.now()
        
        for name in sensor.Measures:

            # Begin critical thread safe operation
            measure = sensor.Measures[name]
            sensor.Measures[name] = []
            # End critical thread safe operation

            # Compute average value
            if len(measure) > 0:
                timestamp = 0.0
                value= 0.0
                for i in range(len(measure)):
                    value = value + float(measure[i][0])
                    timestamp = timestamp + measure[i][1]
                value = value / float(len(measure))
                timestamp = timestamp  / float(len(measure))
                db.AddSensorValue(name,value,timestamp)
            else:
                # If no valid measure zero insert
                timestamp = time.time()
                value= 0.0
                if "ZeroFill" in sensor.Metrics[name].keys():
                    if sensor.Metrics[name]["ZeroFill"] == "True":
                        db.AddSensorValue(name,value,timestamp)                

        if now.hour % 6 == 0:
            doActivity(now.hour/6,config)

        logger.info("End scheduler tasks")
        time.sleep(300)
