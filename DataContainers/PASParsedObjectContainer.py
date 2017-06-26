#!/usr/bin/python
# -*- coding: utf-8 -*-

from Common.print_debug import *
from DataContainers.PASParsedObject import *
from XMLParsing.XMLObjectReader import *

class PASParsedObjectContainer:

    def __init__(self):
        XMLObjectReader.readObjects()
        self._parsedObjects = {}


    def __getitem__(self, objectId):
        objectId = objectId.lower()
        return self._parsedObjects[objectId]

    def removeIndexAt(self, objectIndex):
        if objectIndex in self._parsedObjects:
            print_debug("Removing index element : {0}, startIndex = {1}".format(objectIndex,
                self._parsedObjects[objectIndex].startIndex), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
            self._parsedObjects.pop(objectIndex)
        else:
            raise KeyError("XMLObjectReader.removeIndexAt : ObjectIndex {0} do not exist, cannot remove it".format(objectIndex))

    def addIndexToObject(self, objectIndex, startIndex):
        """
        Creates a new object with index 'objectIndex' using the PASParsedObject whose objectIndex is 'startIndex'
        """
        print_debug("Trying to add index {0} to startIndex {1}".format(objectIndex, startIndex), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
        if startIndex not in self._parsedObjects:
            # parse object and raise an exception if failed to parse
            if self.parseObject(startIndex) == "Non existing object":
                raise PASParsingException("XMLObjectReader.addIndexToObject : start index {0} do not exist".format(startIndex))

        startIndex = XMLObjectReader.getStartIndexFromObjectIndex(startIndex)
        if startIndex == "Invalid index":
            raise PASParsingException("XMLObjectReader.addIndexToObject : start index {0} has got an invalid index !".format(startIndex))


        objectIndex = objectIndex.split(' ')[0]
        count = int(self._parsedObjects[startIndex].objectCount)
        offset = int(objectIndex, 16) - int(self._parsedObjects[startIndex].objectIndex, 16)
        if offset >= count or offset < 0:
            raise PASParsingException("Invalid objectIndex : {0} for object at start_index={1} : count = {2})".format(objectIndex, startIndex, count))

        if objectIndex in self._parsedObjects:
            raise PASParsingException("XMLObjectReader.addIndexToObject : index {0} already exists".format(startIndex))

        XMLObjectReader._PASObjXMLDict[objectIndex] = XMLObjectReader._PASObjXMLDict[startIndex]
        self._parsedObjects[objectIndex] = PASParsedObject(objectIndex)
        XMLObjectReader.xmlParseObject(self._parsedObjects[objectIndex], objectIndex)
        print_debug("Success to add index {0} to startIndex {1}".format(objectIndex, startIndex), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
        return self._parsedObjects[objectIndex]



    def parseObject(self, objectId):
        """
        Parses the object whose "start_index" is objectId
        constructs an arborescence of the types contained in this object
        Uses the data in XMLObjectReader.typeReader to calculate the position of each typed field in the final DATA representing this object

        Also constructs the spectrum of this object
        The "spectrum" is presentation of the way data of this type are presented in the file inside .dds export
        (file whose name is object's start_index)
        Example : aaaa 00 bb
        00 = padding
        [a-z] = data (two successive data are named with a different letter)
        """
        spectrum="Empty Spectrum"
        objectId = objectId.lower()
#        objectId = XMLObjectReader.getStartIndexFromObjectIndex(objectId)
        print_debug("XMLObjectReader.parseObject objectId = {0}".format(objectId), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
        if objectId not in self._parsedObjects:
            if XMLObjectReader.objectExist(objectId):
                self._parsedObjects[objectId] = PASParsedObject(objectId)
                XMLObjectReader.xmlParseObject(self._parsedObjects[objectId], objectId)
                spectrum = self._parsedObjects[objectId].spectrum
            else:
                spectrum = "Non existing object"
        else:
            spectrum = self._parsedObjects[objectId].spectrum
        return spectrum

