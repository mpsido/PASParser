#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import QT_TR_NOOP as tr

from PASParsedObject import *
from PASObjectNode import *


class PASParserTreeModel(QAbstractItemModel):

    def __init__(self, parent=None):
        super(PASParserTreeModel, self).__init__(parent)

        self.treeView = parent
        self.headers = [tr('Name'),tr('Range'),tr('Size'), tr('Nb elements'), tr('Value')]

        self.nbColumns = 5

        # Create root item
        self.root = PASObjectNode('', '', '', '', '', None)


    def flags(self, index):
        flags = QAbstractItemModel.flags(self, index)
        node = self.nodeFromIndex(index)
        if index.column() == 4 and (node.typeOfNode == ENUM_TYPE_NODE_ARRAY_ITEM_IN_OBJECT or
            (node.typeOfNode == ENUM_TYPE_NODE_TYPE_IN_OBJECT and len(node) == 0)):
            flags |= Qt.ItemIsEditable
        return flags

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[section])
        return QVariant()

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
            return QModelIndex()


    def setData(self, index, value, role = Qt.EditRole):
        success = False
        if role == Qt.EditRole:
            node = self.nodeFromIndex(index)
            if node.typeOfNode == ENUM_TYPE_NODE_TYPE_IN_OBJECT:
                node.pasTypeOrObject.value = str(value.toString())
                sucess = True
            elif node.typeOfNode == ENUM_TYPE_NODE_ARRAY_ITEM_IN_OBJECT:
                node.pasTypeOrObject[node.parent.rowOfChild(node)] = str(value.toString())
                sucess = True
        if (success):
            self.dataChanged.emit(index, index)
        return success

    def data(self, index, role):
        if role == Qt.DecorationRole:
            return QVariant()

        if role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignTop | Qt.AlignLeft))

        if role != Qt.DisplayRole:
            return QVariant()

        node = self.nodeFromIndex(index)

        if index.column() == 0:
            return QVariant(node.name)
        elif index.column() == 1:
            return QVariant(node.range_)
        elif index.column() == 2:
            return QVariant(node.size)
        elif index.column() == 3:
            return QVariant(node.nb_elements)
        elif index.column() == 4:
            if node.typeOfNode == ENUM_TYPE_NODE_TYPE_IN_OBJECT:
                return QVariant(node.pasTypeOrObject.value)
            elif node.typeOfNode == ENUM_TYPE_NODE_ARRAY_ITEM_IN_OBJECT:
                return QVariant( node.pasTypeOrObject[node.parent.rowOfChild(node)] )
            else:
                return QVariant()
        else:
            return QVariant()


    def columnCount(self, parent):
        return self.nbColumns


    def rowCount(self, parent):
        node = self.nodeFromIndex(parent)
        if node is None:
            return 0
        return len(node)


    def parent(self, child):
        if not child.isValid():
            return QModelIndex()

        node = self.nodeFromIndex(child)

        if node is None:
            return QModelIndex()

        parent = node.parent

        if parent is None:
            return QModelIndex()

        grandparent = parent.parent
        if grandparent is None:
            return QModelIndex()
        row = grandparent.rowOfChild(parent)

        assert row != - 1
        return self.createIndex(row, 0, parent)

    def isChildOfRoot(self, index):
        return self.parent(index) == QModelIndex()

    def nodeFromIndex(self, index):
        return index.internalPointer() if index.isValid() else self.root

    def changeData(self, index):
        self.dataChanged.emit(index, index)

