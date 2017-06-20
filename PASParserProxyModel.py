# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
#from PyQt4.QtCore import QT_TR_NOOP as tr
from PASParserTreeModel import *


class PASParserProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(PASParserProxyModel, self).__init__(parent)

    def filterAcceptsRow(self, source_row, source_parent):
        accept = True
        sourceModel = self.sourceModel()
        sourceIndex = sourceModel.index(source_row, 0, source_parent)
        node = sourceModel.nodeFromIndex(sourceIndex)
        if node.typeOfNode == ENUM_TYPE_NODE_OBJECT:
            if self.filterRegExp().indexIn(node.id) == -1:
                accept = False
        return accept

    def rowCount(self, parent):
        sourceIndex = self.mapToSource(parent)
        node = self.sourceModel().nodeFromIndex(sourceIndex)
        if node.typeOfNode >= ENUM_TYPE_NODE_OBJECT:
            return len(node)
        else:
            return super(PASParserProxyModel, self).rowCount(parent)
