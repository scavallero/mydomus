#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   MyDomus
#   Home Domotic Service
#   Copyright (c) 2016 Massimiliano Petra (massimiliano.petra@gmail.com)
#   https://github.com/massimilianopetra/mydomus
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

import MySQLdb

def InitDB(config,logger):
    logger.info("Init database")
    if "DbHost" not in config.keys():
        logger.error("Missing DbHost in config file")
        return False
    if "DbUser" not in config.keys():
        logger.error("Missing DbUser in config file")
        return False
    if "DbPassword" not in config.keys():
        logger.error("Missing DbPassword in config file")
        return False
    if "DbName" not in config.keys():
        logger.error("Missing DbName in config file")
        return False
    
    db = MySQLdb.connect(host=config["DbHost"],   
                     user=config["DbUser"],   
                     passwd=config["DbPassword"])
    cur = db.cursor()
    sql = """
          CREATE DATABASE IF NOT EXISTS %s;
          """ % config["DbName"]
    cur.execute(sql)

    sql = """
          USE %s;
          """ % config["DbName"]
    cur.execute(sql)
    
    sql = """
          CREATE TABLE IF NOT EXISTS sensors (
             ID int NOT NULL AUTO_INCREMENT,
             Name varchar(255),
             PRIMARY KEY (ID)
          );
          """ 
    cur.execute(sql)

    sql = """
          CREATE TABLE IF NOT EXISTS dailyreadings (
             ID int NOT NULL AUTO_INCREMENT,
             SensorID Int,
             Timestamp Float,
             Value Float,
             PRIMARY KEY (ID)
          );
          """ 
    cur.execute(sql)
    
    db.commit()
    db.close()
    logger.info("Init database completed")
    

    return

def AddSensosrName(config,logger,Name):
    db = MySQLdb.connect(host=config["DbHost"],   
                     user=config["DbUser"],   
                     passwd=config["DbPassword"])
    cur = db.cursor()

    sql = """
          USE %s;
          """ % config["DbName"]
    cur.execute(sql)
    
    sql = """
            SELECT COUNT(*) FROM sensors WHERE Name = '%s';
          """ % Name
    cur.execute(sql)
    row = cur.fetchone()
    if row[0] == 0:
        sql = """
                INSERT INTO sensors(Name) VALUES ('%s');
              """ % Name
        cur.execute(sql)
    
    db.commit()
    db.close()
    
def AddSensorValue(config,logger,Name,Value,timestamp):
    db = MySQLdb.connect(host=config["DbHost"],   
                     user=config["DbUser"],   
                     passwd=config["DbPassword"])
    cur = db.cursor()
    
    sql = """
          CREATE TABLE IF NOT EXISTS DailyReadings (
             ID int NOT NULL AUTO_INCREMENT,
             SensorID Int,
             Timestamp Float,
             Value Float,
             PRIMARY KEY (ID)
          );
          """
    cur.execute(sql)
    
    db.commit()
    db.close()
