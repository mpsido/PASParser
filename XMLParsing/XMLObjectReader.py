#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The purpose of this module is to construct a class providing tools read DATA field of a given PAS object
This class uses object definitions from OD.xml and OD_types.xml files
"""

import re
from Common.Singleton import *
from PASType import *
from lxml import etree
from XMLParsing.XMLParsedObject import *
from Common.print_debug import *



@Singleton
class XMLObjectReader:
    """
    This class parses OD.xml file to prepare object parsing
    """
    #define class attributes

    def __init__(self):
        self.OD = etree.parse("OD.xml")
        self.typeReader = PASTypeReader()
        self._PASObjXMLDict = {}     #see _readObjects documentation
        self._objectIndexRanges = [] #list of tuple for getStartIndexFromObjectIndex function
        self.PASObjectsString = ""   #see _readObjects documentation
        self._XMLParsedObjects = {}  #dict of XMLParsedObject each call of xmlParseObject function adds an object in it (if not already there)
        self._readObjects()


    def __getitem__(self, startIndex):
        return self._XMLParsedObjects[self.getStartIndexFromObjectIndex(startIndex)]

    def isDataValid(self, objectId, data):
        objectId = self.getStartIndexFromObjectIndex(objectId)
        if objectId not in self._XMLParsedObjects:
            xmlParsedObject = self.xmlParseObject(objectId)
            self._XMLParsedObjects[objectId] = xmlParsedObject
        spectrum = self._XMLParsedObjects[objectId].spectrum
        if spectrum == "" or spectrum == "Empty Spectrum":
            print("This Object was not correctly parsed")
            return False
        while data.endswith(' '):
           data = data[:-1]

        if len(data) != len(spectrum):
            print_debug("len(data) != len(spectrum)", DEBUG_DATA_CHECK)
            return False

        #Construct a regex to check data
        regexBase = "(?:[0-9]|[a-fA-F])"
        regexString = ""
        cursor = 0
        for field in spectrum.split(' '):
            regexString += "(?:" + regexBase + "){" + "{0}".format(len(field)) + "} "

        while regexString.endswith(' '):
           regexString = regexString[:-1]

#        print(regexString)
        regMatch = re.compile(regexString)

        return regMatch.match(data) is not None

    def getCountForObjectNode(self, xmlNode):
        countNode = xmlNode.find('count')
        count = 1
        if countNode is not None and countNode.get('value') != '':
            count = int(countNode.get('value'))
        else:
            elt_int_id = xmlNode.get('start_index')[2:].lower()
            joinGroup = xmlNode.find('joinGroup')
            if joinGroup is None:
                print_debug("Object with id {0} has no objectCount (default value = 1)".format(elt_int_id), DEBUG_DATA_READING)
            else:
                joinGroup = joinGroup.get('gid')
                print_debug("XMLObjectReader._readObjects: StartIndex {0} JoinGroup = {1}".format(elt_int_id, joinGroup), DEBUG_DATA_READING)
                xmlRequest = "//group/objectGroup[@gid='{0}']/count".format(joinGroup)
                print_debug('XMLObjectReader._readObjects: xml request "{0}"'.format(xmlRequest), DEBUG_DATA_READING)
                joinGroupNode = self.OD.xpath(xmlRequest)
                if len(joinGroupNode) > 0:
                    count = joinGroupNode[0].get('value')
                    if int(count) > 0:
                        print_debug("XMLObjectReader._readObjects: xml request found {0}".format(count), DEBUG_DATA_READING)
                        count = int(count)
                    else:
                        print_debug("XMLObjectReader._readObjects: StartIndex {0} has JoinGroup = {1} with count but no value in the count".format(elt_int_id, joinGroup), DEBUG_DATA_READING)
                else:
                    print_debug("XMLObjectReader._readObjects: StartIndex {0} has JoinGroup = {1} but no count on the joinGroup".format(elt_int_id, joinGroup), DEBUG_DATA_READING)
        return count

    def _readObjects(self):
        """
        Reads OD.xml file and "
        initializes _PASObjXMLDict, _objectIndexRanges and PASObjectsString
         - PASObjectsString is a string that lists of all the objects with their 'name' and 'start_index'
            ex: "tDDS_ExtInfoELOA_t 0x70001"
         - _objectIndexRanges is a list of tuple that indicates for each object its address scale
            ex: For start_index=0x20000 (20000, 20800) because count = 2048
        - _PASObjXMLDict is a list of xml node objects we are gonna need later when parsing object content through 'xmlParseObject' function
        """
        elts = ""
        if len(self.PASObjectsString) > 0:
            print_debug("self._readObjects PASObjectsString={0}".format(self.PASObjectsString), DEBUG_DATA_READING)
            elts = self.PASObjectsString
        else:
            for elt in self.OD.findall("group/object"):
                elt_id = elt.get('start_index').lower()
                if re.match(r'0x[0-9A-Fa-f]+', elt_id) is not None:
                    elt_int_id = elt_id[2:]
                    self._PASObjXMLDict[elt_int_id] = elt

                    count = self.getCountForObjectNode(elt)

                    self._objectIndexRanges.append( (int(elt_int_id,16), int(elt_int_id,16) + count))
                    print_debug("Range : {0} to {1}".format(self._objectIndexRanges[-1][0], self._objectIndexRanges[-1][1]), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)

                    elts += elt.get('name') + " " + str(elt_id) + "\n"
                else:
                    print_debug("start_index id={0} is not in format 0x[0-9A-Fa-f]+".format(elt_id+ " "), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
            if elts.endswith('\n'):
                elts = elts[:-1]
            self.PASObjectsString = elts
        return elts

    @staticmethod
    def calculatePadding(position, dataPadding):
        padding = 0
        while (position + padding) % dataPadding != 0:
            padding += 1
        print_debug("Padding {0} at position {1} equals {2}".format(dataPadding, position, padding), DEBUG_FLAG_PADDING)
        return padding

    def _initParsedObjectAtIndex(self, parsedObject, startIndex):
        parsedObject.groupName = self._XMLParsedObjects[startIndex].groupName
        parsedObject.objectName = self._XMLParsedObjects[startIndex].objectName
        parsedObject.startIndex = self._XMLParsedObjects[startIndex].startIndex
        parsedObject.objectCount = self._XMLParsedObjects[startIndex].objectCount
        parsedObject.fields = self._XMLParsedObjects[startIndex].fields
        parsedObject.spectrum = self._XMLParsedObjects[startIndex].spectrum



    def xmlParseObject(self, objectId):
        """
        Parses 'xmlNode' in order to construct a XMLParsedObject using data attributes contained in OD.xml

        Constructs an arborescence of the types contained in this object using the data in self.typeReader
        Calculates the position of each typed field in the final DATA representing this object

        Also constructs the spectrum of this object
        The "spectrum" is presentation of the way data of this type are presented in the file inside .dds export
        (file whose name is object's start_index)
        Example : aaaa 00 bb
        00 = padding
        [a-z] = data (two successive data are named with a different letter)

        Returns the constructed XMLParsedObject object
        """

        startIndex = self.getStartIndexFromObjectIndex(objectId)
        if startIndex in self._XMLParsedObjects:
            parsedObject = self._XMLParsedObjects[startIndex]
        else:
            letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            spectrum = ""
            l = 0
            byteNumber = 0
            xmlNode = self._PASObjXMLDict[startIndex]
            parsedObject = XMLParsedObject()
            parsedObject.groupName = xmlNode.getparent().get('name')
            parsedObject.objectName = xmlNode.get('name')
            parsedObject.startIndex = xmlNode.get('start_index')[2:]
            parsedObject.objectCount = self.getCountForObjectNode(xmlNode)


            print_debug("Created a new parsedObj with id {} and startIndex {} count = {}".format(objectId,
                parsedObject.startIndex, parsedObject.objectCount), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)

            for typeNode in xmlNode.findall('subindex'): #<subindex name="" type="type_0230" version="03150000">
                nameOfField = typeNode.get('name')
                typeName = typeNode.get('type')
                count = int(typeNode.get('count')) #longueur du tableau
                pasType = self.typeReader.PASTypesDict[typeName]
                print_debug("DATA {4}:Type {0} size {1} count {2} padding {3}"
                    .format(typeName, pasType.size, count, pasType.padding, letters[l]), DEBUG_FLAG_PADDING)
                padding = self.calculatePadding(byteNumber, pasType.padding)

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
                    count -= 1
                    spectrum += " "
                    byteNumber += pasType.size
                l += 1
            if spectrum.endswith(' '):
                spectrum = spectrum[:-1]

            parsedObject.spectrum = spectrum

            self._XMLParsedObjects[startIndex] = parsedObject

        return parsedObject



    def spectrum(self, objectId):
        return self[self.getStartIndexFromObjectIndex(objectId)].spectrum


    def objectExist(self, objectId):
        return self.getStartIndexFromObjectIndex(objectId) in self._PASObjXMLDict


    def getStartIndexFromObjectIndex(self, objectIndex):
        try:
            objIdx = int(objectIndex, 16)
        except ValueError:
            return "Invalid index"
        else:
            startIndexList = [idx for idx,end in self._objectIndexRanges if objIdx >= idx and objIdx < end]
            if len(startIndexList) > 1:
                raise PASParsingException("self.getStartIndexFromObjectIndex {0}".format([ hex(index) for index in  startIndexList] ))
            if len(startIndexList) == 0:
                return "Invalid index"
            else:
                return hex(startIndexList[0])[2:]
