#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import ConfigParser
from print_debug import *
from PASObjReader import *


class PASDDSFileReadingException(Exception):
    """Exception levée dans un certain contextes qui restent à définir"""
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
        self._isLastBlock = True
        self._isFirstBlock = True


    def setNextBlock(self, iniNextBlock):
        self.nextBlock = iniNextBlock
        if hasattr(iniNextBlock, 'previousBlock'):
            self.previousBlock = iniNextBlock.previousBlock
        iniNextBlock.previousBlock = self
        iniNextBlock._isFirstBlock = False
        self._isLastBlock = False


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
        self._PAS_OD_WRITE_Blocks = []
        self._objectIdsList = []
        self.objReader = PASObjReader()
        self.bFileParsed = False

    def __iter__(self):
        """Initializes iteration, this object iterates iniBlocks"""
        # iterates self.iniBlocks (type INIBlock)
        self.bIterating = True
        self.currentBlock = self.firstBlock
        print_debug("Init: {0}".format(self.currentBlock.name), DEBUG_DDS_OPT_PARSING)
        return self

    def next(self):
        i = 0
        if hasattr(self.currentBlock, "nextBlock"):
            i += 1
            currentBlock = self.currentBlock
            self.currentBlock = self.currentBlock.nextBlock
            print_debug("Next: {0}".format(self.currentBlock.name), DEBUG_DDS_OPT_PARSING)
        elif self.bIterating:
            currentBlock = self.currentBlock
            self.bIterating = False
        else:
            print_debug("StopIteration {0}".format(i), DEBUG_DDS_OPT_PARSING)
            raise StopIteration()
        return currentBlock

    def __repr__(self):
        """Constructs the full file text content"""
        description = ""
        for iniBlock in self:
            description += str(iniBlock)
        return description

    def parse(self, path, fileName):
        if self.bFileParsed == False:# or path != self.filePath:
            print_debug("PASDDSObjectParser.parse Parsing object {0} at {1}".format(fileName, path), DEBUG_DDS_OPT_PARSING)
            self.open(os.sep.join([path,fileName]))
        self.bFileParsed = True


    def open(self, filePath):
        pathInfo = re.split(r'[/\\]', filePath)
        fileName = pathInfo[-1]
        path = os.sep.join(pathInfo[:-1])

        if os.path.isfile(filePath) == False:
            fileName = self.objReader.getStartIndexFromObjectIndex(fileName)
            filePath = os.sep.join([path,fileName])

        if os.path.isfile(filePath) == False:
            raise PASDDSFileReadingException("{0} is not a valid file path".format(filePath))


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


    def getId(self, offset = 0):
        id = hex(int(self._PAS_OD_WRITE_Blocks[offset]['ID'].split(' ')[0], 16))[2:] #ex ID=00020004 0000 -> "20004"
        return id


    def getData(self, offset = 0):
        return self._PAS_OD_WRITE_Blocks[offset]['DATA']

    def getObjectIdList(self):
        return self._objectIdsList

    def nbDataId(self):
        """Returns the number of [PAS_OD_WRITE] blocks in the file """
        return len(self._PAS_OD_WRITE_Blocks)

    def removeDataAtId(self, objectId):
        """Removes the PAS_OD_WRITE block located at position offset
        raises IndexError if offset is invalid """
        if objectId not in self._objectIdsList:
            print_debug("PASDDSObjectParser.removeDataAtId Id {0} is missing, cannot remove it".format(newId), DEBUG_DDS_OPT_PARSING)
        else:
            offset = self._objectIdsList.index(objectId) #raises IndexError if offset is invalid
            blockToRemove = self._PAS_OD_WRITE_Blocks.pop(offset)
            self._objectIdsList.pop(offset)

            blockToRemove.previousBlock.setNextBlock(blockToRemove.nextBlock)
#            if offset > 0 and hasattr(blockToRemove, 'nextBlock'):
#                self._PAS_OD_WRITE_Blocks[offset-1].nextBlock = blockToRemove.nextBlock
            return blockToRemove

    def appendDataId(self, newId):
        """
        Adds a PAS_OD_WRITE block in the file
        Setting the ID of the new created block to 'newId'
        The new block is appended after last PAS_OD_WRITE block
        """
        if newId in self._objectIdsList:
            print_debug("PASDDSObjectParser.appendDataId Id {0} already exists cannot add it again".format(newId), DEBUG_DDS_OPT_PARSING)
        else:
            print_debug("PASDDSParser.appendDataId {0}".format(newId), DEBUG_DDS_OPT_PARSING)
            iniBlock = INIBlock()
            iniBlock.name = "[PAS_OD_WRITE]"
            for optionName, optionValue in self._PAS_OD_WRITE_Blocks[-1].iterate():
                if optionName == "ID":
                    optionValue = "{0:>08} 0000".format(newId)
                iniBlock.addItem(optionName, optionValue)

            if len(self._PAS_OD_WRITE_Blocks) > 0:
