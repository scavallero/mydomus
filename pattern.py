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

import re
import logging

#########################################################################
# Module setup
########################################################################

logger = logging.getLogger("Mydomus")

WORD = r"(\b\w+\b)"
GREEDYDATA = r"(.*)"
FLOAT = r"([-+]?\d*\.\d+|\d+)"
INT = r"([-+]?\d+)"
NOTSPACE = r"\S+"
SPACE = r"\s*"    

class parser():
    
    def __init__(self):
        self.pattern = ""
        self.field = ()
        
    def check(self,pattern,string):
        self.pattern = eval(pattern)
        m = re.match(eval(pattern),string)
        if m:
            self.field = m.groups()
        else:
            self.field = ()

        return self.field
        

