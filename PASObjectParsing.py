#!/usr/bin/python
# -*- coding: utf-8 -*-

from print_debug import *
from PASParsingException import *

DEBUG_FLAG_PADDING = 1
DEBUG_FLAG_RANGES = 2 
DEBUG_DATA_READING = 4

set_debug_flags(0)

class PASParsedTypeInObject:
	"""Class that represents a type stored inside an object: 
	it keeps the indexes where the data is stored inside the object and provides tools the read and write the data"""
	def __init__(self):
		self.objectName = ""
		self.nameOfField = ""
		self.typeName = ""
		self.arraySize = 0
		self.size = 0

	def __getitem__(self, index):
		dataRange = (0,0)
		if self.arraySize > 1:
			dataRange = self.range[index]
		elif index > 0:
			raise IndexError("Trying to read data {0} of type {1} but this is not an array in object {3} name of field {4}"
				.format(index, self.typeName, self.objectName, self.nameOfField))
		else:
			dataRange = self.range
		return dataRange

	def setIndex(self, objectName, nameOfField, typeName, start_pos, size, arraySize):
		self.objectName = objectName
		self.nameOfField = nameOfField
		self.typeName = typeName
		self.arraySize = arraySize
		self.size = size
		if arraySize == 1:
			print_debug("adding index {0} {1} {2}".format(typeName, start_pos, start_pos + size), DEBUG_FLAG_RANGES)
			self.range = (start_pos, start_pos + size - 1)
		else:
			print_debug("adding array {0}".format(typeName), DEBUG_FLAG_RANGES)
			indexes = []
			for i in range(0, arraySize):
				indexes.append( (start_pos, start_pos + size - 1) )
				start_pos += size
			self.range = indexes


