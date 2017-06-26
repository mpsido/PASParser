#!/usr/bin/python
# -*- coding: utf-8 -*-

from XMLParsing.XMLParsedObject import *

from print_debug import *
from PASParsingException import *
import re


class PASParsedObject(XMLParsedObject):
    """Same as XMLParsedObject, but this class also stores data"""

    def __init__(self, objectIndex):
        super(PASParsedObject, self).__init__()
        self.dataString = ""
        self.formatedData = {}
        self.objectIndex = objectIndex

    def writeFormatedData(self, formatedData):
        """transforms the formated data "formatedData" back into raw string """
        self.dataString = ""
        cursor = 0
        for field in self.fields:
            if field.arraySize == 1:
                self.dataString += PASParsedObject.paddingString(field.range_[0], cursor)
                self.dataString += formatedData[field.nameOfField] + " "
                cursor = field.range_[1] + 1
            else:
                self.dataString += PASParsedObject.paddingString(field.range_[0][0], cursor)
                for i in range(0, field.arraySize):
                    self.dataString += formatedData[field.nameOfField][i] + " "
                cursor = field.range_[-1][1] + 1

        if self.dataString.endswith(' '):
            self.dataString = self.dataString[:-1]
        return self.dataString

    def modifyData(self, fieldName, newValue, indexInArray=0):
        """modifies the field "fieldName" in "data" and gives it the value "newValue" """
        if fieldName not in self.formatedData:
            raise KeyError("Cannot modify field {0} in object {1}: it does not exist".format(fieldName, self.objectIndex))
        else:
            newValue = newValue.upper()
            if re.match(r'^([0-9]|[A-F])+$', newValue) is None:
                raise PASParsingException("Value {0} is invalid, it must be an hexadecimal number".format(newValue))
            if len(newValue) % 2 != 0:
                newValue = "0" + newValue

            fieldValue = self.__getitem__(fieldName)
            lengthOfField = fieldValue.size*2 #two characters for each byte
            if len(newValue) > lengthOfField:
                raise PASParsingException("Value {0} cannot fit in a data field of length {1}".format(newValue, lengthOfField))

            zPad = "{0:"+"<0{0}s".format(lengthOfField)+"}"
            newValue = zPad.format(newValue)
            if fieldValue.arraySize == 1:
                self.formatedData[fieldName] = newValue
            else: #data field is an array
                self.formatedData[fieldName][indexInArray] = newValue
            self.dataString = self.writeFormatedData(self.formatedData)
        return self.dataString

    def readData(self, data):
        """
        Extracts the value of each field in the bit stream given in "data"
        Exemple object with start_index 0x30092
        Object: 10000
        sub0             = 1B
        eEquipType               = 01
        u8Number                 = 02
        xBaseAddress             = 0A
        eBoard_slot[0]           = 14
        eBoard_slot[1]           = 0D
        eBoard_slot[2]           = 09
        eBoard_slot[3]           = 00
        eBoard_slot[4]           = 00
        eBoard_slot[5]           = 00
        eBoard_slot[6]           = 00
        eBoard_slot[7]           = 00
        eBoard_slot[8]           = 00
        eBoard_slot[9]           = 00
        eBoard_slot[10]          = 00
        eBoard_slot[11]          = 00
        eBoard_slot[12]          = 00
        eBoard_slot[13]          = 00
        eBoard_slot[14]          = 00
        xEAES_Used               = 00
        eVariant                 = 03
        xSNTPMaster              = 0B01010A
        tSubSlotType[0]          = 010110
        tSubSlotType[1]          = 000000
        tSubSlotType[2]          = 000000
        tSubSlotType[3]          = 000000
        tSubSlotType[4]          = 000000
        tSubSlotType[5]          = 000000

        This function returns a dict object as follows:
        {'sub0' : 07,'u8IndexBoard' : 01, etc...}
        """
        print_debug("Reading object {0} with data {1}".format(self.objectIndex, data), DEBUG_DATA_READING)
        self.formatedData = {}
        self.dataString = ""

        data = data.replace(' ','')
        for field in self.fields:
            if field.arraySize == 1:
                print_debug("{0}\t\t = {1}".format(field.nameOfField, data[2*field.range_[0]:2*(field.range_[1]+1)]), DEBUG_DATA_READING)
                self.formatedData[field.nameOfField] = data[2*field.range_[0]:2*(field.range_[1]+1)]
                #we could convert into integer here, but we can leave it to the "display module"
            else:
                arrayContent = []
                for i in range(0, field.arraySize):
                    arrayContent.append(data[2*field.range_[i][0]:2*(field.range_[i][1]+1)])
                    print_debug("{0}[{1}]\t\t = {2}".format(field.nameOfField, i, arrayContent[i]), DEBUG_DATA_READING)
                self.formatedData[field.nameOfField] = arrayContent
        self.dataString = self.writeFormatedData(self.formatedData)
        return self.formatedData


    
