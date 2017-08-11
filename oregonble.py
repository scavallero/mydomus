#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#   oregonble
#   Oregon Scientific BLE Driver
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

import binascii
from bluepy import btle

class NotificationDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        self.data = [None,None]
        
    def handleNotification(self, _cHandle, _data):
        hexdata = binascii.hexlify(_data)
        if _cHandle == 0x0017:
            if hexdata[0] == '8':
                # Type 1
                self.data[1] = binascii.hexlify(_data)
            else:
                # Type 0
                self.data[0] = binascii.hexlify(_data)
    
    def getTHB(self):
        return self.data
    
class Station:
        
    def __init__(self, name,mac):
        self.name = name
        self.mac = mac
        self.connected = False
        self.peripherial = None
        self.T = [0,0,0,0]
        self.H = [0,0,0,0]
        

    # if mac address is available, it connects to device and obtains the peripherial
    def connect(self):
        if self.mac != None and self.connected == False:
            self.peripherial = btle.Peripheral(self.mac, btle.ADDR_TYPE_RANDOM)
            self.peripherial.setDelegate(NotificationDelegate())
            self.connected = True
            
        return self.connected

    def disconnect(self):
        if self.connected:
            self.peripherial.disconnect()
            self.connect = False

    def enableNotification(self):
        if self.connected:
            try:
                # Enable notifications
                self.peripherial.writeCharacteristic(0x000c, "\x02\x00")
                self.peripherial.writeCharacteristic(0x000f, "\x02\x00")
                self.peripherial.writeCharacteristic(0x0012, "\x02\x00")
                self.peripherial.writeCharacteristic(0x0015, "\x01\x00")
                self.peripherial.writeCharacteristic(0x0018, "\x02\x00")
                self.peripherial.writeCharacteristic(0x001b, "\x02\x00")
                self.peripherial.writeCharacteristic(0x001e, "\x02\x00")
                self.peripherial.writeCharacteristic(0x0021, "\x02\x00")
                self.peripherial.writeCharacteristic(0x0032, "\x01\x00")
            except:
                self.peripherial.disconnect()
                self.peripherial = None
                self.connected = False

    def run(self):
        if self.connected:
            # Enable and wait for notifications
            try:
                # Enable notification
                self.enableNotification()
            # Wait for notifications
                while self.peripherial.waitForNotifications(5.0):
                    continue
            except:
                return False
        
            data = self.peripherial.delegate.getTHB()
            if data[0] is not None and data[0] is not None:

                # Temperature
                self.T[0] = int(data[0][4:6] + data[0][2:4],16)
                if self.T[0] >= 0x8000:
                    self.T[0] = ((self.T[0] + 0x8000) & 0xFFFF) - 0x8000
                self.T[1] = int(data[0][8:10] + data[0][6:8],16)
                if self.T[1] >= 0x8000:
                    self.T[1] = ((self.T[1] + 0x8000) & 0xFFFF) - 0x8000
                self.T[2] = int(data[0][12:14] + data[0][10:12],16)
                if self.T[2] >= 0x8000:
                    self.T[2] = ((self.T[2] + 0x8000) & 0xFFFF) - 0x8000                
                self.T[3] = int(data[0][16:18] + data[0][14:16],16)
                if self.T[3] >= 0x8000:
                    self.T[3] = ((self.T[3] + 0x8000) & 0xFFFF) - 0x8000                

                # Humidity
                self.H[0] = int(data[0][18:20],16)
                self.H[1] = int(data[0][20:22],16)
                self.H[2] = int(data[0][22:24],16)
                self.H[3] = int(data[0][24:26],16)

                return True
            else:
                return False
        else:
            return False
            
    # Dele currently stored mac address and scan for a valid device 
    def scan(self, verbose=False):
        self.mac = None
        try:
            # Scanning device list
            scanner = btle.Scanner().withDelegate(btle.DefaultDelegate())
            self.devices = scanner.scan(5.0)
        except btle.BTLEException as err:
            if (verbose):
                print(err)
                print('Scanning failure, did you run with sudo?')
            return None

        for dev in self.devices:
            if self.name == dev.getValueText(9):
                self.mac = dev.addr
            if (verbose):
                print "Device %s %s (%s) RSSI=%d dB" % (dev.getValueText(9), dev.addr, dev.addrType, dev.rssi)

        return self.mac

    def getTemperature(self, channel):
        if channel <= 3:
            return self.T[channel]/10.0
        else:
            return None

    def getHumidity(self, channel):
        if channel <= 3:
            return self.H[channel]
        else:
            return None

if __name__ == '__main__':        
    ws = Station("IDTW218H",None)      
    mac = ws.scan(verbose=True)
    if mac != None:
        print mac
    else:
        print "Device not found"
    ws.connect()
    if ws.run():
        t_indoor=ws.getTemperature(0)
        h_indoor=ws.getHumidity(0)
        t_outdoor=ws.getTemperature(1)
        h_outdoor=ws.getHumidity(1)
        print "Outdoor %.1f C %d%%, Indoor %.1f C %d%%" % (t_outdoor, h_indoor, t_indoor, h_outdoor)
    ws.disconnect()
