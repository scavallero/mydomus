# MyDomus

MyDomus is a personal home automation service. 
Currently supported sensors are:

* OregonScientific Bluetooth LE Weather Sensors
* Aurora Photovoltaic Inverter Powerone
* Generic sensors based on agent Arduino
* 123Solar Solar Web logger


## Installing

To install mydomus service follow these steps:


* sudo cp mydomus.sh /etc/init.d
* sudo chmod +x /etc/init.d/mydomus.sh
* sudo update-rc.d mydomus.sh defaults
* sudo cp mydomus /usr/local
* sudo mkdir /var/log/mydomus
* sudo mkdir /etc/mydomus
* sudo cd /etc/mydomus
* sudo ln -s /usr/local/mydomus/mydomus.conf mydomus.conf
* sudo service mydomus start
* sudo cd /var/www/html
* sudo ln -s /usr/local/mydomus/html mydomus
* sudo chown -R www-data mydomus

## Configuration

MyDomus is configured via the mydomus.conf JSON file present in the directory /etc/mydomus. Here you can see an example of 
configuration:

```
{
    "DomoticzURL": "http://192.168.1.104:8080/json.htm",
    "DelayLoop": 150,
    "Sensors": {
        "ArduinoTemperature": {
            "Status": "Off",
            "Type": "UsbTemperature",
            "Device": "/dev/ttyUSB0",
            "IDX": 1
        },
        "SolarPower": {
            "Status": "On",
            "Type": "123Solar",
            "URL": "http://192.168.1.112/123solar/programs",
            "Mode": "Electricity",
            "IDX": 7
        },
        "SolarPowerSM": {
            "Status": "Off",
            "Type": "123Solar",
            "URL": "http://192.168.1.112/123solar/programs",
            "Mode": "SmartMeter",
            "IDX": 17
        }, 
        "WeatherStation": {
            "Status": "On",
            "Type": "oregonble",
            "Device": "hci0",
            "Name": "IDTW218H",
            "Peripherials": {
            	"Computer Room" : {
            	    "Channel": 0,
            	    "Mode": "THB",
            	    "IDX": 22		    
            	},
            	"Living Room" : {
            	    "Channel": 1,
            	    "Mode": "TH",
            	    "IDX": 23		    
            	},
            	"Attic" : {
            	    "Channel": 2,
            	    "Mode": "T",
            	    "IDX": 24		    
            	}         	
            }
        }                  
    }
}
```


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/scavallero/mydomus/tags). 

## Authors

* **Massimiliano Petra** - *Initial work* - 

## Contributor

## License

_Copyright © 2016 Salvatore Cavallero_

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


