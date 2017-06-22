#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The purpose of this module is to construct a class providing tools read DATA field of a given PAS object 
This class uses object definitions from OD.xml and OD_types.xml files
"""

import re
from PASType import *
from lxml import etree
from PASParsedObject import *
from print_debug import *

DEBUG_FLAG_PADDING = 1
DEBUG_FLAG_RANGES = 2 

# set_debug_flags(0)


class PASObjReader:
    """This class parses OD.xml file to prepare object parsing
    Objects are parsed through function "parseObject"
    """
    def __init__(self, xmlFilePath = ""):
        if xmlFilePath == "":
            xmlFilePath = "OD.xml"
        self.OD = etree.parse(xmlFilePath)
        self._PASObjXMLDict = {}
        self._parsedObjects = {}
        self.typeReader = PASTypeReader()
        self.readObjects()
    def readObjects(self):
        elts = ""
        if (hasattr(self, 'PASObjectsString')):
            elts = self.PASObjectsString
        else:
            for elt in self.OD.findall("group/object"):
                elt_id = elt.get('start_index').lower()
                if re.match(r'0x[0-9A-Fa-f]+', elt_id) is not None:
                    elt_int_id = elt_id[2:]
                    self._PASObjXMLDict[elt_int_id] = elt
                    elts += elt.get('name') + " " + str(elt_id) + "\n"
                else:
                    print ("start_index id={0} is not in format 0x[0-9A-Fa-f]+".format(elt_id+ " "))
            if elts.endswith('\n'):
                elts = elts[:-1]
            self.PASObjectsString = elts
        return elts

    def calculatePadding(position, dataPadding):
        padding = 0
        while (position + padding) % dataPadding != 0:
            padding += 1
        print_debug("Padding {0} at position {1} equals {2}".format(dataPadding, position, padding), DEBUG_FLAG_PADDING)
        return padding

    calculatePadding = staticmethod(calculatePadding)


    def __getitem__(self, objectId):
        objectId = objectId.lower()
        self.parseObject(objectId)
        return self._parsedObjects[objectId]

    def removeIndexAt(self, objectIndex):
        if objectIndex in self._parsedObjects:
            if objectIndex != self._parsedObjects[objectIndex].startIndex: #do not delete startIndex object
                del self._parsedObjects[objectIndex]
        else:
            raise KeyError("PASObjReader.removeIndexAt : ObjectIndex {0} do not exist, cannot remove it".format(objectIndex))

    def addIndexToObject(self, objectIndex, startIndex):
        """
        Creates a new object with index 'objectIndex' using the PASParsedObject whose objectIndex is 'startIndex'
        """
        if startIndex not in self._parsedObjects:
            raise PASParsingException("PASObjReader.addIndexToObject : start index {0} do not exist".format(startIndex))

        count = int(self._parsedObjects[startIndex].objectCount)
        offset = int(objectIndex, 16) - int(self._parsedObjects[startIndex].objectIndex, 16)
        if offset >= count or offset < 0:
            raise PASParsingException("Invalid objectIndex : {0} for object at start_index={1} : count = {2})".format(objectIndex, startIndex, count))

        if objectIndex in self._parsedObjects:
            raise PASParsingException("PASObjReader.addIndexToObject : index {0} already exists".format(startIndex))

        self._parsedObjects[objectIndex] = PASObjReader._xmlParseObject(self._PASObjXMLDict[startIndex], self.typeReader, objectIndex)
        self._parsedObjects[objectIndex].startIndex = startIndex


    def _xmlParseObject(xmlNode, typeReader, objectId):
        """
        Parses 'xmlNode' in order to construct a PASParsedObject object
        The created PASParsedObject object's objectId given will be 'objectId'
        returns the constructed PASParsedObject object
        """
        letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        spectrum = ""
        l = 0
        byteNumber = 0
        parsedObject = PASParsedObject(objectId)
        parsedObject.groupName = xmlNode.getparent().get('name')
        parsedObject.objectName = xmlNode.get('name')
        if xmlNode.find('count') is not None:
            parsedObject.objectCount = int(xmlNode.find('count').get('value'))
        else:
            parsedObject.objectCount = 1
        for typeNode in xmlNode.findall('subindex'): #<subindex name="" type="type_0230" version="03150000">
            nameOfField = typeNode.get('name')
            typeName = typeNode.get('type')
            count = int(typeNode.get('count')) #longueur du tableau
            pasType = typeReader.PASTypesDict[typeName]
            print_debug("DATA {4}:Type {0} size {1} count {2} padding {3}"
                .format(typeName, pasType.size, count, pasType.padding, letters[l]), DEBUG_FLAG_PADDING)
            padding = PASObjReader.calculatePadding(byteNumber, pasType.padding)

            #add padding
            for j in range (0, padding):
                spectrum += "00"
            if (padding > 0):
                byteNumber += padding
                spectrum += " "

            #fill in parsed object with the type we are currently parsing
            parsedObject.addField(nameOfField, typeName, byteNumber, pasType.size, count)

            while count > 0:
                spectrum += pasType.spectrum.replace('X', letters[l])
                # for i in range(0, pasType.size):
                #     spectrum += letters[l] + letters[l]
                count -= 1
                spectrum += " "
                byteNumber += pasType.size
            l += 1
        if spectrum.endswith(' '):
            spectrum = spectrum[:-1]
        parsedObject.spectrum = spectrum

        return parsedObject

    _xmlParseObject = staticmethod(_xmlParseObject)


    def parseObject(self, objectId):
        """
        Parses the object whose "start_index" is objectId
        constructs an arborescence of the types contained in this object
        Uses the data in self.self.typeReader to calculate the position of each typed field in the final DATA representing this object

        Also constructs the spectrum of this object
        The "spectrum" is presentation of the way data of this type are presented in the file inside .dds export
        (file whose name is object's start_index)
        Example : aaaa 00 bb
        00 = padding
        [a-z] = data (two successive data are named with a different letter)
        """
        spectrum="Empty Spectrum"
        objectId = objectId.lower()
        if objectId not in self._parsedObjects:
            if objectId in self._PASObjXMLDict:
                self._parsedObjects[objectId] = PASObjReader._xmlParseObject(self._PASObjXMLDict[objectId], self.typeReader, objectId)
                self._parsedObjects[objectId].startIndex = objectId
                spectrum = self._parsedObjects[objectId].spectrum
            else:
                spectrum = "Non existing object"
        else:
            spectrum = self._parsedObjects[objectId].spectrum
        return spectrum
