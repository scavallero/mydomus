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
import logging
import dbutil
import pattern
import sensorload
import os
import auth


#########################################################################
# Module setup
########################################################################

logger = logging.getLogger("Mydomus")

Metrics = {}
Measures = {}
LastRead = {}
Config = {}

CWD = os.path.dirname(os.path.realpath(__file__))


#########################################################################
# Embedded sensors routine
#########################################################################

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def UpdateSensorValue(Name,Value):
    global Metrics
    global Measures
    global Config
    global LastRead

    timestamp = time.time()
    if Name in Measures.keys():
        if is_number(Value):
            Measures[Name].append((Value,timestamp))
            LastRead[Name] = (Value,timestamp)
            logger.info('Sensor [%s] read [%s]' % (Name,Value))
        else:
            logger.error('Update sensor [%s] failure for value [%s]' % (Name,Value))
    else:
        logger.error('Update sensor [%s] failure' % Name)

def DoWunder(group):

    if ('ApiKey' in group.keys()) and ('IDStation' in group.keys()):
        apikey = group['ApiKey']
        idstation = group['IDStation']
        resp = requests.get("http://api.wunderground.com/api/%s/conditions/q/pws:%s.json" % (apikey,idstation), data=None)
        data = resp.json()
        #print json.dumps(data, sort_keys=True, indent=4)

        for item in group['Metrics']:

            sensor = group['Metrics'][item]
            if sensor['Class'] == "temp_c":
                value = str(data["current_observation"]["temp_c"])
                print item,value
            elif sensor['Class'] == "relative_humidity":
                value = data["current_observation"]["relative_humidity"].split("%")[0]
                print item,value
            elif sensor['Class'] == "pressure_mb":
                value = str(data["current_observation"]["pressure_mb"])
                print item,value    
            elif sensor['Class'] == "wind_kph":
                value = str(data["current_observation"]["wind_kph"])
                print item,value
            elif sensor['Class'] == "precip_1hr":
                value = str(data["current_observation"]["precip_1hr_metric"])
                print item,value

            UpdateSensorValue(item, value)
    else:
        logger.error("Missing Apikey or IDStation")
        
def DoRandom(group):

    for item in group['Metrics']:

        sensor = group['Metrics'][item]

        start_int = sensor['RangeMin']
        end_init = sensor['RangeMax']
        UpdateSensorValue(item, str(random.randint(start_int,end_init)))
        

def DoCpuTempRead(group):

    for item in group['Metrics']:

        sensor = group['Metrics'][item]

        bashCommand = "cat /sys/class/thermal/thermal_zone0/temp"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        UpdateSensorValue(item,output.strip())

def DoAurora(group):

    for item in group['Metrics']:

        sensor = group['Metrics'][item]
        value = "NA"

        bashCommand = "aurora -a %d -Y6 -d0 %s " % (sensor['Address'],sensor['Port'])
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        for w in output.split('\n'):
            if "Grid Power Reading" in w:
                value = "%.1f" % float(w.split('=')[1].strip().split(' ')[0])
        UpdateSensorValue(item,value)
        
def CheckExtCmd(group):
    result = True
    for item in group['Metrics']:

        sensor = group['Metrics'][item]

        if "command" not in sensor.keys():
            result = False
            logger.error("Missing 'command' parameter for extcmd group")
        if "pattern" not in sensor.keys():
            result = False
            logger.error("Missing 'pattern' parameter for extcmd group")
        if "value" not in sensor.keys():
            result = False
            logger.error("Missing 'value' parameter for extcmd group")
        if "unit" not in sensor.keys():
            result = False
            logger.error("Missing 'unit' parameter for extcmd group")
            
            
    return result

def DoExtCmd(group):

    for item in group['Metrics']:

        sensor = group['Metrics'][item]
        #bashCommand = os.path.join(".","plugins",sensor['command'])
        bashCommand = os.path.join(CWD,"plugins",sensor['Command'])
        logger.debug("ExtCmd: "+bashCommand)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,cwd=os.path.join(CWD,"plugins"))
        output, error = process.communicate()

        p = pattern.parser()
        p.check(sensor['Pattern'],output)
        logger.debug("Result: "+output)
        UpdateSensorValue(item,p.field[sensor['Value']-1].strip())
        
                
        
#########################################################################
        
