#!/usr/bin/env python
# -*- coding: utf-8 -*-


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

    def setParent(self, parent):
        if parent != None:
            self.parent = parent
            self.parent.appendChild(self)
        else:
            self.parent = None

    def appendChild(self, child):
        self.children.append(child)

    def childAtRow(self, row):
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
