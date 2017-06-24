#!/usr/bin/env python
# -*- coding: utf-8 -*-

from print_debug import *

ENUM_TYPE_NODE_ROOT = 0
ENUM_TYPE_NODE_OBJECT = 1
ENUM_TYPE_NODE_TYPE_IN_OBJECT = 2
ENUM_TYPE_NODE_ARRAY_ITEM_IN_OBJECT = 3

class PASObjectNode(object):
    def __init__(self, id, rangeOrObjectName, size, nb_elements, pasTypeOrObject, parent=None):
        self.id = id
        self.rangeOrObjectName = rangeOrObjectName
        self.size = size
        self.nb_elements = nb_elements
        self.pasTypeOrObject = pasTypeOrObject

        if parent == None:
            self.typeOfNode = ENUM_TYPE_NODE_ROOT
        else:
            self.typeOfNode = parent.typeOfNode + 1

        self.parent = parent
        self.children = []

        self.setParent(parent)

        self.nodeUpdated = False

    def getStartIndex(self):
        return self.pasTypeOrObject.startIndex

    def setParent(self, parent):
        if parent != None:
            self.parent = parent
            self.parent.appendChild(self)
        else:
            self.parent = None

    def appendChild(self, child):
        self.children.append(child)

    def childAtRow(self, row):
        if row > len(self.children):
            print_debug("PASObjectNode.childAtRow : Element: {0} Row: {1} is out of range. Nb Elements: {2}".format(self.id, row, len(self.children)), DEBUG_MMI)
            return self
        return self.children[row]

    def rowOfChild(self, child):
        for i, item in enumerate(self.children):
            if item == child:
                return i
        return -1

    def removeChild(self, row):
        value = self.children[row]
        self.children.remove(value)

        return True

    def __len__(self):
        return len(self.children)
