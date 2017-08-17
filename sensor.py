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
import requests
import threading
import httpapp
import subprocess
import random
import dbutil

Devices = {}
Sensors = {}
LastRead = {}
Config = {}

#########################################################################
# Embedded sensors routine
#########################################################################

def UpdateSensorValue(Name,Value,logger):
    global Devices
    global Sensors
    global Config
    global LastRead

    timestamp = time.time()
    if Name in Sensors.keys():
        Sensors[Name].append((Value,timestamp))
        LastRead[Name] = (Value,timestamp)
        logger.info('Sensor [%s] read [%s]' % (Name,Value))
    else:
        logger.error('Update sensor [%s] failure' % Name)

def DoWunder(group,logger):

    if ('ApiKey' in group.keys()) and ('IDStation' in group.keys()):
        apikey = group['ApiKey']
        idstation = group['IDStation']
        resp = requests.get("http://api.wunderground.com/api/%s/conditions/q/pws:%s.json" % (apikey,idstation), data=None)
        data = resp.json()
        #print json.dumps(data, sort_keys=True, indent=4)

        for item in group['Peripherials']:

            sensor = group['Peripherials'][item]
            if sensor['Type'] == "temp_c":
                value = str(data["current_observation"]["temp_c"])
                print item,value
            elif sensor['Type'] == "relative_humidity":
                value = data["current_observation"]["relative_humidity"].split("%")[0]
                print item,value
            elif sensor['Type'] == "pressure_mb":
                value = str(data["current_observation"]["pressure_mb"])
                print item,value    
            elif sensor['Type'] == "wind_kph":
                value = str(data["current_observation"]["wind_kph"])
                print item,value

            UpdateSensorValue(item, value,logger)
    else:
        logger.error("Missing Apikey or IDStation")
        
def DoRandom(group,logger):

    for item in group['Peripherials']:

        sensor = group['Peripherials'][item]

        start_int = sensor['RangeMin']
        end_init = sensor['RangeMax']
        UpdateSensorValue(item, str(random.randint(start_int,end_init)),logger)
        

def DoCpuTempRead(group,logger):

    for item in group['Peripherials']:

        sensor = group['Peripherials'][item]

        bashCommand = "cat /sys/class/thermal/thermal_zone0/temp"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        UpdateSensorValue(item,output.strip(),logger)
        
#########################################################################
        
def run(logger,config):

    global Devices
    global Sensors
    global Config
    global LastRead

    logger.info("Thread started")

    Config = config
    db = dbutil.dbutil(config,logger)
    
    @httpapp.addurl('/get/sensor/')
    def getSensor(p,m):
        
        global Devices
        global Sensors
        global LastRead
        
        fields = p.split('/')
        if len(fields) == 4: 
            if fields[3] in LastRead.keys():
                value = LastRead[fields[3]][0]
                return '{"status":"ok","value":%s}' % value
            else:
                return '{"status":"error","value":"sensor not exist"}'  
        else:
            return '{"status":"error","value":"missing sensor name"}'

    @httpapp.addurl('/get/daily/')
    def getDaily(p,m):
        
        global Devices
        global Sensors
        global Config

        output = ""
        db = dbutil.dbutil(Config,logger)

        fields = p.split('/')
        if len(fields) == 4: 
            if fields[3] in Sensors.keys():
                data = db.GetSensorDaily(fields[3])
                return '{"status":"ok","value":%s}' % data
            else:
                return '{"status":"error","value":"sensor not exist"}'  
        else:
            return '{"status":"error","value":"missing sensor name"}'
        
    @httpapp.addurl('/get/sensor/config')
    def getSensorConfig(p,m):
        
        global Devices
        global Sensors

        return '{"status":"ok","value":%s}' % json.dumps(Groups, sort_keys=True)
        
    
    # Setup devices sensors and groups
    if "Sensors" not in config.keys():
        logger.error("No sensors has been yet configured")
        return
    
    Groups = config['Sensors']
    
    logger.info("Begin sensors setup")
    for key in Groups:
        group=Groups[key]
        if group['Status'] == 'On':
            Groups[key]['Timestamp'] = "NA"
            for item in group['Peripherials']:
                if item in Sensors.keys():
                    logger.error("Sensor %s duplicated" % item)
                elif item == "config":
                    logger.error("Invalid sensor name 'config' reserved keyword")
                Sensors[item] = []
                LastRead[item] = ("","")
                db.AddSensosrName(item)
                
                
    logger.info("End sensors setup")

    # Main sensor loop
    while(True):
        logger.info("Begin sensosrs polling")
        t = time.time()
        for key in Groups:
            group=Groups[key]
            if group['Status'] == 'On':
                if 'Delay' in Groups[key].keys() and Groups[key]['Timestamp'] != "NA":
                    if t-Groups[key]['Timestamp'] > Groups[key]['Delay']:
                        # Delayed group
                        Groups[key]['Timestamp'] = t
                        if group['Type'] == "random":
                            DoRandom(group,logger)
                        elif group['Type'] == "cputemp":
                            DoCpuTempRead(group,logger)
                        elif group['Type'] == "wunderground":
                            t = threading.Thread(target=DoWunder,args=(group,logger))
                            t.start()
                            
                else:
                    # Non delayed group
                    Groups[key]['Timestamp'] = t
                    if group['Type'] == "random":
                        DoRandom(group,logger)
                    elif group['Type'] == "cputemp":
                        DoCpuTempRead(group,logger)
                    elif group['Type'] == "wunderground":
                        t = threading.Thread(target=DoWunder,args=(group,logger))
                        t.start()
            
        logger.info("End sensors polling")
        time.sleep(float(config['SamplingPeriod']))
