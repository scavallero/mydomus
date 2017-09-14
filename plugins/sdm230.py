#!/usr/bin/python

import minimalmodbus
import argparse

DEVICE = '/dev/ttyUSB0'
BAUDRATE = 2400

parser = argparse.ArgumentParser()
parser.add_argument('command',help='command (example: voltage reads voltage')
parser.add_argument("-d", "--device", help="serial device (default '" + DEVICE + "')")
parser.add_argument("-b", "--baudrate", help="baudrate (default '" + str(BAUDRATE) + "')")
args = parser.parse_args()
if args.device:
    DEVICE = args.device
if args.baudrate:
    BAUDRATE = args.baudrate
    
    
rs485 = minimalmodbus.Instrument(DEVICE, 1)
rs485.serial.baudrate = 2400
rs485.serial.bytesize = 8
rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
rs485.serial.stopbits = 1
rs485.serial.timeout = 1
rs485.debug = False
rs485.mode = minimalmodbus.MODE_RTU


Volts = rs485.read_float(0, functioncode=4, numberOfRegisters=2)
Current = rs485.read_float(6, functioncode=4, numberOfRegisters=2)
Active_Power = rs485.read_float(12, functioncode=4, numberOfRegisters=2)
Apparent_Power = rs485.read_float(18, functioncode=4, numberOfRegisters=2)
Reactive_Power = rs485.read_float(24, functioncode=4, numberOfRegisters=2)
Power_Factor = rs485.read_float(30, functioncode=4, numberOfRegisters=2)
Phase_Angle = rs485.read_float(36, functioncode=4, numberOfRegisters=2)
Frequency = rs485.read_float(70, functioncode=4, numberOfRegisters=2)
Import_Active_Energy = rs485.read_float(72, functioncode=4, numberOfRegisters=2) 
Export_Active_Energy = rs485.read_float(74, functioncode=4, numberOfRegisters=2)
Import_Reactive_Energy = rs485.read_float(76, functioncode=4, numberOfRegisters=2)
Export_Reactive_Energy = rs485.read_float(78, functioncode=4, numberOfRegisters=2)
Total_Active_Energy = rs485.read_float(342, functioncode=4, numberOfRegisters=2)
Total_Reactive_Energy = rs485.read_float(344, functioncode=4, numberOfRegisters=2)

if args.command.lower == 'all':
    print 'voltage: {0:.1f} V'.format(Volts)
    print 'current: {0:.1f} A'.format(Current)
    print 'power: {0:.1f} W'.format(Active_Power)
    print 'phase: {0:.1f} Deg'.format(Phase_Angle)
    print 'frequency: {0:.1f} Hz'.format(Frequency)
    print 'energy: {0:.3f} kwh'.format(Import_Active_Energy)

if args.command.lower == 'voltage':
    print 'voltage: {0:.1f} V'.format(Volts)

if args.command.lower == 'current':
    print 'current: {0:.1f} A'.format(Current)

if args.command.lower == 'power':
    print 'power: {0:.1f} W'.format(Active_Power)

if args.command.lower == 'phase':
    print 'phase: {0:.1f} Deg'.format(Phase_Angle)

if args.command.lower == 'frequency':
    print 'frequency: {0:.1f} Hz'.format(Frequency))

if args.command.lower == 'energy':
    print 'energy: {0:.3f} kwh'.format(Import_Active_Energy)
    
    

