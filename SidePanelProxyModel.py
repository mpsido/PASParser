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

    def setCurrentNode(self, node):
        self.currentNode = node
#        self.dataChanged.emit(self.index(0,0), self.index(self.rowCount(), 1))
        self.layoutChanged.emit()


    def flags(self, index):
        flags = QAbstractItemModel.flags(self, index)
        if index.column() == 1:
            flags |= Qt.ItemIsEditable
        return flags

    def data(self, index, role):
        if role != Qt.DisplayRole:
            return super(SidePanelProxyModel, self).data(index, role)

        sourceIndex = self.mapToSource(index)
        if hasattr(self, 'currentNode'):
            if index.column() == 0:
                return QVariant(self.currentNode.childAtRow(sourceIndex.row()).name)
            elif index.column() == 1:
                if self.currentNode.typeOfNode == ENUM_TYPE_NODE_OBJECT:
                    return QVariant(self.currentNode.childAtRow(sourceIndex.row()).pasTypeOrObject.value)
                elif self.currentNode.typeOfNode == ENUM_TYPE_NODE_TYPE_IN_OBJECT:
                    if len(self.currentNode) > 0:
                        return QVariant( self.currentNode.childAtRow(sourceIndex.row()).pasTypeOrObject[sourceIndex.row()] )
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

