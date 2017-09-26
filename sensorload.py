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

import json
import logging
import re
import os

#########################################################################
# Module setup
########################################################################

logger = logging.getLogger("Mydomus")

'''
logger.setLevel(logging.DEBUG)
handler_stream = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(module)-10s %(message)s')
handler_stream.setFormatter(formatter)
logger.addHandler(handler_stream)
'''

def load(config):
    logger.info("Start loading sensors configuration")
    CWD = os.path.dirname(os.path.realpath(__file__))
    files = [f for f in os.listdir(os.path.join(CWD,"sensors")) if re.match(r'.*\.conf', f)]

    mtr = {}
    
    config['Sensors'] = {}
        
    for item in files:
        with open(os.path.join(CWD,"sensors",item)) as data_file:
            try:
                c = json.load(data_file) 
                if 'Sensors' in c.keys():
                    # Check sensor
                    for sensor in c['Sensors'].keys():
                        if sensor in config['Sensors'].keys():
                            logger.error("Duplicate sensor: %s [%s]" % (sensor,item))
                        else:
                            fail = False
                            if 'Status' not in c['Sensors'][sensor].keys():
                                logger.error("Missing Status key: %s [%s]" % (sensor,item))
                                fail = True
                            if 'Type' not in c['Sensors'][sensor].keys():
                                logger.error("Missing Type key: %s [%s]" % (sensor,item))
                                fail = True
                            if 'Metrics' not in c['Sensors'][sensor].keys():
                                logger.error("Missing Metrics key: %s [%s]" % (sensor,item))
                                fail = True
                                
                            # Check metrics
                            local_mtr = {}
                            for metric in c['Sensors'][sensor]['Metrics'].keys():

                                m = c['Sensors'][sensor]['Metrics'][metric]
                                
                                if metric in mtr.keys() or metric in local_mtr.keys():
                                    logger.error("Duplicate metric: %s [%s:%s]" % (metric,sensor,item))
                                else:
                                    logger.info("Found metric: %s" % metric)
                                    mtr
                                    
                                    if 'Class' not in m.keys():
                                        logger.error("Missing Class key: %s [%s:%s]" % (metric,sensor,item))
                                        fail = True

                                    if 'YLabel' not in m.keys():
                                        logger.error("Missing YLabel key: %s [%s:%s]" % (metric,sensor,item))
                                        fail = True                            
                                    
                                    if 'Unit' not in m.keys():
                                        logger.error("Missing Unit key: %s [%s:%s]" % (metric,sensor,item))
                                        fail = True
                                        
                                    # Add local metric
                                    if not fail:
                                        local_mtr[metric] = m


                            if not fail:
                                config['Sensors'][sensor] = c['Sensors'][sensor]
                                for k in local_mtr.keys():
                                    mtr[k] = local_mtr[k]
                        
            except ValueError:  # includes simplejson.decoder.JSONDecodeError
                logger.error('json decoding failure: %s' % item)
    logger.info("Sensors configurations loaded")
    
    return config
