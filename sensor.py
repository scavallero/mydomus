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
import traceback


#########################################################################
# Module setup
########################################################################

logger = logging.getLogger("Mydomus")

Metrics = {}
Measures = {}
AuxiliaryData = {}
LastRead = {}
Config = {}
Callbacks = {}
Handlers = {}

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
            logger.warning('Update sensor [%s] failure for value [%s]' % (Name,Value))
    else:
        logger.warning('Update sensor [%s] failure' % Name)

def UpdateAuxiliaryData(Name,Value):
    global AuxiliaryData
    global Config

    Sensors = Config['Sensors']
    timestamp = time.time()
    if Name in Sensors.keys():
        AuxiliaryData[Name].append((Value,timestamp))
        logger.info('Auxiliary data for group [%s] success' % Name)
    else:
        logger.warning('Auxiliary data for group [%s] failure' % Name)


#############################################################
#####               Wunderground Sensor                 #####
#############################################################
        
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

#############################################################
#####                  Random Sensor                    #####
#############################################################
        
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

#############################################################
#####                  Aurora Sensor                    #####
#############################################################
        
def DoAurora(group):

    bashCommand = "aurora -a %d -Y6 -d0 -e %s " % (group['Address'],group['Port'])
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
        
    for item in group['Metrics']:
        sensor = group['Metrics'][item]
        value = "NA"
        for w in output.split('\n'):
            if "Grid Power Reading" in w and  group['Metrics'][item]['Class'] == "power":
                value = "%.1f" % float(w.split('=')[1].strip().split(' ')[0])
                UpdateSensorValue(item,value)
            if "Daily Energy " in w and  group['Metrics'][item]['Class'] == "energy":
                value = "%.2f" % float(w.split('=')[1].strip().split(' ')[0])
                UpdateSensorValue(item,value)

#############################################################
#####                  WeThermo Sensor                  #####
#############################################################
                
def DoWethermo(group):

    if ('Address' in group.keys()):
        resp = requests.get("http://%s/info" % group['Address'])
        data = resp.json()
        UpdateAuxiliaryData(group['Name'],data)
        
        for item in group['Metrics']:

            sensor = group['Metrics'][item]
            if sensor['Class'] == "wethermo_temp":
                value = str(data["Temp"])
                
            UpdateSensorValue(item, value)
    else:
        logger.error("Missing Address field for WeThermo")

def CallWethermo(m,b):

    global Metrics
    global Config
    
    Sensors = Config['Sensors']

    logger.info("WeThermo call -> Metrics: %s, Body: %s" % (m,b))
        
    req = json.loads(b)
    group = Sensors[Metrics[m]['SensorName']]
    
    if 'value' in req:
        if ('Address' in group.keys()):
            if req['value'] == 4:
                resp = requests.get("http://%s/display" % group['Address'])
                return '{"status":"ok","request":%s,"response":"%s"}' % (b,resp.text)
        else:
            return '{"status":"error","value":"missing address in wethermo config","request":%s}' % b   
    else:
        return '{"status":"error","value":"missing value field in request","request":%s}' % b
    
#############################################################
#####                   SDM230 Sensor                   #####
#############################################################

def DoSdm230(group):

    try:
        import minimalmodbus
    except:
        #logger.error(traceback.format_exc())
        logger.error("Missing required library (minimalmodbus) for SDM230 sensor ")
        group['Status'] = "Off" # Disable sensor 
        return

    if "Port" not in group.keys():
        logger.error("Missing Port field for SDM230 sensor ")
        group['Status'] = "Off" # Disable sensor
        return

    if "Baudrate" not in group.keys():
        logger.error("Missing Baudrate field for SDM230 sensor ")
        group['Status'] = "Off" # Disable sensor
        return

    try:
        rs485 = minimalmodbus.Instrument(group["Port"], 1)
        rs485.serial.baudrate = group["Baudrate"]
        rs485.serial.bytesize = 8
        rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
        rs485.serial.stopbits = 1
        rs485.serial.timeout = 1
        rs485.debug = False
        rs485.mode = minimalmodbus.MODE_RTU
    except:
        logger.error("Can't open SDM230 device")
        return

    for item in group['Metrics']:

        sensor = group['Metrics'][item]
        if sensor['Class'] == "active_power":
            value = "%.1f" % rs485.read_float(12, functioncode=4, numberOfRegisters=2)
            UpdateSensorValue(item, value)
        if sensor['Class'] == "volts":
            value = "%.1f" % rs485.read_float(0, functioncode=4, numberOfRegisters=2)
            UpdateSensorValue(item, value)
        if sensor['Class'] == "current":
            value = "%.1f" % rs485.read_float(6, functioncode=4, numberOfRegisters=2)
            UpdateSensorValue(item, value)
        if sensor['Class'] == "reactive_power":
            value = "%.1f" % rs485.read_float(24, functioncode=4, numberOfRegisters=2)
            UpdateSensorValue(item, value)
        if sensor['Class'] == "power_factor":
            value = "%.1f" % rs485.read_float(30, functioncode=4, numberOfRegisters=2)
            UpdateSensorValue(item, value)