class PASParsedObject:
	"""This class is a container for PASParsedTypeInObject objects, it constructs them and store them"""

	def __init__(self, objectName):
		self.indexes = [] #list of PASParsedTypeInObject
		self.spectrum = ""
		self.objectName = objectName

	def writeFormatedData(self, formatedData):
		"""transforms the formated data "formatedData" back into raw string """
		dataString = ""
		cursor = 0
		for index in self.indexes:
			if index.arraySize == 1:
				padding = index.range[0] - cursor
				zeroPadding = "{0:"+"<0{0}s".format(padding*2)+"}"
				if padding > 0:
					dataString += zeroPadding.format("") + " "
				dataString += formatedData[index.nameOfField] + " "
				cursor = index.range[1] + 1
			else:
				padding = index.range[0][0] - cursor
				zeroPadding = "{0:"+"<0{0}s".format(padding*2)+"}"
				if padding > 0:
					dataString += zeroPadding.format("") + " "
				for i in range(0, index.arraySize):
					dataString += formatedData[index.nameOfField][i] + " "
				cursor = index.range[index.arraySize - 1][1] + 1

		if dataString.endswith(' '):
			dataString = dataString[:-1]
		return dataString

	def modifyData(self, data, fieldName, newValue, indexInArray=0):
		"""modifies the field "fieldName" in "data" and gives it the value "newValue" """
		formatedData = self.readData(data)
		if fieldName not in formatedData:
			raise KeyError("Cannot modify field {0} in object {1}: it does not exist".format(fieldName, self.objectName))
		else:
			if len(newValue) % 2 != 0:
				newValue = "0" + newValue
			
			fieldValue = self.at(fieldName)
			lengthOfField = fieldValue.size*2 #two characters for each byte
			if len(newValue) > lengthOfField:
				raise PASParsingException("Value {0} cannot fit in a data field of length {1}".format(newValue, lengthOfField))

			zPad = "{0:"+"<0{0}s".format(lengthOfField)+"}"
			newValue = zPad.format(newValue)
			if fieldValue.arraySize == 1:
				formatedData[fieldName] = newValue
			else: #data field is an array
				formatedData[fieldName][indexInArray] = newValue
		return self.writeFormatedData(formatedData)

	def readData(self, data):		
		"""
		Extracts the value of each field in the bit stream given in "data"
		Exemple object with start_index 0x30092
		Object: 30092
		sub0					: Type: type_0001 at position 0 to 0 size 1
		u8IndexBoard			: Type: type_0001 at position 1 to 1 size 1
		u16DDSCrc				: Type: type_0115 at position 2 to 3 size 2
		xFirstDeviceConfigRIDX	: Type: type_0176 at position 4 to 5 size 2
		u16DeviceTotal			: Type: type_0003 at position 6 to 7 size 2
		eBackupPower			: Type: type_0154 at position 8 to 8 size 1
		xBatteryConfig			: Type: type_0229 at position 10 to 19 size 10
		u16DurationCmd			: Type: type_0003 at position 20 to 21 size 2
		spectrum : 	AA BB CCCC DDDD EEEE FF 00 GGGGGGGGGGGGGGGGGGGG HHHH
		data 	 :	07 01 5B6C 0000 0000 00 00 00000000000000000001 0000

		This function returns a dict object as follows:
		{'sub0' : 07,'u8IndexBoard' : 01, etc...}
		"""
		print_debug("Reading object {0} with data {1}".format(self.objectName, data), DEBUG_DATA_READING)
		formatedData = {}
		data = data.replace(' ','')
		for index in self.indexes:
			if index.arraySize == 1:
				print_debug("{0}\t\t = {1}".format(index.nameOfField, data[2*index.range[0]:2*(index.range[1]+1)]), DEBUG_DATA_READING)
				formatedData[index.nameOfField] = data[2*index.range[0]:2*(index.range[1]+1)]
				#we could convert into integer here, but we can leave it to the "display module"
			else:
				arrayContent = []
				for i in range(0, index.arraySize):
					arrayContent.append(data[2*index.range[i][0]:2*(index.range[i][1]+1)])
					print_debug("{0}[{1}]\t\t = {2}".format(index.nameOfField, i, arrayContent[i]), DEBUG_DATA_READING)
				formatedData[index.nameOfField] = arrayContent
		return formatedData

	def __repr__(self):
		"""
		Displays a description of the object parsed in this class
		Exemple object with start_index 0x30092
		Object: 30092
		sub0					: Type: type_0001 at position 0 to 0 size 1
		u8IndexBoard			: Type: type_0001 at position 1 to 1 size 1
		u16DDSCrc				: Type: type_0115 at position 2 to 3 size 2
		xFirstDeviceConfigRIDX	: Type: type_0176 at position 4 to 5 size 2
		u16DeviceTotal			: Type: type_0003 at position 6 to 7 size 2
		eBackupPower			: Type: type_0154 at position 8 to 8 size 1
		xBatteryConfig			: Type: type_0229 at position 10 to 19 size 10
		u16DurationCmd			: Type: type_0003 at position 20 to 21 size 2
		spectrum : 	AA BB CCCC DDDD EEEE FF 00 GGGGGGGGGGGGGGGGGGGG HHHH
		data 	 :	07 01 5B6C 0000 0000 00 00 00000000000000000001 0000
		"""
		description = "Object: {0}\n".format(self.objectName)
		for index in self.indexes:
			if index.arraySize == 1:
				description += "{0}\t\t: Type: {1} at position {2} to {3} size {4}\n"\
				.format(index.nameOfField, index.typeName, index.range[0], index.range[1], index.size)
			else:
				description += "{0}\t\t: Array {1} elements of type {2} from {3} to {4} each element has a size: {5}\n"\
				.format(index.nameOfField, index.arraySize, index.typeName, index.range[0][0], index.range[index.arraySize - 1][1], 
					index.size)
		return description


	def at(self, nameOfField):
		dataField = PASParsedTypeInObject()
		for index in self.indexes:
			if index.nameOfField == nameOfField:
				dataField = index
				break
		return dataField

	def __getitem__(self, index):
		return self.indexes[index]

	def addIndex(self, nameOfField, typeName, start_pos, size, arraySize):
		""" adds a field in this parsed object """
		parsedType = PASParsedTypeInObject()
		parsedType.setIndex(self.objectName, nameOfField, typeName, start_pos, size, arraySize)
		self.indexes.append(parsedType)
    
