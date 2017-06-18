#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import ConfigParser
from print_debug import *
from PASObjReader import *

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

class INIBlock:
    def __init__(self):
        self.name = ""
        self.textContent = ""
#        self.iniOptions = {} #avoid using dico to keep order
        self.iniOptionsNames = []
        self.iniOptionsValues = []

    def __repr__(self):
        description = ""
#        for option, value in self.iniOptions.items():
        for i in range(0, len(self.iniOptionsNames)):
            option = self.iniOptionsNames[i]
            value = self.iniOptionsValues[i]
            description += option + "=" + value + "\n"
        return description

    def __getitem__(self, optionName):
        return self.iniOptionsValues[self.iniOptionsNames.index(optionName)]


    def __setitem__(self, optionName, newValue):
        self.iniOptionsValues[self.iniOptionsNames.index(optionName)] = newValue

    def addItem(self, optionName, value):
        self.iniOptionsNames.append(optionName)
        self.iniOptionsValues.append(value)

class PASDDSParser:
    def __init__(self):
        self.filePath = ""
        self.fileName = ""
        self.fileTextContent = ""
        self.iniBlockNames = []
        self.iniBlockTexts = []
        self.iniBlocks = []
        self.objReader = PASObjReader()

    def __repr__(self):
        description = ""
        for i,blockName in enumerate(self.iniBlockNames):
            description += blockName + "\n"
            description += str(self.iniBlocks[i]) #+ "\n\n"
        return description


    def parse(self,  path, fileName):
        self.open(path+"/"+fileName)


    def open(self, filePath):
        if os.path.isfile(filePath) == False:
            raise PASDDSFileReadingException("{0} is not a valid file path".format(filePath))

        fileName = re.split(r'[/\\]', filePath)[-1]
        if re.match(r'^([0-9]|[a-f])+$', fileName, flags=re.I) is None:
            raise PASDDSFileReadingException("Apparently file {0} is not a dds object file".format(filePath))

        self.filePath = filePath
        self.fileName = fileName

        with open(filePath, 'r') as file:
            self.fileTextContent = file.read()
            file.close()

        self.parseBlocks()

        self.parseValues()

    def write(self):
        with open(self.filePath, 'w') as file:
            file.write(str(self))
            file.close()

    def sections(self):
        return self.iniBlockNames

    def __getitem__(self,blockName):
        return self.iniBlocks[self.iniBlockNames.index('['+blockName+']')]


    def getData(self):
        return self['PAS_OD_WRITE']['DATA']


    def setData(self, newValue):
        if self.objReader[self.fileName].isDataValid(newValue):
            self['PAS_OD_WRITE']['DATA'] = newValue
        else:
            raise PASDDSFileReadingException("Data is invalid :\nDATA     = {0}\nSPECTRUM = {1}".format(newValue, self.objReader[self.fileName].spectrum))


    def parseBlocks(self):
        blocksSeparator = re.compile("^\s*\[.*\](?:\s*)$", flags = re.MULTILINE)
        self.iniBlockNames = [blockName.lstrip().rstrip() for blockName in blocksSeparator.findall(self.fileTextContent)]

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
                    iniBlock.addItem(optName, optValue)

            self.iniBlocks.append(iniBlock)