#############################################################
#####                External API Sensor                #####
#############################################################
        
def CallApi(m,b):
    
    req = json.loads(b)
    if 'value' in req:
        UpdateSensorValue(m,req['value'])
        return '{"status":"ok","request":%s}' % b
    else:
        return '{"status":"error","value":"missing value field in request","request":%s}' % b

#############################################################
#####                External CMD Sensor                #####
#############################################################
    
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
    global AuxiliaryData
    global Config
    global LastRead
    global Callbacks
    global Handlers

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
        Sensors[key]['Name'] = key
        group=Sensors[key]
        AuxiliaryData[key] = []
        
        # ##### Setup Handlers ##### #
        Callbacks[key] = None
        Handlers[key] = None
        
        if group['Type'] == "random":
            Handlers[key]=DoRandom
        elif group['Type'] == "cputemp":
            Handlers[key]=DoCpuTempRead
        elif group['Type'] == "aurora":
            Handlers[key]=DoAurora
        elif group['Type'] == "extcmd":
            Handlers[key]=DoExtCmd
        elif group['Type'] == "wunderground":
            Handlers[key]=DoWunder
        elif group['Type'] == "wethermo":
            Handlers[key]=DoWethermo
            Callbacks[key]=CallWethermo
        elif group['Type'] == "sdm230":
            Handlers[key]=DoSdm230
        elif group['Type'] == "api":
            Callbacks[key]=CallApi
            
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
                db.AddSensor(item,group['Type'],Metrics[item]['Class'])
                
                
    logger.info("End sensors setup")
    
    Config = config
    
    @httpapp.addurl('/call/sensor/')
    def callSensor(p,m,b=None):
        
        global Metrics
        global Callbacks

        p = auth.decodeUrlToken(p)

        if p:
            if b is not None:
                try:
                    req = json.loads(b) 
                    fields = p.split('/')
                    if len(fields) == 4: 
                        if fields[3] in Metrics.keys():
                            sensorname = Metrics[fields[3]]['SensorName']
                            if sensorname in Callbacks.keys():
                                if Callbacks[sensorname] is not None:
                                    return Callbacks[sensorname](fields[3],b)
                                else:
                                    return '{"status":"error","value":"callback is none"}'
                            else:
                                return '{"status":"error","value":"callback not registered"}'
                        else:
                            return '{"status":"error","value":"sensor not exist"}'
                    else:
                        return '{"status":"error","value":"missing sensor name"}'
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    return '{"status":"error","value":"json decoding error","body":"%s"}' % b 
            else:
                return '{"status":"error","value":"missing body"}'
        else:
            return '{"status":"error","value":"token authorization failure"}'        

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
                    mclass = Metrics[fields[3]]['Class']
                    return '{"status":"ok","value":%s,"ylabel":"%s","unit":"%s","mclass":"%s"}' % (value,ylabel,unit,mclass)
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
                    mclass = Metrics[fields[3]]['Class']
                    return '{"status":"ok","value":%s,"ylabel":"%s","unit":"%s","mclass":"%s"}' % (data,ylabel,unit,mclass)
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
                    mclass = Metrics[fields[3]]['Class']
                    return '{"status":"ok","avg":%s,"rng":%s,"ylabel":"%s","unit":"%s","mclass":"%s"}' % (avg,rng,ylabel,unit,mclass)
                else:
                    return '{"status":"error","value":"sensor not exist"}'  
            else:
                return '{"status":"error","value":"missing sensor name"}'
        else:
            return '{"status":"error","value":"token authorization failure"}' 
        
    @httpapp.addurl('/get/config/')
    def getSensorConfig(p,m):

        p = auth.decodeUrlToken(p)
        if p:
            return '{"status":"ok","value":%s}' % json.dumps(Sensors, sort_keys=True)
        else:
            return '{"status":"error","value":"token authorization failure"}'         


    ######################################################
    # Main sensor loop
    ######################################################
    while(True):
        logger.info("Sensosrs polling")
        t = time.time()
        for key in Sensors:
            group=Sensors[key]
            if group['Status'] == 'On':
                if 'Delay' in Sensors[key].keys() and Sensors[key]['Timestamp'] != "NA":
                    if t-Sensors[key]['Timestamp'] > Sensors[key]['Delay']:
                        # Delayed group
                        Sensors[key]['Timestamp'] = t
                        if key in Handlers.keys():
                            if Handlers[key] is not None:
                                tr = threading.Thread(target=Handlers[key],args=(group,))
                                tr.start()
                else:
                    # Non delayed group
                    Sensors[key]['Timestamp'] = t
                    if key in Handlers.keys():
                        if Handlers[key] is not None:
                            tr = threading.Thread(target=Handlers[key],args=(group,))
                            tr.start()
            
        time.sleep(float(config['SamplingPeriod']))
