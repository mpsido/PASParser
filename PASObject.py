#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The purpose of this module is to construct a class providing tools read DATA field of a given PAS object 
This class uses object definitions from OD.xml and OD_types.xml files
"""

import re
from PASType import *
from lxml import etree


class PASParsedObject:
	"""Constructs a tree object/type/data fiels (start,end, number of elements in array if > 0 list of start-end)"""

	def __init__(self):
		self.indexes = {}
		self.spectrum = ""

	def __repr__(self):
		return str(self.indexes)

	def __getitem__(self, name):
		return self.indexes[name]
    
	def setIndex(self, name, start_pos, size, arraySize):
		if arraySize == 1:
			print("adding index", name, start_pos, start_pos + size)
			self.indexes[name] = (start_pos, start_pos + size)
		else:
			print("adding array", name)
			indexes = []
			for i in range(0, arraySize):
				indexes.append( (start_pos, start_pos+size) )
				start_pos += size + 1
			self.indexes[name] = indexes


class PASObjReader:
	def __init__(self):
		self.OD = etree.parse("OD.xml")
		self._PASObjDict = {}
		self._PASObjXMLDict = {}
		self.parsedObjects = {}
		self.readObjects()
	def readObjects(self):
		elts = ""
		if (hasattr(self, 'PASObjectsString')):
			elts = self.PASObjectsString
		else:
			for elt in self.OD.findall("group/object"):
				elt_id = elt.get('start_index')
				if re.match(r'0x[0-9A-Fa-f]+', elt_id) is not None:
				    elt_int_id = elt_id[2:]
				    self._PASObjDict[elt_int_id] = elt.get('name')
				    self._PASObjXMLDict[elt_int_id] = elt
				    elts += self._PASObjDict[elt_int_id] + " " + str(elt_id) + "\n"
				else:
					print ("start_index id={0} is not in format 0x[0-9A-Fa-f]+".format(elt_id+ " "))
			if elts.endswith('\n'):
				elts = elts[:-1]
			self.PASObjectsString = elts
		return elts

	def calculatePadding(position, dataPadding):
		# print("Padding {0} at position {1} equals {2}".format(dataPadding, position, position%dataPadding))
		return position % dataPadding

	calculatePadding = staticmethod(calculatePadding)

	def getDataSpectrum(self, objectId, TypeReader):
		""" 
		Dispay the way that data of this type should be presented in the file inside .dds export whose name is this type id
		Example : aaaa 00 bb 
		00 = padding
		[a-z] = data (two successive data are named with a different letter)
		"""
		spectrum="Empty Spectrum"
		if objectId not in self.parsedObjects:
			if objectId in self._PASObjXMLDict:
				letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
				spectrum = ""
				l = 0
				byteNumber = 0
				parsedObject = PASParsedObject()
				for typeNode in self._PASObjXMLDict[objectId].findall('subindex'): #<subindex name="" type="type_0230" version="03150000">
					typeName = typeNode.get('type')
					count = int(typeNode.get('count')) #longueur du tableau
					pasType = TypeReader._PASTypesDict[typeName]
					# print ("DATA {4}:Type {0} size {1} count {2} padding {3}".format(typeName, pasType.size, count, pasType.padding, letters[l]))
					padding = PASObjReader.calculatePadding(byteNumber, pasType.padding)


					for j in range (0, padding):
						spectrum += "00"
					if (padding > 0):
						byteNumber += padding
						spectrum += " "

					parsedObject.setIndex(typeName, byteNumber, pasType.size, count)

					while count > 0:
						spectrum += pasType.spectrum.replace('X', letters[l])
						# for i in range(0, pasType.size):
						# 	spectrum += letters[l] + letters[l]
						count -= 1
						spectrum += " "

					byteNumber += pasType.size
					l += 1
			if spectrum.endswith(' '):
			    spectrum = spectrum[:-1]
			parsedObject.spectrum = spectrum
			self.parsedObjects[objectId] = parsedObject
			print (parsedObject)
			print spectrum
		else:
			spectrum = self.parsedObjects[objectId].spectrum
		return spectrum
