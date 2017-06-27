#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QT_TR_NOOP as tr

from DataContainers.ObjectData import *
from MMI.PASObjectNode import *

#eColumnNumbers = enum
(
    eId,
#    eObjectName,
    eRange,
    eSize,
    eNbElements,
    eValue
)=range(5)


class PASParserTreeModel(QtCore.QAbstractItemModel):

    def __init__(self, parent=None):
        super(PASParserTreeModel, self).__init__(parent)
        self.treeView = parent
        self.headers = [tr('Start index'), tr('Range'),tr('Size'), tr('Nb elements'), tr('Value')]
        self.nbColumns = 5

        # Create root item
        self.root = PASObjectNode('', '', '', '', '', None)


    def flags(self, index):
        flags =QtCore.QAbstractItemModel.flags(self, index)
        node = self.nodeFromIndex(index)
        if index.column() == eValue and (node.typeOfNode == ENUM_TYPE_NODE_ARRAY_ITEM_IN_OBJECT or
            (node.typeOfNode == ENUM_TYPE_NODE_TYPE_IN_OBJECT and len(node) == 0)):
            flags |= QtCore.Qt.ItemIsEditable
        return flags

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.headers[section])
        return QtCore.QVariant()

    def insertRow(self, row, parent):
        return self.insertRows(row, 1, parent)


    def insertRows(self, row, count, parent):
        self.beginInsertRows(parent, row, (row + (count - 1)))
        self.endInsertRows()
        return True


    def removeRow(self, row, parentIndex):
        return self.removeRows(row, 1, parentIndex)


    def removeRows(self, row, count, parentIndex):
        self.beginRemoveRows(parentIndex, row, row)
        node = self.nodeFromIndex(parentIndex)
        node.removeChild(row)
        self.endRemoveRows()

        return True


    def index(self, row, column, parent):
        node = self.nodeFromIndex(parent)
        if row < len(node):
            return self.createIndex(row, column, node.childAtRow(row))
        else:
            return QtCore.QModelIndex()


    def setData(self, index, value, role = QtCore.Qt.EditRole):
        success = False
        if role == QtCore.Qt.EditRole:
            node = self.nodeFromIndex(index)
            if node.typeOfNode == ENUM_TYPE_NODE_TYPE_IN_OBJECT:
                dataBefore = node.pasTypeOrObject.value
                node.pasTypeOrObject.value = str(value.toString())
                if node.pasTypeOrObject.value != dataBefore:
                    while node.parent is not None:
                        node.nodeUpdated = True
                        node = node.parent
                success = True
            elif node.typeOfNode == ENUM_TYPE_NODE_ARRAY_ITEM_IN_OBJECT:
                row = node.parent.rowOfChild(node)
                dataBefore = node.pasTypeOrObject[row]
                node.pasTypeOrObject[row] = str(value.toString())
                if node.pasTypeOrObject[row] != dataBefore:
                    while node.parent is not None:
                        node.nodeUpdated = True
                        node = node.parent
                success = True

        if (success):
            self.dataChanged.emit(index, index)
        return success

    def data(self, index, role):
        if role == QtCore.Qt.DecorationRole:
            return QtCore.QVariant()

        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.QVariant(int(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft))

        if role == QtCore.Qt.FontRole:
            node = self.nodeFromIndex(index)
            if node.nodeUpdated == True:
                font = QtGui.QFont()
                font.setBold(True)
                return font
            else:
                return QtCore.QVariant()

        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        node = self.nodeFromIndex(index)

        if index.column() == eId:
            return QtCore.QVariant(node.id)
#        elif index.column() == eObjectName:
#            return QtCore.QVariant(node.eObjectName)
        elif index.column() == eRange:
                return QtCore.QVariant(node.rangeOrObjectName)
        elif index.column() == eSize:
            return QtCore.QVariant(node.size)
        elif index.column() == eNbElements:
            if node.typeOfNode == ENUM_TYPE_NODE_OBJECT:
                return QtCore.QVariant(node.pasTypeOrObject.objectCount)
            else:
                return QtCore.QVariant(node.nb_elements)
        elif index.column() == eValue:
            if node.typeOfNode == ENUM_TYPE_NODE_TYPE_IN_OBJECT:
                return QtCore.QVariant(node.pasTypeOrObject.value)
            elif node.typeOfNode == ENUM_TYPE_NODE_ARRAY_ITEM_IN_OBJECT:
                return QtCore.QVariant( node.pasTypeOrObject[node.parent.rowOfChild(node)] )
            else:
                return QtCore.QVariant()
        else:
            return QtCore.QVariant()


    def columnCount(self, parent):
        return self.nbColumns


    def rowCount(self, parent):
        node = self.nodeFromIndex(parent)
        if node is None:
            return 0
        return len(node)


    def parent(self, child):
        if not child.isValid():
            return QtCore.QModelIndex()

        node = self.nodeFromIndex(child)

        if node is None:
            return QtCore.QModelIndex()

        parent = node.parent

        if parent is None:
            return QtCore.QModelIndex()

        grandparent = parent.parent
        if grandparent is None:
            return QtCore.QModelIndex()
        row = grandparent.rowOfChild(parent)

        assert row != - 1
        return self.createIndex(row, 0, parent)

    def isChildOfRoot(self, index):
        return self.parent(index) == QtCore.QModelIndex()

    def nodeFromIndex(self, index):
        return index.internalPointer() if index.isValid() else self.root

    def changeData(self, index):
        self.dataChanged.emit(index, index)

