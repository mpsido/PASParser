#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import ConfigParser
from print_debug import *

ENUM_DEBUG_OPT_PARSING = 1

set_debug_flags(0)


class PASDDSFileReadingException(Exception):
    """Exception levée dans un certain contexteâ€¦ qui reste Ã  dÃ©finir"""
    def __init__(self, message):
        """On se contente de stocker le message d'erreur"""
        self.message = message
    def __str__(self):
        """On renvoie le message"""
        return self.message

class PASINIParser(ConfigParser.RawConfigParser):
    def __init__(self):
        ConfigParser.RawConfigParser.__init__(self)
        self.optionxform = str
        self.data =""
        self.objectId = ""

    def parse(self,  ELITE, start_index):
        self.objectId = start_index
        self.fileName = ELITE+"/"+start_index
        self.read(self.fileName)

    def getData(self):
        self.data = self.get('PAS_OD_WRITE', 'DATA')
        return self.data

    def setData(self, newValue):
        data = newValue
        self.set('PAS_OD_WRITE', 'DATA', data)

    def write(self):
        with open(self.fileName, 'wb') as configFile:
            ConfigParser.RawConfigParser.write(self, configFile)

class INIBlock:
    def __init__(self):
        self.name = ""
        self.textContent = ""
        self.iniOptions = {}

class PASDDSParser:
    def __init__(self):
        self.filePath = ""
        self.fileName = ""
        self.fileTextContent = ""
        self.iniBlockNames = []
        self.iniBlockTexts = []
        self.iniBlocks = []



    def open(self, filePath):
        if os.path.isfile(filePath) == False:
            raise PASDDSFileReadingException("{0} is not a valid file path".format(filePath))

        fileName = re.split(r'[/\\]', filePath)[-1]
        if re.match(r'^([0-9]|[a-f])+$', fileName, flags=re.I) is None:
            raise PASDDSFileReadingException("Apparently file {0} is not a dds object file".format(filePath))

        self.filePath = filePath
        self.fileName = fileName

        file = open(filePath, 'r')
        self.fileTextContent = file.read()

        file.close()

        self.parseBlocks()

        self.parseValues()

    def parseBlocks(self):
        blocksSeparator = re.compile("^\s*\[.*\](?:\s*)$", flags = re.MULTILINE)
        self.iniBlockNames = blocksSeparator.findall(self.fileTextContent)

        self.iniBlockTexts = [ block.lstrip() for block in  blocksSeparator.split(self.fileTextContent) ]
        if self.iniBlockTexts[0].lstrip() == '':
            self.iniBlockTexts.pop(0)

    def parseValues(self):
        for i,block in enumerate(self.iniBlockTexts):
            print_debug("At {0}, block {1}".format(i, block), ENUM_DEBUG_OPT_PARSING)
            iniBlock = INIBlock()
            iniBlock.name = self.iniBlockNames[i]
            iniBlock.textContent = block
            print_debug("*********** {0} *********".format(iniBlock.name), ENUM_DEBUG_OPT_PARSING)

            optionLine = re.compile("^(\w[\w_]*)=(.*)$", flags = re.MULTILINE)
            for line in block.split("\n"):
                line = line.lstrip().rstrip()
                if line == "":
                    continue
                if optionLine.match(line) is None:
                    raise PASDDSFileReadingException("Line \"{0}\" is not in ini format".format(line))
                else:
                    opt = optionLine.search(line)
                    optName = opt.group(1)
                    optValue = opt.group(2)
                    print_debug("{0} : {1}".format(optName, optValue), ENUM_DEBUG_OPT_PARSING)
                    iniBlock.iniOptions[optName] = optValue

            self.iniBlocks.append(iniBlock)


