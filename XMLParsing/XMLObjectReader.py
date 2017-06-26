#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The purpose of this module is to construct a class providing tools read DATA field of a given PAS object 
This class uses object definitions from OD.xml and OD_types.xml files
"""

import re
from PASType import *
from lxml import etree
from XMLParsing.XMLParsedObject import *
from print_debug import *


class XMLObjectReader:
    """This class parses OD.xml file to prepare object parsing
    Objects are parsed through function "parseObject"
    """
    #define class attributes
    OD = etree.parse("OD.xml")
    typeReader = PASTypeReader()
    _PASObjXMLDict = {}     #see readObjects documentation
    _objectIndexRanges = [] #list of tuple for getStartIndexFromObjectIndex function
    PASObjectsString = ""   #see readObjects documentation
    spectrums = {}
    _XMLParsedObjects = {}  #dict of XMLParsedObject each call of xmlParseObject function adds an object in it (if not already there)

    @classmethod
    def isDataValid(XMLObjectReader, objectId, data):
        objectId = XMLObjectReader.getStartIndexFromObjectIndex(objectId)
        if objectId not in XMLObjectReader.spectrums:
            xmlParsedObject = XMLParsedObject()
            XMLObjectReader.xmlParseObject(xmlParsedObject, objectId)
            XMLObjectReader._XMLParsedObjects[objectId] = xmlParsedObject
        if XMLObjectReader.spectrums[objectId] == "" or XMLObjectReader.spectrums[objectId] == "Empty Spectrum":
            print("This Object was not correctly parsed")
            return False
        while data.endswith(' '):
           data = data[:-1]

        if len(data) != len(XMLObjectReader.spectrums[objectId]):
            print_debug("len(data) != len(spectrum)", DEBUG_DATA_CHECK)
            return False

        #Construct a regex to check data
        regexBase = "(?:[0-9]|[a-fA-F])"
        regexString = ""
        cursor = 0
        for field in XMLObjectReader.spectrums[objectId].split(' '):
            regexString += "(?:" + regexBase + "){" + "{0}".format(len(field)) + "} "

        while regexString.endswith(' '):
           regexString = regexString[:-1]

#        print(regexString)
        regMatch = re.compile(regexString)

        return regMatch.match(data) is not None

    @classmethod
    def readObjects(XMLObjectReader):
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
        if len(XMLObjectReader.PASObjectsString) > 0:
            print_debug("XMLObjectReader.readObjects PASObjectsString={0}".format(XMLObjectReader.PASObjectsString), DEBUG_DATA_READING)
            elts = XMLObjectReader.PASObjectsString
        else:
            for elt in XMLObjectReader.OD.findall("group/object"):
                elt_id = elt.get('start_index').lower()
                if re.match(r'0x[0-9A-Fa-f]+', elt_id) is not None:
                    elt_int_id = elt_id[2:]
                    XMLObjectReader._PASObjXMLDict[elt_int_id] = elt

                    if elt.find('count') is not None:
                        count = int(elt.find('count').get('value'))
                    #TODO certains objets ont leur count défini dans le 'joinGroup'
                    else:
                        count = 1

                    XMLObjectReader._objectIndexRanges.append( (int(elt_int_id,16), int(elt_int_id,16) + count))
                    print_debug("Range : {0} to {1}".format(XMLObjectReader._objectIndexRanges[-1][0], XMLObjectReader._objectIndexRanges[-1][1], DEBUG_FLAG_ADD_REMOVE_ELEMENTS))

                    elts += elt.get('name') + " " + str(elt_id) + "\n"
                else:
                    print_debug("start_index id={0} is not in format 0x[0-9A-Fa-f]+".format(elt_id+ " "), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
            if elts.endswith('\n'):
                elts = elts[:-1]
            XMLObjectReader.PASObjectsString = elts
        return elts

    @staticmethod
    def calculatePadding(position, dataPadding):
        padding = 0
        while (position + padding) % dataPadding != 0:
            padding += 1
        print_debug("Padding {0} at position {1} equals {2}".format(dataPadding, position, padding), DEBUG_FLAG_PADDING)
        return padding

    @classmethod
    def _initParsedObjectAtIndex(XMLObjectReader, parsedObject, startIndex):
        parsedObject.groupName = XMLObjectReader._XMLParsedObjects[startIndex].groupName
        parsedObject.objectName = XMLObjectReader._XMLParsedObjects[startIndex].objectName
        parsedObject.startIndex = XMLObjectReader._XMLParsedObjects[startIndex].startIndex
        parsedObject.objectCount = XMLObjectReader._XMLParsedObjects[startIndex].objectCount
        parsedObject.fields = XMLObjectReader._XMLParsedObjects[startIndex].fields
        parsedObject.spectrum = XMLObjectReader._XMLParsedObjects[startIndex].spectrum


    @classmethod
    def xmlParseObject(XMLObjectReader, parsedObject, objectId):
        """
        Parses 'xmlNode' in order to fill the given 'parsedObject' with data attributes contained in OD.xml
        The XMLParsedObject object's objectId given will be set to 'objectId'
        returns the constructed XMLParsedObject object
        """

        startIndex = XMLObjectReader.getStartIndexFromObjectIndex(objectId)
        if startIndex in XMLObjectReader._XMLParsedObjects:
            XMLObjectReader._initParsedObjectAtIndex(parsedObject, startIndex)
        else:
            letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            spectrum = ""
            l = 0
            byteNumber = 0
            xmlNode = XMLObjectReader._PASObjXMLDict[startIndex]
            parsedObject.groupName = xmlNode.getparent().get('name')
            parsedObject.objectName = xmlNode.get('name')
            parsedObject.startIndex = xmlNode.get('start_index')[2:]
            if xmlNode.find('count') is not None:
                parsedObject.objectCount = int(xmlNode.find('count').get('value'))
                #TODO certains objets ont leur count défini dans le 'joinGroup'
            else:
                parsedObject.objectCount = 1

            print_debug("Created a new parsedObj with id {} and startIndex {} count = {}".format(objectId,
                parsedObject.startIndex, parsedObject.objectCount), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)

            for typeNode in xmlNode.findall('subindex'): #<subindex name="" type="type_0230" version="03150000">
                nameOfField = typeNode.get('name')
                typeName = typeNode.get('type')
                count = int(typeNode.get('count')) #longueur du tableau
                pasType = XMLObjectReader.typeReader.PASTypesDict[typeName]
                print_debug("DATA {4}:Type {0} size {1} count {2} padding {3}"
                    .format(typeName, pasType.size, count, pasType.padding, letters[l]), DEBUG_FLAG_PADDING)
                padding = XMLObjectReader.calculatePadding(byteNumber, pasType.padding)

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
            XMLObjectReader.spectrums[startIndex] = spectrum
            parsedObject.spectrum = spectrum



    @classmethod
    def getStartIndexFromObjectIndex(XMLObjectReader, objectIndex):
        try:
            objIdx = int(objectIndex, 16)
        except ValueError:
            return "Invalid index"
        else:
            startIndexList = [idx for idx,end in XMLObjectReader._objectIndexRanges if objIdx >= idx and objIdx < end]
            if len(startIndexList) > 1:
                raise PASParsingException("XMLObjectReader.getStartIndexFromObjectIndex {0}".format([ hex(index) for index in  startIndexList] ))
            if len(startIndexList) == 0:
                return "Invalid index"
            else:
                return hex(startIndexList[0])[2:]
