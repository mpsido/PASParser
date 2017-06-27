import os,re
from Common.PASParsingException import PASParsingException
from DataContainers.ObjectDataContainer import ObjectDataContainer
from DDS.PASDDSParser import PASDDSParser, PASDDSFileReadingException
from Common.print_debug import *

class DDSReader:
    def __init__(self):
        self.ddsParser = PASDDSParser()
        self.objContainer = ObjectDataContainer()
        self.path = ''
        self._objectIds = []

    def writeData(self):
        self.ddsParser.write()

    def getObject(self, objectId):
        print_debug("DDSReader.getObject {0}".format(objectId))
        return self.objContainer[objectId]

    def getObjectIds(self):
        return self._objectIds

    def readObject(self, objectId):
        print_debug("DDSReader.readObject {0}".format(objectId))
        return self.objContainer[objectId].readData(self.ddsParser.getData(objectId))


    def setDataInObject(self, objectId, data):
        return self.ddsParser.setData(objectId, data)


    def removeObject(self, objectId):
        if objectId not in self.objContainer:
            raise PASParsingException("Cannot remove an unexisting object {0}".format(objectId))

        self.objContainer.removeIndexAt(objectId)
        self.ddsParser.removeDataAtId(objectId)


    def copyObject(self, objectId):
        if objectId not in self.objContainer:
            raise PASParsingException("Cannot copy an unexisting object {0}".format(objectId))

        newId = objectId
        while newId in self.objContainer:
            newObjectId = int(objectId, 16) + 1
            newId = hex(newObjectId)[2:]

        self.ddsParser.appendDataId(objectId, newId)
        newObject = self.objContainer.addIndexToObject(newId, objectId)
        newObject.readData(self.ddsParser.getData(newId))

        return newId


    def updateObject(self, objectId):
        self.setDataInObject(objectId, self.objContainer[objectId].dataString)

    def parse(self, path):
        if os.path.isdir(path) == False:
            raise PASParsingException("DDS.DDSReader : invalid path: {0}".format(path))


        indexes = filter(lambda x: re.match(r'^[0-9A-Fa-f]+$', x), os.listdir(path))

        if len(indexes) == 0:
            raise PASParsingException("DDS.DDSReader : no valid DDS file at path: {0}".format(path))

        self.path = path
        for index in indexes:
            self.ddsParser.parse(path, index)
            for i in range(0, self.ddsParser.getNbObjects(index)):
                id = self.ddsParser.getId(index, i)
                self.objContainer.parseObject( id )
                self._objectIds.append(id)


