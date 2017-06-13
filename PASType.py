#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
The purpose of this module is to construct a class providing tools read DATA field of a given PAS type 
This class uses object definitions from OD_types.xml 
"""

import re
from lxml import etree

# class PASType(object):
class PASType:
	def __init__(self):
		self.name =""
		self.id=0
		self.size=0
		# self._size=0
		self.cat=""
		self.padding=0
		self.spectrum = ""
	def __repr__(self):
		return self.name
	
	# def _set_size(self, typeSize):
	# 	print("set_size")
	# 	self._size = typeSize
	# 	self.spectrum = ""
	# 	for i in range(0, typeSize):
	# 		self.spectrum += "XX"
	# def _get_size(self):
	# 	return self._size
	# size = property(fget=_get_size, fset=_set_size)


class PASTypeReader:
	def __init__(self, xmlFilePath = ""):
		if xmlFilePath == "":
			xmlFilePath = "OD_types.xml"
		self.OD_types = etree.parse(xmlFilePath)
		self.PASTypesDict = {}
		self.readTypes()


	def readTypes(self):
		types = ""
		if (hasattr(self, 'PASTypesString')):
			types = self.PASTypesString
		else:
			for elt in self.OD_types.findall("type"):
				elt_id = elt.get('id')

				#construction d'un objet "PASType"
				Type = PASType()
				Type.id = elt_id
				Type.name = elt.get('name')
				Type.cat = elt.get('cat')
				Type.size = int(elt.get('size'))
				for i in range(0, Type.size):
					Type.spectrum += "XX"
				Type.padding = int(elt.get('padding'))
				Type.xmlNode = elt

				self.PASTypesDict[elt_id] = Type
				types += Type.name + "\n"

			if len(types) > 0:
				types = types[:-1]
			self.PASTypesString = types

		return types