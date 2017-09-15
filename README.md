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

    "LogFileName": "/var/log/mydomus/mydomus.log",
    "ServerAddress": "127.0.0.1",
    "ServerPort": 9001,
    "RedirectOutput": "False",
    "DbHost": "127.0.0.1",
    "DbName": "mydomus",
    "DbUser": "mydomus",
    "DbPassword": "mydomus",
    "SamplingPeriod": 30,
    "Sensors": {
        "RandomGroup": {
            "Status": "On",
            "Type": "random",
            "Delay": 50,
            "Devices" : {
                "Random100" : {
                    "RangeMin": 1,
                    "RangeMax": 100
                }
            }
        },
        "WunderGroup": {
            "Status": "On",
            "Type": "wunderground",
            "Delay": 250,
            "ApiKey": "0cedebb6dc0593c2",
            "IDStation": "IPIEMONT26",
            "Devices" : {
                "ExternalTemperature" : {
                    "Type": "temp_c"
                },
                "ExternalHumidity" : {
                    "Type": "relative_humidity"
                },
                "Pressure" : {
                    "Type": "pressure_mb"
                },
                "WindSpeed" : {
                    "Type": "wind_kph"
                },
                "Precipitation" :  {
                    "Type": "precip_1hr"
                }
            }
        },
        "CpuGroup": {
            "Status": "On",
            "Type": "cputemp",
            "Devices" : {
                "CpuTemperature" : 0
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


