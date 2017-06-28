#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Common.print_debug import *


class XMLParsedTypeInObject(object):
    """Class that represents a type stored inside an object:
    it keeps the indexes where the data is stored inside the object and provides tools the read and write the data"""
    def __init__(self):
        self.startIndex = ""
        self.nameOfField = ""
        self.arraySize = 0

    @property
    def typeName(self):
        return self.pasType.typeName


    @property
    def enumFields(self):
        return self.pasType.enumFields

    @property
    def size(self):
        return self.pasType.size

    @property
    def cat(self):
        return self.pasType.cat

    def setInfos(self, startIndex, nameOfField, start_pos, arraySize, pasType):
        self.startIndex = startIndex
        self.nameOfField = nameOfField
        self.arraySize = arraySize
        self.pasType = pasType
        if arraySize == 1:
            print_debug("adding index {0} {1} {2}".format(pasType.typeName, start_pos, start_pos + pasType.size), DEBUG_FLAG_RANGES)
            self.range_ = (start_pos, start_pos + pasType.size - 1)
        else:
            print_debug("adding array {0}".format(pasType.typeName), DEBUG_FLAG_RANGES)
            indexes = []
            for i in range(0, arraySize):
                indexes.append( (start_pos, start_pos + pasType.size - 1) )
                start_pos += pasType.size
            self.range_ = indexes
