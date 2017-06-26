#!/usr/bin/python
# -*- coding: utf-8 -*-

from Common.print_debug import *
from DataContainers.ObjectData import *
from XMLParsing.XMLObjectReader import *


class ObjectDataContainer:
    def __init__(self):
        self._objectXmlReader = XMLObjectReader()
        self._objectDatas = {} #objects of type ObjectData

    def isDataValid(self, objectId, data):
        return self._objectXmlReader.isDataValid(objectId, data)

    def __getitem__(self, objectId):
        objectId = objectId.lower()
        return self._objectDatas[objectId]

    def removeIndexAt(self, objectIndex):
        if objectIndex in self._objectDatas:
            print_debug("Removing index element : {0}, startIndex = {1}".format(objectIndex,
                self._objectXmlReader[objectIndex].startIndex), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
            self._objectDatas.pop(objectIndex)
        else:
            raise KeyError("ObjectDataContainer.removeIndexAt : ObjectIndex {0} do not exist, cannot remove it".format(objectIndex))

    def addIndexToObject(self, objectIndex, startIndex):
        """
        Creates a new object with index 'objectIndex' using the ObjectData whose objectIndex is 'startIndex'
        """
        print_debug("Trying to add index {0} to startIndex {1}".format(objectIndex, startIndex), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
        if startIndex not in self._objectDatas:
            # parse object and raise an exception if failed to parse
            if self.parseObject(startIndex) == "Non existing object":
                raise PASParsingException("ObjectDataContainer.addIndexToObject : start index {0} do not exist".format(startIndex))

        startIndex = self._objectXmlReader.getStartIndexFromObjectIndex(startIndex)
        if startIndex == "Invalid index":
            raise PASParsingException("ObjectDataContainer.addIndexToObject : start index {0} has got an invalid index !".format(startIndex))


        objectIndex = objectIndex.split(' ')[0]
        count = int(self._objectXmlReader[startIndex].objectCount)
        offset = int(objectIndex, 16) - int(self._objectDatas[startIndex].objectIndex, 16)
        if offset >= count or offset < 0:
            raise PASParsingException("Invalid objectIndex : {0} for object at start_index={1} : count = {2})".format(objectIndex, startIndex, count))

        if objectIndex in self._objectDatas:
            raise PASParsingException("ObjectDataContainer.addIndexToObject : index {0} already exists".format(startIndex))

        xmlParsedObject = self._objectXmlReader.xmlParseObject(objectIndex)
        self._objectDatas[objectIndex] = ObjectData(objectIndex, xmlParsedObject)
        print_debug("Success to add index {0} to startIndex {1}".format(objectIndex, startIndex), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
        return self._objectDatas[objectIndex]



    def parseObject(self, objectId):
        """
        Parses the object whose "start_index" is objectId
        constructs an arborescence of the types contained in this object
        Uses the data in self._objectXmlReader.typeReader to calculate the position of each typed field in the final DATA representing this object

        Also constructs the spectrum of this object
        The "spectrum" is presentation of the way data of this type are presented in the file inside .dds export
        (file whose name is object's start_index)
        Example : aaaa 00 bb
        00 = padding
        [a-z] = data (two successive data are named with a different letter)
        """
        spectrum="Empty Spectrum"
        objectId = objectId.lower()
#        objectId = self._objectXmlReader.getStartIndexFromObjectIndex(objectId)
        print_debug("self._objectXmlReader.parseObject objectId = {0}".format(objectId), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
        if objectId not in self._objectDatas:
            if self._objectXmlReader.objectExist(objectId):
                xmlParsedObject = self._objectXmlReader.xmlParseObject(objectId)
                self._objectDatas[objectId] = ObjectData(objectId, xmlParsedObject)
                spectrum = xmlParsedObject.spectrum
            else:
                spectrum = "Non existing object"
        else:
            spectrum = self._objectDatas[objectId].spectrum
        return spectrum

