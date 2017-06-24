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


class PASObjReader:
    """This class parses OD.xml file to prepare object parsing
    Objects are parsed through function "parseObject"
    """
    #define class attributes
    OD = etree.parse("OD.xml")
    typeReader = PASTypeReader()
    _PASObjXMLDict = {}
    _objectIndexRanges = [] #list of tuple for getStartIndexFromObjectIndex function
    PASObjectsString = ""
    spectrums = {}

    @classmethod
    def isDataValid(PASObjReader, objectId, data):
        objectId = PASObjReader.getStartIndexFromObjectIndex(objectId)
        if objectId not in PASObjReader.spectrums:
            PASObjReader._xmlParseObject(objectId, PASObjReader.typeReader, objectId)
        if PASObjReader.spectrums[objectId] == "" or PASObjReader.spectrums[objectId] == "Empty Spectrum":
            print("This Object was not correctly parsed")
            return False
        while data.endswith(' '):
           data = data[:-1]

        if len(data) != len(PASObjReader.spectrums[objectId]):
            print_debug("len(data) != len(spectrum)", DEBUG_DATA_CHECK)
            return False

        #Construct a regex to check data
        regexBase = "(?:[0-9]|[a-fA-F])"
        regexString = ""
        cursor = 0
        for field in PASObjReader.spectrums[objectId].split(' '):
            regexString += "(?:" + regexBase + "){" + "{0}".format(len(field)) + "} "

        while regexString.endswith(' '):
           regexString = regexString[:-1]

#        print(regexString)
        regMatch = re.compile(regexString)

        return regMatch.match(data) is not None

    @classmethod
    def readObjects(PASObjReader):
        elts = ""
        if len(PASObjReader.PASObjectsString) > 0:
            print_debug("PASObjReader.readObjects PASObjectsString={0}".format(PASObjReader.PASObjectsString), DEBUG_DATA_READING)
            elts = PASObjReader.PASObjectsString
        else:
            for elt in PASObjReader.OD.findall("group/object"):
                elt_id = elt.get('start_index').lower()
                if re.match(r'0x[0-9A-Fa-f]+', elt_id) is not None:
                    elt_int_id = elt_id[2:]
                    PASObjReader._PASObjXMLDict[elt_int_id] = elt

                    if elt.find('count') is not None:
                        count = int(elt.find('count').get('value'))
                    #TODO certains objets ont leur count défini dans le 'joinGroup'
                    else:
                        count = 1

                    PASObjReader._objectIndexRanges.append( (int(elt_int_id,16), int(elt_int_id,16) + count))
                    print_debug("Range : {0} to {1}".format(PASObjReader._objectIndexRanges[-1][0], PASObjReader._objectIndexRanges[-1][1], DEBUG_FLAG_ADD_REMOVE_ELEMENTS))

                    elts += elt.get('name') + " " + str(elt_id) + "\n"
                else:
                    print_debug("start_index id={0} is not in format 0x[0-9A-Fa-f]+".format(elt_id+ " "), DEBUG_FLAG_ADD_REMOVE_ELEMENTS)
            if elts.endswith('\n'):
                elts = elts[:-1]
            PASObjReader.PASObjectsString = elts
        return elts

    @staticmethod
    def calculatePadding(position, dataPadding):
        padding = 0
        while (position + padding) % dataPadding != 0:
            padding += 1
        print_debug("Padding {0} at position {1} equals {2}".format(dataPadding, position, padding), DEBUG_FLAG_PADDING)
        return padding

    @classmethod
    def _xmlParseObject(PASObjReader, startIndex, typeReader, objectId):
        """
        Parses 'xmlNode' in order to construct a PASParsedObject object
        The created PASParsedObject object's objectId given will be 'objectId'
        returns the constructed PASParsedObject object
        """
        letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        spectrum = ""
        l = 0
        byteNumber = 0
        xmlNode = PASObjReader._PASObjXMLDict[startIndex]
        parsedObject = PASParsedObject(objectId)
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
                count -= 1
                spectrum += " "
                byteNumber += pasType.size
            l += 1
        if spectrum.endswith(' '):
            spectrum = spectrum[:-1]
        PASObjReader.spectrums[startIndex] = spectrum
        parsedObject.spectrum = spectrum

        return parsedObject


    @classmethod
    def getStartIndexFromObjectIndex(PASObjReader, objectIndex):
        try:
            objIdx = int(objectIndex, 16)
        except ValueError:
            return "Invalid index"
        else:
            startIndexList = [idx for idx,end in PASObjReader._objectIndexRanges if objIdx >= idx and objIdx < end]
            if len(startIndexList) > 1:
                raise PASParsingException("PASObjReader.getStartIndexFromObjectIndex {0}".format([ hex(index) for index in  startIndexList] ))
            if len(startIndexList) == 0:
                return "Invalid index"
            else:
                return hex(startIndexList[0])[2:]
