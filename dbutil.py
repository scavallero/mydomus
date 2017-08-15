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

import MySQLdb
import time

class dbutil():
    
    def __init__(self,config,logger):
        self.config = config
        self.logger = logger

    def open(self):
        self.db = MySQLdb.connect(host=self.config["DbHost"],   
                         user=self.config["DbUser"],   
                         passwd=self.config["DbPassword"])
        self.cur = self.db.cursor()

    def use(self):
        sql = """
              USE %s;
              """ % self.config["DbName"]
        self.cur.execute(sql)

    def close(self):
        self.db.commit()
        self.db.close()
        
    def InitDB(self):
        self.logger.info("Init database")
        if "DbHost" not in self.config.keys():
            self.logger.error("Missing DbHost in config file")
            return False
        if "DbUser" not in self.config.keys():
            self.logger.error("Missing DbUser in config file")
            return False
        if "DbPassword" not in self.config.keys():
            self.logger.error("Missing DbPassword in config file")
            return False
        if "DbName" not in self.config.keys():
            self.logger.error("Missing DbName in config file")
            return False

        self.open()
                
        sql = """
              CREATE DATABASE IF NOT EXISTS %s;
              """ % self.config["DbName"]
        self.cur.execute(sql)

        self.use()
        
        sql = """
              CREATE TABLE IF NOT EXISTS sensors (
                 ID Int NOT NULL AUTO_INCREMENT,
                 Name varchar(255),
                 PRIMARY KEY (ID)
              );
              """ 
        self.cur.execute(sql)

        sql = """
              CREATE TABLE IF NOT EXISTS dailyreadings (
                 ID BIGINT NOT NULL AUTO_INCREMENT,
                 SensorID Int,
                 Timestamp Double,
                 Value Double,
                 PRIMARY KEY (ID)
              );
              """ 
        self.cur.execute(sql)

        sql = """
              CREATE TABLE IF NOT EXISTS measures (
                 ID BIGINT NOT NULL AUTO_INCREMENT,
                 SensorID Int,
                 Timestamp Double,
                 Value Double,
                 PRIMARY KEY (ID)
              );
              """
        self.cur.execute(sql)
        
        self.close()
        
        self.logger.info("Init database completed")

        return True

    def AddSensosrName(self,Name):
        self.open()
        self.use()
        
        sql = """
                SELECT COUNT(*) FROM sensors WHERE Name = '%s';
              """ % Name
        self.cur.execute(sql)
        row = self.cur.fetchone()
        if row[0] == 0:
            sql = """
                    INSERT INTO sensors(Name) VALUES ('%s');
                  """ % Name
            self.cur.execute(sql)
        
        self.close()
        
    def AddSensorValue(self,Name,Value,Timestamp):
        self.open()
        self.use()
        
        sql = """
            INSERT INTO dailyreadings (SensorID,Timestamp,Value)
            SELECT ID,%f,%f FROM sensors WHERE sensors.Name = '%s';
              """ % (Timestamp,Value,Name)

        self.cur.execute(sql)
        
        self.close()

    def GetSensorDaily(self,Name):
        self.open()
        self.use()

        yesterday = time.time()-(24*3600)
        
        sql = """
            SELECT Timestamp,Value FROM dailyreadings d
            JOIN sensors s on d.SensorID = s.ID
            WHERE s.Name = '%s' AND d.Timestamp > %f;
              """ % (Name,yesterday)

        output = "["
        self.cur.execute(sql)
        i = True
        for row in self.cur:
            if i:
                i = False
                output = output + "[%f,%f]" % (row[0]*1000.0,row[1])
            else:
                output = output + ",[%f,%f]" % (row[0]*1000.0,row[1])
        output = output + "]"
        
        self.close()
        return output

    def ClearSensorDaily(self):
        self.open()
        self.use()

        h = time.time()-(48*3600)
        
        sql = """
            DELETE FROM dailyreadings d
            WHERE d.Timestamp < %f;
              """ % h

        self.cur.execute(sql)        
        self.close()
        
