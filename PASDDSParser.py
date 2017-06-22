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
        """Constructs the INI block as a text"""
        description = self.name + "\n"
        for option,value in self.iterate():
            description += option + "=" + value + "\n"
        return description

    def __getitem__(self, optionName):
        return self.iniOptionsValues[self.iniOptionsNames.index(optionName)]


    def __setitem__(self, optionName, newValue):
        self.iniOptionsValues[self.iniOptionsNames.index(optionName)] = newValue

    def addItem(self, optionName, value):
        assert len(optionName) > 0
        self.iniOptionsNames.append(optionName)
        self.iniOptionsValues.append(value)

    def iterate(self):
        for i in range(0, len(self.iniOptionsNames)):
            yield self.iniOptionsNames[i], self.iniOptionsValues[i]


class PASDDSObjectParser:
    def __init__(self):
        self.filePath = ""
        self.fileName = ""
        self.fileTextContent = ""
        self.iniBlockNames = []
        self.iniBlockTexts = []
        self.iniBlocks = []
        self.PAS_OD_WRITE_Blocks = []
        self.objReader = PASObjReader()

    def __iter__(self):
        """Initializes iteration, this object iterates iniBlocks"""
        # iterates self.iniBlocks (type INIBlock)
        self.bIterating = True
        self.currentBlock = self.firstBlock
        print_debug("Init: {0}".format(self.currentBlock.name), ENUM_DEBUG_OPT_PARSING)
        return self

    def next(self):
        i = 0
        if hasattr(self.currentBlock, "nextBlock"):
            i += 1
            currentBlock = self.currentBlock
            self.currentBlock = self.currentBlock.nextBlock
            print_debug("Next: {0}".format(self.currentBlock.name), ENUM_DEBUG_OPT_PARSING)
        elif self.bIterating:
            currentBlock = self.currentBlock
            self.bIterating = False
        else:
            print_debug("StopIteration {0}".format(i), ENUM_DEBUG_OPT_PARSING)
            raise StopIteration()
        return currentBlock

    def __repr__(self):
        """Constructs the full file text content"""
        description = ""
        for iniBlock in self:
            description += str(iniBlock)
        return description

