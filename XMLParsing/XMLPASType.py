#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
The purpose of this module is to construct a class providing tools read DATA field of a given PAS type 
This class uses object definitions from OD_types.xml 
"""

import re
from lxml import etree

from Common.Singleton import *
from Common.print_debug import *

class XMLPASType:
    def __init__(self):
        self.typeName =""
        self.id=0
        self.size=0
        # self._size=0
        self.cat=""
        self.padding=0
        self.typeSpectrum = ""
        self.display = None

    def __repr__(self):
        return self.typeName

    def parseEnum(self):
        print_debug("parsing Enum {}".format(self.typeName), DEBUG_MMI)
        self.enumFields = []
        for elt in self.xmlNode.findall("enum"):
            self.enumFields.append(elt.get('name'))

@Singleton
class XMLPASTypeReader:


    def __init__(self):
        self.OD_types = etree.parse("OD_types.xml")
        self.XMLPASTypesDict = {}
        self.readTypes()

    def readTypes(self):
        types = ""
        if (hasattr(XMLPASTypeReader, 'XMLPASTypesString')):
            types = self.XMLPASTypesString
        else:
            for elt in self.OD_types.findall("type"):
                elt_id = elt.get('id')

                #construction d'un objet "XMLPASType"
                pasType = XMLPASType()
                pasType.id = elt_id
                pasType.typeName = elt.get('name')
                pasType.cat = elt.get('cat')
                pasType.size = int(elt.get('size'))
                pasType.display = elt.get('display')
                for i in range(0, pasType.size):
                    pasType.typeSpectrum += "XX"
                pasType.padding = int(elt.get('padding'))
                pasType.xmlNode = elt

                if pasType.cat == "enum":
                    pasType.parseEnum()


                self.XMLPASTypesDict[elt_id] = pasType
                types += pasType.typeName + "\n"

            if len(types) > 0:
                types = types[:-1]
            self.XMLPASTypesString = types

        return types

