#!/usr/bin/python
# -*- coding: utf-8 -*-


import ConfigParser
# import os
# >>> os.chdir('/home/sefi-user/PAS_parser')
# >>> config = ConfigParser.RawConfigParser()
# >>> config.read('ECS-ELITE_1_C-1/74000')
# ['ECS-ELITE_1_C-1/74000']
# >>> config.get('PAS_OD_WRITE', 'DATA')
# '02 00 606D0C006054D052584D50463863580260096400D00764006400F40101010104 00A41011301068ABE000'
# >>> 



class PASINIParser(ConfigParser.RawConfigParser):
    def __init__(self):
        ConfigParser.RawConfigParser.__init__(self)
        self.optionxform = str

    def parse(self,  ELITE, start_index):
        self.fileName = ELITE+"/"+start_index
        self.read(self.fileName)

    def getData(self):
        return self.get('PAS_OD_WRITE', 'DATA')

    def setData(self, newValue):
        return self.set('PAS_OD_WRITE', 'DATA', newValue)

    def write(self):
        with open(self.fileName, 'wb') as configFile:
            ConfigParser.RawConfigParser.write(self, configFile)


