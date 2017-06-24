#!/usr/bin/env python
# -*- coding: utf-8 -*-

from print_debug import *


class PASParsedTypeInObject(object):
    """Class that represents a type stored inside an object:
    it keeps the indexes where the data is stored inside the object and provides tools the read and write the data"""
    def __init__(self):
        self.objectIndex = ""
        self.nameOfField = ""
        self.typeName = ""
        self.arraySize = 0
        self.size = 0

    def _get_value(self):
        return self._motherObject.formatedData[self.nameOfField]

    def _set_value(self, value):
        self._motherObject.modifyData(self.nameOfField, value)

    value = property(fget=_get_value, fset=_set_value)

    def __setitem__(self, index, newValue):
        if self.arraySize > 1:
            self._motherObject.modifyData(self.nameOfField, newValue, index)
        else:
            raise IndexError("Trying to set data {0} of type {1} but {4} is not an array in object {3}"
                .format(index, self.typeName, self.objectIndex, self.nameOfField))

    def __getitem__(self, index):
        dataValue = ""
        if self.arraySize > 1:
            dataValue = self._motherObject.formatedData[self.nameOfField][index]
        else:
            raise IndexError("Trying to read data {0} of type {1} but {4} is not an array in object {3}"
                .format(index, self.typeName, self.objectIndex, self.nameOfField))
        return dataValue

    def setInfos(self, objectIndex, nameOfField, typeName, start_pos, size, arraySize, motherObject):
        self.objectIndex = objectIndex
        self.nameOfField = nameOfField
        self.typeName = typeName
        self.arraySize = arraySize
        self.size = size
        self._motherObject = motherObject
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
