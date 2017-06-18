#!/usr/bin/python
# -*- coding: utf-8 -*-

from print_debug import *
from PASParsingException import *
import re

from PASParsedTypeInObject import *

DEBUG_FLAG_PADDING = 1
DEBUG_FLAG_RANGES = 2 
DEBUG_DATA_READING = 4
DEBUG_DATA_CHECK = 8

set_debug_flags(8)


class PASParsedObject:
    """This class is a container for PASParsedTypeInObject objects, it constructs them and store them"""

    def __init__(self, objectName):
        self.fields = [] #list of PASParsedTypeInObject
        self.spectrum = ""
        self.groupName = ""
        self.objectName = objectName
        self.dataString = ""
        self.formatedData = {}

    def isDataValid(self, data):
        if self.spectrum == "" or self.spectrum == "Empty Spectrum":
            print("This Object was not correctly parsed")
            return False
        while data.endswith(' '):
           data = data[:-1]

        if len(data) != len(self.spectrum):
            print_debug("len(data) != len(spectrum)", DEBUG_DATA_CHECK)
            return False

        #Construct a regex to check data
        regexBase = "(([0-9]|[a-fA-F]){2})"
        regexString = ""
        cursor = 0
        for field in self.fields:
            if field.arraySize == 1:
                regexString += PASParsedObject.paddingString(field.range_[0], cursor)
                regexString += regexBase + "{" + "{0}".format(field.size) + "} "
                cursor = field.range_[1] + 1
            else:
                regexString += PASParsedObject.paddingString(field.range_[0][0], cursor)
                for arrayField in field.range_:
                    regexString += regexBase + "{" + "{0}".format(field.size) + "} "
                cursor = field.range_[-1][1] + 1

        while regexString.endswith(' '):
           regexString = regexString[:-1]

#        print(regexString)
        regMatch = re.compile(regexString)

        return regMatch.match(data) is not None

    def paddingString(nextbyteCursor, currentCursor):
        strPadding = ""
        padding = nextbyteCursor - currentCursor
        if padding > 0:
            zeroPadding = "{0:"+"<0{0}s".format(padding*2)+"}"
            strPadding = zeroPadding.format("") + " "
        return strPadding

    paddingString = staticmethod(paddingString)

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
            raise KeyError("Cannot modify field {0} in object {1}: it does not exist".format(fieldName, self.objectName))
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
        print_debug("Reading object {0} with data {1}".format(self.objectName, data), DEBUG_DATA_READING)
        self.formatedData = {}
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
        return self.formatedData

    def __repr__(self):
        """
        Displays a description of the object parsed in this class
        Exemple object with start_index 0x30092
        Object: 30092
        sub0                    : Type: type_0001 at position 0 to 0 size 1
        u8IndexBoard            : Type: type_0001 at position 1 to 1 size 1
        u16DDSCrc                : Type: type_0115 at position 2 to 3 size 2
        xFirstDeviceConfigRIDX    : Type: type_0176 at position 4 to 5 size 2
        u16DeviceTotal            : Type: type_0003 at position 6 to 7 size 2
        eBackupPower            : Type: type_0154 at position 8 to 8 size 1
        xBatteryConfig            : Type: type_0229 at position 10 to 19 size 10
        u16DurationCmd            : Type: type_0003 at position 20 to 21 size 2
        spectrum :     AA BB CCCC DDDD EEEE FF 00 GGGGGGGGGGGGGGGGGGGG HHHH
        data      :    07 01 5B6C 0000 0000 00 00 00000000000000000001 0000
        """
        description = "Object: {0}\n".format(self.objectName)
        for index in self.fields:
            if index.arraySize == 1:
                description += "{0}\t\t: Type: {1} at position {2} to {3} size {4}\n"\
                .format(index.nameOfField, index.typeName, index.range_[0], index.range_[1], index.size)
            else:
                description += "{0}\t\t: Array {1} elements of type {2} from {3} to {4} each element has a size: {5}\n"\
                .format(index.nameOfField, index.arraySize, index.typeName, index.range_[0][0], index.range_[index.arraySize - 1][1],
                    index.size)
        description += "spectrum :     {0}\n".format(self.spectrum)
        if bool(self.formatedData):
            description += "data     :     {0}".format(self.writeFormatedData(self.formatedData))
        return description

    def __setitem__(self, fieldId, newValue):
        return self.modifyData(fieldId, newValue)

    def __getitem__(self, fieldId):
        if type(fieldId) is int:
            dataField = self.fields[fieldId]
        else:
            dataField = [field for field in self.fields if field.nameOfField == fieldId][0]
        return dataField

    def addField(self, nameOfField, typeName, start_pos, size, arraySize):
        """ adds a field in this parsed object """
        parsedType = PASParsedTypeInObject()
        parsedType.setInfos(self.objectName, nameOfField, typeName, start_pos, size, arraySize, self)
        self.fields.append(parsedType)

    def nbFields(self):
        return len(self.fields)
    
