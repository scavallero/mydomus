//
//   AgentArduino.ino
//   Arduino agent for domotic service
//   Copyright (C) 2016  Massimiliano Petra (massimiliano.petra@gmail.com)
//   https://github.com/massimilianopetra/mydomus
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.
//

#include <RCSwitch.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// Serial command buffer size
#define INPUT_SIZE 30

// Temperature sensosr DS18B20 definition 
#define ONE_WIRE_BUS 10
#define TEMPERATURE_PRECISION 12
#define FREQUENCY 60

// RCSwitch definition
#define RCTX_PIN 11               // RCSwitch Transmission Pin
#define RCTX_PULSE_LENGTH  310    // RCSwitch Pulse length [msec]
#define RCTX_PROTOCOL 1           // RCSwitch Protocol
#define RCTX_REPETITION 5         // RCSwitch Number of re-transmission


// Setup DS18B20
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
DeviceAddress insideThermometer;

// Globals
RCSwitch mySwitch = RCSwitch();
char input[INPUT_SIZE + 1];
char* command;

// Function to print a device address
void printAddress(DeviceAddress deviceAddress)
{
  for (uint8_t i = 0; i < 8; i++)
  {
    // zero pad the address if necessary
    if (deviceAddress[i] < 16) Serial.print("0");
    Serial.print(deviceAddress[i], HEX);
  }
}

// Function to print the temperature for a device
void printTemperature(DeviceAddress deviceAddress)
{
  float tempC = sensors.getTempC(deviceAddress);
  Serial.print(tempC);
  Serial.println();
}

// Function to print a device's resolution
void printResolution(DeviceAddress deviceAddress)
{
  Serial.print("Resolution: ");
  Serial.print(sensors.getResolution(deviceAddress));
  Serial.println();    
}


void setup() {
  
  Serial.begin(9600);
  
  // RCWitch setup
  mySwitch.enableTransmit(RCTX_PIN); 
  mySwitch.setPulseLength(RCTX_PULSE_LENGTH);  
  mySwitch.setProtocol(RCTX_PROTOCOL);      
  mySwitch.setRepeatTransmit(RCTX_REPETITION); 

  // Start up the DS18B20 library
  sensors.begin();

  
  // Locate devices on the bus
  //Serial.print(sensors.getDeviceCount(), DEC);
  //Serial.println(" Temperature Devices");

  if (!sensors.getAddress(insideThermometer, 0)) Serial.println("LOG|Unable to find address for Device 0"); 

  // show the addresses we found on the bus
  //printAddress(insideThermometer);
  //Serial.println();

  // set the resolution 
  sensors.setResolution(insideThermometer, TEMPERATURE_PRECISION);

}

void loop() {
  
  unsigned long value;
  
  // Read command from serial port
  byte s = Serial.readBytes(input, INPUT_SIZE);
  input[s] = 0;

  if (strncmp(input,"RCTX",4) == 0) {
    command = strtok(input, "|");
    command = strtok(0, "|");
    if (command != 0) {
      value = atol(command);
      Serial.print("ACK|RCTX|");
      Serial.println(value,DEC);
      mySwitch.send(value, 24);
    }
  } else if (strncmp(input,"GETTEMP",7) == 0) {
    sensors.requestTemperatures();
    printTemperature(insideThermometer);
  }
  
  delay(1000);
}
