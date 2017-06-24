#!/usr/bin/python
# -*- coding: utf-8 -*-

from print_debug import *
from PASObjReader import *

class PASParsedObjectContainer:

    def __init__(self):
        PASObjReader.readObjects()
        self._parsedObjects = {}


    def __getitem__(self, objectId):
        objectId = objectId.lower()
#        self.parseObject(objectId)
        return self._parsedObjects[objectId]

    def removeIndexAt(self, objectIndex):
        if objectIndex in self._parsedObjects:
            if objectIndex != self._parsedObjects[objectIndex].startIndex: #do not delete startIndex object
                print_debug("Removing index element : {0}, startIndex = {1}".format(objectIndex,
                    self._parsedObjects[objectIndex].startIndex), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
                self._parsedObjects.pop(objectIndex)
#                PASObjReader._PASObjXMLDict.pop(objectIndex)
            else:
                print_debug("Refuse to remove startIndex element : {0}".format(self._parsedObjects[objectIndex].startIndex), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
        else:
            raise KeyError("PASObjReader.removeIndexAt : ObjectIndex {0} do not exist, cannot remove it".format(objectIndex))

    def addIndexToObject(self, objectIndex, startIndex):
        """
        Creates a new object with index 'objectIndex' using the PASParsedObject whose objectIndex is 'startIndex'
        """
        print_debug("Trying to add index {0} to startIndex {1}".format(objectIndex, startIndex), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
        if startIndex not in self._parsedObjects:
            raise PASParsingException("PASObjReader.addIndexToObject : start index {0} do not exist".format(startIndex))

        startIndex = PASObjReader.getStartIndexFromObjectIndex(startIndex)

        objectIndex = objectIndex.split(' ')[0]
        count = int(self._parsedObjects[startIndex].objectCount)
        offset = int(objectIndex, 16) - int(self._parsedObjects[startIndex].objectIndex, 16)
        if offset >= count or offset < 0:
            raise PASParsingException("Invalid objectIndex : {0} for object at start_index={1} : count = {2})".format(objectIndex, startIndex, count))

        if objectIndex in self._parsedObjects:
            raise PASParsingException("PASObjReader.addIndexToObject : index {0} already exists".format(startIndex))

        PASObjReader._PASObjXMLDict[objectIndex] = PASObjReader._PASObjXMLDict[startIndex]
        self._parsedObjects[objectIndex] = PASObjReader._xmlParseObject(startIndex, PASObjReader.typeReader, objectIndex)
        print_debug("Success to add index {0} to startIndex {1}".format(objectIndex, startIndex), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
        return self._parsedObjects[objectIndex]



    def parseObject(self, objectId):
        """
        Parses the object whose "start_index" is objectId
        constructs an arborescence of the types contained in this object
        Uses the data in PASObjReader.typeReader to calculate the position of each typed field in the final DATA representing this object

        Also constructs the spectrum of this object
        The "spectrum" is presentation of the way data of this type are presented in the file inside .dds export
        (file whose name is object's start_index)
        Example : aaaa 00 bb
        00 = padding
        [a-z] = data (two successive data are named with a different letter)
        """
        spectrum="Empty Spectrum"
        objectId = objectId.lower()
#        objectId = PASObjReader.getStartIndexFromObjectIndex(objectId)
        print_debug("PASObjReader.parseObject objectId = {0}".format(objectId), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
        if objectId not in self._parsedObjects:
            if PASObjReader.getStartIndexFromObjectIndex(objectId) in PASObjReader._PASObjXMLDict:
                self._parsedObjects[objectId] = PASObjReader._xmlParseObject(objectId, PASObjReader.typeReader, objectId)
                spectrum = self._parsedObjects[objectId].spectrum
            else:
                spectrum = "Non existing object"
        else:
            spectrum = self._parsedObjects[objectId].spectrum
        return spectrum