def run(config):

    global Metrics
    global Measures
    global Config
    global LastRead

    logger.info("Thread started")

    #######################################################
    # Setup Sensors
    #######################################################

    db = dbutil.dbutil(config)
    config = sensorload.load(config)
    
    if "Sensors" not in config.keys():
        logger.error("No sensors has been yet configured")
        return
    
    Sensors = config['Sensors']
    
    logger.info("Begin sensors setup")
    for key in Sensors:
        group=Sensors[key]
        if group['Status'] == 'On':
            Sensors[key]['Timestamp'] = "NA"
            for item in group['Metrics']:
                if item in Measures.keys():
                    logger.error("Sensor %s duplicated" % item)
                elif item == "config":
                    logger.error("Invalid sensor name 'config' reserved keyword")
                Measures[item] = []
                Metrics[item] = group['Metrics'][item]
                Metrics[item]["SensorName"] = key

                # Add YLabel and Unit if not exist
                if "Unit" not in Metrics[item].keys():
                    Metrics[item]["Unit"] = ""
                if "YLabel" not in Metrics[item].keys():
                    Metrics[item]["YLabel"] = ""
                
                LastRead[item] = ("","")
                db.AddSensosrName(item)
                
                
    logger.info("End sensors setup")
    
    Config = config
    
    
    @httpapp.addurl('/get/sensor/')
    def getSensor(p,m):
        
        global Metrics
        global Measures
        global LastRead

        p = auth.decodeUrlToken(p)
        if p:
            fields = p.split('/')
            if len(fields) == 4: 
                if fields[3] in LastRead.keys():
                    value = LastRead[fields[3]][0]
                    ylabel = Metrics[fields[3]]['YLabel']
                    unit = Metrics[fields[3]]['Unit']
                    return '{"status":"ok","value":%s,"ylabel":"%s","unit":"%s"}' % (value,ylabel,unit)
                else:
                    return '{"status":"error","value":"sensor not exist"}'  
            else:
                return '{"status":"error","value":"missing sensor name"}'
        else:
            return '{"status":"error","value":"token authorization failure"}'

    @httpapp.addurl('/get/daily/')
    def getDaily(p,m):
        
        global Metrics
        global Measures
        global Config

        output = ""
        db = dbutil.dbutil(Config)

        p = auth.decodeUrlToken(p)
        if p:
            fields = p.split('/')
            if len(fields) == 4: 
                if fields[3] in Measures.keys():
                    data = db.GetSensorDaily(fields[3])
                    ylabel = Metrics[fields[3]]['YLabel']
                    unit = Metrics[fields[3]]['Unit']
                    
                    return '{"status":"ok","value":%s,"ylabel":"%s","unit":"%s"}' % (data,ylabel,unit)
                else:
                    return '{"status":"error","value":"sensor not exist"}'  
            else:
                return '{"status":"error","value":"missing sensor name"}'
        else:
            return '{"status":"error","value":"token authorization failure"}'

    @httpapp.addurl('/get/history/')
    def getHistory(p,m):
        
        global Metrics
        global Measures
        global Config

        output = ""
        db = dbutil.dbutil(Config)

        p = auth.decodeUrlToken(p)
        if p:
            fields = p.split('/')
            if len(fields) == 5: 
                if fields[3] in Measures.keys():
                    if fields[4] == 'null':
                        avg,rng = db.GetSensorHistory(fields[3],False)
                    else:
                        avg,rng = db.GetSensorLastdays(fields[3],True,days=int(fields[4]))
                    ylabel = Metrics[fields[3]]['YLabel']
                    unit = Metrics[fields[3]]['Unit']
                    return '{"status":"ok","avg":%s,"rng":%s,"ylabel":"%s","unit":"%s"}' % (avg,rng,ylabel,unit)
                else:
                    return '{"status":"error","value":"sensor not exist"}'  
            else:
                return '{"status":"error","value":"missing sensor name"}'
        else:
            return '{"status":"error","value":"token authorization failure"}' 
        
    @httpapp.addurl('/get/sensor/config/')
    def getSensorConfig(p,m):
        
        global Metrics
        global Measures

        p = auth.decodeUrlToken(p)
        if p:
            return '{"status":"ok","value":%s}' % json.dumps(Sensors, sort_keys=True)
        else:
            return '{"status":"error","value":"token authorization failure"}'         


    ######################################################
    # Main sensor loop
    ######################################################
    while(True):
        logger.info("Begin sensosrs polling")
        t = time.time()
        for key in Sensors:
            group=Sensors[key]
            if group['Status'] == 'On':
                if 'Delay' in Sensors[key].keys() and Sensors[key]['Timestamp'] != "NA":
                    if t-Sensors[key]['Timestamp'] > Sensors[key]['Delay']:
                        # Delayed group
                        Sensors[key]['Timestamp'] = t
                        if group['Type'] == "random":
                            DoRandom(group)
                        elif group['Type'] == "cputemp":
                            DoCpuTempRead(group)
                        elif group['Type'] == "aurora":
                            DoAurora(group)
                        elif group['Type'] == "extcmd":
                            DoExtCmd(group)
                        elif group['Type'] == "wunderground":
                            t = threading.Thread(target=DoWunder,args=(group,))
                            t.start()
                            
                else:
                    # Non delayed group
                    Sensors[key]['Timestamp'] = t
                    if group['Type'] == "random":
                        DoRandom(group)
                    elif group['Type'] == "cputemp":
                        DoCpuTempRead(group)
                    elif group['Type'] == "aurora":
                        DoAurora(group)
                    elif group['Type'] == "extcmd":
                        DoExtCmd(group)
                    elif group['Type'] == "wunderground":
                        t = threading.Thread(target=DoWunder,args=(group,))
                        t.start()
            
        logger.info("End sensors polling")
        time.sleep(float(config['SamplingPeriod']))
