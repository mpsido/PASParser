#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PASObjectNode import *
from PyQt4.QtCore import QT_TR_NOOP as tr



class SidePanelProxyModel(QSortFilterProxyModel):

    def __init__(self, parent=None):
        super(SidePanelProxyModel, self).__init__(parent)
        self.nbColumns = 2
        self.headers = [tr('Name'), tr('Value')]

    def rowCount(self, parent = QModelIndex()):
        if hasattr(self, 'currentNode'):
            return len(self.currentNode)
        else:
            return 0

    def setCurrentNodeIndex(self, index):
        node = self.sourceModel().nodeFromIndex(index)
        if node.typeOfNode == ENUM_TYPE_NODE_OBJECT or (node.typeOfNode == ENUM_TYPE_NODE_TYPE_IN_OBJECT and len(node) > 0):
            self.currentNodeIndex = index
            self.currentNode = node
            self.layoutChanged.emit()


    def setData(self, index, value, role = Qt.EditRole):
        return self.sourceModel().setData(self.sourceModel().index(index.row(), index.column(), self.currentNodeIndex), value, role)


    def flags(self, index):
        flags = QAbstractItemModel.flags(self, index)
        sourceIndex = self.mapToSource(index)
        if index.column() == 1 and len(self.currentNode.childAtRow(sourceIndex.row())) == 0:
            flags |= Qt.ItemIsEditable
        return flags

    def data(self, index, role):
        if role != Qt.DisplayRole:
            return self.sourceModel().data(self.sourceModel().index(index.row(), index.column(), self.currentNodeIndex), role)

        sourceIndex = self.mapToSource(index)
        if hasattr(self, 'currentNode'):
            if index.column() == 0:
                return QVariant(self.currentNode.childAtRow(sourceIndex.row()).id)
            elif index.column() == 1:
                if self.currentNode.typeOfNode == ENUM_TYPE_NODE_OBJECT:
                    return QVariant(self.currentNode.childAtRow(sourceIndex.row()).pasTypeOrObject.value)
                elif self.currentNode.typeOfNode == ENUM_TYPE_NODE_TYPE_IN_OBJECT:
                    if len(self.currentNode) > 0:
                        return QVariant( self.currentNode.pasTypeOrObject[sourceIndex.row()] )
                    else:
                        return QVariant(self.currentNode.pasTypeOrObject.value)
                else:
                    return QVariant()
            else:
                return QVariant()



    def columnCount(self, parent):
        return self.nbColumns


    #redéfinir headerData si je veux changer les colonnes
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[section])
        return QVariant()

