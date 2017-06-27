#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Common.print_debug import *


class XMLParsedTypeInObject(object):
    """Class that represents a type stored inside an object:
    it keeps the indexes where the data is stored inside the object and provides tools the read and write the data"""
    def __init__(self):
        self.startIndex = ""
        self.nameOfField = ""
        self.typeName = ""
        self.arraySize = 0
        self.size = 0


    def setInfos(self, startIndex, nameOfField, typeName, start_pos, size, arraySize):
        self.startIndex = startIndex
        self.nameOfField = nameOfField
        self.typeName = typeName
        self.arraySize = arraySize
        self.size = size
        if arraySize == 1:
            print_debug("adding index {0} {1} {2}".format(typeName, start_pos, start_pos + size), DEBUG_FLAG_RANGES)
            self.range_ = (start_pos, start_pos + size - 1)
        else:
            print_debug("adding array {0}".format(typeName), DEBUG_FLAG_RANGES)
            indexes = []
            for i in range(0, arraySize):
                indexes.append( (start_pos, start_pos + size - 1) )
                start_pos += size
            self.range_ = indexes
