#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QAbstractItemModel
from PyQt4.QtCore import QVariant, Qt, QModelIndex
from PASObjectNode import *
from PyQt4.QtCore import QT_TR_NOOP as tr


(eName, eType, eValue) = range(3)


class SidePanelProxyModel(QtGui.QSortFilterProxyModel):

    def __init__(self, parent=None):
        super(SidePanelProxyModel, self).__init__(parent)
        self.nbColumns = 3
        self.headers = [tr('Name'), tr('Type'), tr('Value')]

    def rowCount(self, parent = QModelIndex()):
        if hasattr(self, 'currentNode'):
            return len(self.currentNode)
        else:
            return 0

    def mapToSource(self, index):
        if hasattr(self, 'currentNodeIndex'):
            return self.sourceModel().index(index.row(), index.column(), self.currentNodeIndex)
        else:
            return super(SidePanelProxyModel, self).mapToSource(index)

    def setCurrentNodeIndex(self, index):
        node = self.sourceModel().nodeFromIndex(index)
        if node.typeOfNode == ENUM_TYPE_NODE_OBJECT or (node.typeOfNode == ENUM_TYPE_NODE_TYPE_IN_OBJECT and len(node) > 0):
            self.beginRemoveRows(QModelIndex(), 0, self.rowCount())
            self.endRemoveRows()
            self.currentNodeIndex = index
            self.currentNode = node
            if len(self.currentNode) > 0:
                self.beginInsertRows(QModelIndex(), 0, len(self.currentNode))
                self.endInsertRows()
            else:
                self.beginInsertRow(QModelIndex(), 0)
                self.endInsertRow()
            self.layoutChanged.emit()


    def setData(self, index, value, role = Qt.EditRole):
        return self.sourceModel().setData(self.mapToSource(index), value, role)


    def flags(self, index):
        flags = QAbstractItemModel.flags(self, index)
        sourceIndex = self.mapToSource(index)
        if index.column() == eValue and len(self.currentNode.childAtRow(sourceIndex.row())) == 0:
            flags |= Qt.ItemIsEditable
        return flags

    def data(self, index, role):
        if role != Qt.DisplayRole:
            return self.sourceModel().data(self.mapToSource(index), role)

        sourceIndex = self.mapToSource(index)
        if hasattr(self, 'currentNode'):
            if index.column() == eName:
                return QVariant(self.currentNode.childAtRow(sourceIndex.row()).id)
#                return QVariant(self.currentNode.pasTypeOrObject.nameOfField)
            elif index.column() == eValue:
                if self.currentNode.typeOfNode == ENUM_TYPE_NODE_OBJECT:
                    return QVariant(self.currentNode.childAtRow(sourceIndex.row()).pasTypeOrObject.value)
                elif self.currentNode.typeOfNode == ENUM_TYPE_NODE_TYPE_IN_OBJECT:
                    if len(self.currentNode) > 0:
                        return QVariant( self.currentNode.pasTypeOrObject[sourceIndex.row()] )
                    else:
                        return QVariant(self.currentNode.pasTypeOrObject.value)
                else:
                    return QVariant()
            elif index.column() == eType:
                if self.currentNode.typeOfNode == ENUM_TYPE_NODE_TYPE_IN_OBJECT:
                    return QVariant(self.currentNode.pasTypeOrObject.cat)
                else:
                    return QVariant(self.currentNode.childAtRow(sourceIndex.row()).pasTypeOrObject.cat)
            else:
                return QVariant()



    def columnCount(self, parent):
        return self.nbColumns


    #redéfinir headerData si je veux changer les colonnes
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[section])
        return QVariant()