#                self._PAS_OD_WRITE_Blocks[-1].nextBlock = iniBlock
                self._PAS_OD_WRITE_Blocks[-1].setNextBlock(iniBlock)
            else:
                self.firstBlockBefore_PAS_OD_WRITE.setNextBlock(iniBlock)
            self._PAS_OD_WRITE_Blocks.append(iniBlock) #TODO test list _PAS_OD_WRITE_Blocks a little bit better in automatic tests
            self._objectIdsList.append(newId)


    def insertDataId(self, newId, offset = 0):
        """Adds a PAS_OD_WRITE block in the file
        Setting the ID of the new created block to 'newId',
        the new block is insered BEFORE the block at 'offset' and its content (exept data) is a copy of the block at 'offset'"""
        if newId in self._objectIdsList:
            print_debug("PASDDSObjectParser.insertDataId Id {0} already exist cannot add it again".format(newId), DEBUG_DDS_OPT_PARSING)
        else:
            iniBlock = INIBlock()
            iniBlock.name = "[PAS_OD_WRITE]"
            for optionName, optionValue in self._PAS_OD_WRITE_Blocks[offset].iterate():
                if optionName == "ID":
                    optionValue = "{0:>08} 0000".format(newId)
                iniBlock.addItem(optionName, optionValue)

#            iniBlock.nextBlock = self._PAS_OD_WRITE_Blocks[offset]
            iniBlock.setNextBlock(self._PAS_OD_WRITE_Blocks[offset])
#            if offset > 0:
#                self._PAS_OD_WRITE_Blocks[offset-1].nextBlock = iniBlock
            self._PAS_OD_WRITE_Blocks.insert(offset, iniBlock)
            self._objectIdsList.insert(offset, newId)

    def setDataAtId(self, objectId, newValue):
        offset = self._objectIdsList.index(objectId)
        self.setData(newValue, offset)

    def setData(self, newValue, offset = 0):
        if self.objReader[self.fileName].isDataValid(newValue):
            self._PAS_OD_WRITE_Blocks[offset]['DATA'] = newValue
        else:
            raise PASDDSFileReadingException("Data is invalid :\nDATA     = {0}\nSPECTRUM = {1}".format(newValue, self.objReader[self.fileName].spectrum))


    def _parseBlocks(self):
        blocksSeparator = re.compile("^\s*\[.*\](?:\s*)$", flags = re.MULTILINE)
        self.iniBlockNames = [blockName.lstrip().rstrip() for blockName in blocksSeparator.findall(self.fileTextContent)]

        self.iniBlockTexts = [ block.lstrip() for block in  blocksSeparator.split(self.fileTextContent) ]
        if self.iniBlockTexts[0].lstrip() == '':
            self.iniBlockTexts.pop(0)

    def _parseValues(self):
        bFirstBlock = True
        for i,block in enumerate(self.iniBlockTexts):
            print_debug("\nAt {0}, block \n{1}".format(i, block), DEBUG_DDS_OPT_PARSING)
            iniBlock = INIBlock()
            iniBlock.name = self.iniBlockNames[i]
            iniBlock.textContent = block
            print_debug("*********** {0} *********".format(iniBlock.name), DEBUG_DDS_OPT_PARSING)

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
                    print_debug("OPT {0} : {1}".format(optName, optValue), DEBUG_DDS_OPT_PARSING)
                    iniBlock.addItem(optName, optValue)

            if bFirstBlock:
                iniBlock.previousBlock = iniBlock
                self.firstBlock = iniBlock
                previousBlock = iniBlock
                bFirstBlock = False
            else:
                print_debug("Block: {0}".format(previousBlock.name), DEBUG_DDS_OPT_PARSING)
#                previousBlock.nextBlock = iniBlock
                previousBlock.setNextBlock(iniBlock)
                previousBlock = iniBlock
            self.iniBlocks.append(iniBlock)

#            if iniBlock.name == "[PAS_OD_WRITE]" and hasattr(self, 'firstBlockBefore_PAS_OD_WRITE') == False:
#                self.firstBlockBefore_PAS_OD_WRITE = iniBlock.previousBlock

        print_debug("Block: {0}".format(iniBlock.name), DEBUG_DDS_OPT_PARSING)
        self._PAS_OD_WRITE_Blocks = [block for block in self.iniBlocks if block.name == "[PAS_OD_WRITE]"]

        self._objectIdsList = [ self.getId(i) for i in range(0, self.nbDataId()) ]


class PASDDSParser:
    def __init__(self):
        self.parsedObjects = {}

    def parse(self,  path, objectId):
        print_debug("Parsing object {0} at {1}".format(objectId, path), DEBUG_DDS_OPT_PARSING)
        if objectId in self.parsedObjects:
            self.parsedObjects[objectId].parse(path, objectId)
        else:
            self.parsedObjects[objectId] = PASDDSObjectParser()
            self.parsedObjects[objectId].parse(path, objectId)

            for id in self.parsedObjects[objectId].getObjectIdList():
                self.parsedObjects[id] = self.parsedObjects[objectId]

    def getNbObjects(self, objectId):
        return self.parsedObjects[objectId].nbDataId()

    def getId(self, objectId, offset = 0):
        return self.parsedObjects[objectId].getId(offset)

    def getData(self, objectId, offset = 0):
        return self.parsedObjects[objectId].getData(offset)

    def setData(self, objectId, data):
        return self.parsedObjects[objectId].setDataAtId(objectId, data)

    def write(self):
        for objectId,parsedObject in self.parsedObjects.items():
            parsedObject.write()

    def removeDataAtId(self, objectId):
        self.parsedObjects[objectId].removeDataAtId(objectId)
        self.parsedObjects.pop(objectId)

    def appendDataId(self, startIndex, objectId):
        parsedObject = self.parsedObjects[startIndex]
        parsedObject.appendDataId(objectId)
        self.parsedObjects[objectId] = parsedObject