#        description = ""
#        for i,blockName in enumerate(self.iniBlockNames):
#            description += blockName + "\n"
#            description += str(self.iniBlocks[i]) #+ "\n\n"
#        return description


    def parse(self,  path, fileName):
        self.open(path+"/"+fileName)


    def open(self, filePath):
        if os.path.isfile(filePath) == False:
            raise PASDDSFileReadingException("{0} is not a valid file path".format(filePath))

        fileName = re.split(r'[/\\]', filePath)[-1]
        if re.match(r'^([0-9]|[a-f])+$', fileName, flags=re.I) is None:
            raise PASDDSFileReadingException("Apparently file {0} is not a dds object file".format(filePath))

        #reset existing data
        self.__init__()

        self.filePath = filePath
        self.fileName = fileName

        with open(filePath, 'r') as file:
            self.fileTextContent = file.read()
            file.close()

        self._parseBlocks()

        self._parseValues()

    def write(self):
        with open(self.filePath, 'w') as file:
            file.write(str(self))
            file.close()

    def sections(self):
        """Returns the names of the sections in the parsed file in a string list.
        Example: [[SECTION_NAME],[SECOND_SECTION]] """
        return self.iniBlockNames

    def __getitem__(self,blockName):
        return self.iniBlocks[self.iniBlockNames.index('['+blockName+']')]


    def getData(self, offset = 0):
        return self.PAS_OD_WRITE_Blocks[offset]['DATA']

    def nbDataId(self):
        """Returns the number of [PAS_OD_WRITE] blocks in the file """
        return len(self.PAS_OD_WRITE_Blocks)

    def removeDataId(self, offset):
        """Removes the PAS_OD_WRITE block located at position offset
        raises IndexError if offset is invalid """
        blockToRemove =  self.PAS_OD_WRITE_Blocks.pop(offset) #raises IndexError if offset is invalid
        if offset > 0 and hasattr(blockToRemove, 'nextBlock'):
            self.PAS_OD_WRITE_Blocks[offset-1].nextBlock = blockToRemove.nextBlock
        return blockToRemove



    def insertDataId(self, newValue, offset = 0):
        """Adds a PAS_OD_WRITE block in the file
        Setting the data value of the new created block to 'newValue',
        the new block is insered BEFORE the block at 'offset' and its content (exept data) is a copy of the block at 'offset'"""
        iniBlock = INIBlock()
        iniBlock.name = "[PAS_OD_WRITE]"
        for optionName, optionValue in self.PAS_OD_WRITE_Blocks[offset].iterate():
            if optionName == "DATA":
                optionValue = newValue
            iniBlock.addItem(optionName, optionValue)

        iniBlock.nextBlock = self.PAS_OD_WRITE_Blocks[offset]
        if offset > 0:
            self.PAS_OD_WRITE_Blocks[offset-1].nextBlock = iniBlock
        self.PAS_OD_WRITE_Blocks.insert(offset, iniBlock)


    def setData(self, newValue, offset = 0):
        if self.objReader[self.fileName].isDataValid(newValue):
            self.PAS_OD_WRITE_Blocks[offset]['DATA'] = newValue
        else:
            raise PASDDSFileReadingException("Data is invalid :\nDATA     = {0}\nSPECTRUM = {1}".format(newValue, self.objReader[self.fileName].spectrum))


    def _parseBlocks(self):
        blocksSeparator = re.compile("^\s*\[.*\](?:\s*)$", flags = re.MULTILINE)
        self.iniBlockNames = [blockName.lstrip().rstrip() for blockName in blocksSeparator.findall(self.fileTextContent)]

        self.iniBlockTexts = [ block.lstrip() for block in  blocksSeparator.split(self.fileTextContent) ]
        if self.iniBlockTexts[0].lstrip() == '':
            self.iniBlockTexts.pop(0)

    def _parseValues(self):
        firstBlock = True
        for i,block in enumerate(self.iniBlockTexts):
            print_debug("\nAt {0}, block \n{1}".format(i, block), ENUM_DEBUG_OPT_PARSING)
            iniBlock = INIBlock()
            iniBlock.name = self.iniBlockNames[i]
            iniBlock.textContent = block
            print_debug("*********** {0} *********".format(iniBlock.name), ENUM_DEBUG_OPT_PARSING)

            optionLine = re.compile("^(\w[\w_]*)=(.*)$", flags = re.MULTILINE)
            for line in block.split("\n"):
                line = line.lstrip().rstrip()
                if line.rstrip().lstrip() == "":
                    continue
                if optionLine.match(line) is None:
                    raise PASDDSFileReadingException("Line \"{0}\" is not in ini format".format(line))
                else:
                    opt = optionLine.search(line)
                    optName = opt.group(1)
                    optValue = opt.group(2)
                    print_debug("OPT {0} : {1}".format(optName, optValue), ENUM_DEBUG_OPT_PARSING)
                    iniBlock.addItem(optName, optValue)

            if firstBlock:
                self.firstBlock = iniBlock
                previousBlock = iniBlock
                firstBlock = False
            else:
                print_debug("Block: {0}".format(previousBlock.name), ENUM_DEBUG_OPT_PARSING)
                previousBlock.nextBlock = iniBlock
                previousBlock = iniBlock
            self.iniBlocks.append(iniBlock)

        print_debug("Block: {0}".format(iniBlock.name), ENUM_DEBUG_OPT_PARSING)
        self.PAS_OD_WRITE_Blocks = [block for block in self.iniBlocks if block.name == "[PAS_OD_WRITE]"]


class PASDDSParser:
    def __init__(self):
        self.parsedObjects = {}

    def parse(self,  path, objectId):
        if objectId in self.parsedObjects:
            self.parsedObjects[objectId].parse(path, objectId)
        else:
            self.parsedObjects[objectId] = PASDDSObjectParser()
            self.parsedObjects[objectId].parse(path, objectId)

    def getData(self, objectId, offset = 0):
        return self.parsedObjects[objectId].getData(offset)

    def setData(self, objectId, data):
        return self.parsedObjects[objectId].setData(data)

    def write(self):
        for objectId,parsedObject in self.parsedObjects.items():
            parsedObject.write()
