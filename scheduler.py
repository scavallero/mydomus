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


#######################################################
# Activity routine
# config['HistoryPeriod'] minute between two activities
#######################################################

def doActivity(iday,config):

    global activity

    h = ((int(time.time())/(config['HistoryPeriod']*60)))*(config['HistoryPeriod']*60)
    db = dbutil.dbutil(config)
    
    logger.info("Begin daily activity")
    # Add measure average for the last 6 hours
    db.AddMeasureAverage(h-(config['HistoryPeriod']*60),h)
    logger.info("Average Window: %f %f" % (h-(config['HistoryPeriod']*60),h))
    if iday == 0:
        db.ClearSensorDaily()
    logger.info("End daily activity")
        
def run(config):

    # Wait for sensor setup completed
    time.sleep(10)
    
    db = dbutil.dbutil(config)
    last_iday = -1
    while(True):
        logger.info("Begin scheduler tasks")
        now = datetime.datetime.now()
        sday = now.hour*3600+now.minute*60+now.second # Seconds of the day
        iday = int(sday/(config['HistoryPeriod']*60)) # Interval of the day
        logger.info("Day interval %d " % iday)

        ###### Five minutes routine ######

        for name in sensor.AuxiliaryData
            # Begin critical thread safe operation
            sensor.AuxiliaryData[name] = []
            # End critical thread safe operation
            
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
                    if sensor.Metrics[name]["ZeroFill"]:
                        db.AddSensorValue(name,value,timestamp)                

        ###### In case start Acitivy ######
        if iday != last_iday:
            doActivity(iday,config)
            last_iday = iday

        logger.info("End scheduler tasks")
        time.sleep(300)
