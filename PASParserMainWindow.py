#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QT_TR_NOOP as tr
import sys
import re
import os
from PASObjReader import *
from PASDDSParser import *
from PASParserTreeModel import PASParserTreeModel,PASObjectNode
from PASParserProxyModel import *
from SidePanelProxyModel import *

import logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

import ui_MainWindow

class PASParserMainWindow(QtGui.QMainWindow, ui_MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(PASParserMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pasDir = []
        self.model = {}
        self.sidePanelModel = {}
        self.proxyModel = {}
        self.treeView = {}
        self.hasModifToSave = {}

        self.ddsParser = {}
        self.objReader = PASObjReader()

        #temporary code for tests:
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        my_dir = os.sep.join([cur_dir, 'ECS-ELITE_1_C-1'])

        self.loadDDS(my_dir)

    @QtCore.pyqtSlot() # signal with no arguments
    def on_action_Import_triggered(self):
        my_dir = QtGui.QFileDialog.getExistingDirectory(self, tr("Open a folder"), ".", QtGui.QFileDialog.ShowDirsOnly)

        self.loadDDS(str(my_dir))

    def loadDDS(self, fullPath):
        """Creates a new tab view that represents the DDS in the selected path "fullPath" """
        if fullPath in self.pasDir:
            print("{0}: folder already open".format(fullPath))
            return

        self.pasDir.append(fullPath)
        shortPath = re.split(r'[/\\]', fullPath)[-1]

        model = PASParserTreeModel(self)
        model.dataChanged.connect(self.repaintViews)
        model.dataChanged.connect(self.setData)
        proxyModel = PASParserProxyModel(self)
        proxyModel.setSourceModel(model)
        self.model[fullPath] = model
        self.proxyModel[fullPath] = proxyModel
        sidePanelModel = SidePanelProxyModel(self)
        self.sidePanelModel[fullPath] = sidePanelModel
        sidePanelModel.setSourceModel(model)
        treeView = QtGui.QTreeView()
        self.treeView[fullPath] = treeView

        treeView.setModel(proxyModel)
        treeView.setColumnWidth(0, 190)
        treeView.setColumnWidth(1, 190)
        treeView.setColumnWidth(2, 50)
        treeView.setColumnWidth(3, 100)
        treeView.clicked.connect(self.on_itemClicked)

        treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        treeView.customContextMenuRequested.connect(self.slot_TreeView_customContextMenuRequested)

        tabIndex = self.tabWidget.addTab(treeView, shortPath)
        # we save the full path in the toolTip we are gonna need it later (we can also use tabData)
        self.tabWidget.setTabToolTip(tabIndex, fullPath)

        #find files whose name is a hexadecimal number
        indexes = filter(lambda x: re.match(r'^[0-9A-Fa-f]+$', x), os.listdir(fullPath))
        for id in indexes:
            PASObjectNode(id, '', '', '', PASParsedObject(0), model.root)
        model.insertRows(0, len(indexes), QtCore.QModelIndex())


    @QtCore.pyqtSlot(QtCore.QModelIndex) # signal with arguments
    def on_itemClicked(self, proxyIndex):
        """Creates the children of an object when we click on it"""
        path = str(self.tabWidget.tabToolTip(self.tabWidget.currentIndex()))
        index = self.proxyModel[path].mapToSource(proxyIndex)
        model = self.model[path]
        node = model.nodeFromIndex(index)
        if model.rowCount(index) == 0 and model.isChildOfRoot(index):
            self.ddsParser[path+"/"+node.id] = PASDDSParser()
            self.ddsParser[path+"/"+node.id].parse(path, node.id)
            data = self.ddsParser[path+"/"+node.id].getData(node.id)
            node.rangeOrObjectName = self.objReader[node.id].objectName
            self.objReader[node.id].readData(data)
            node.pasTypeOrObject = self.objReader[node.id]

            for j, field in enumerate(self.objReader[node.id].fields):
                if field.arraySize == 1:
                    PASObjectNode(field.nameOfField, "byte {0} to {1}".format(field.range_[0], field.range_[1]),
                        field.size, field.arraySize, self.objReader[node.id][field.nameOfField], node)
                else: #in case of array append each field of the array
                    arrayNode = PASObjectNode(field.nameOfField, "byte {0} to {1}".format(field.range_[0][0], field.range_[-1][1]),
                        field.size, field.arraySize, self.objReader[node.id][field.nameOfField], node)
                    for i in range(0, field.arraySize):
                        PASObjectNode(field.nameOfField + "[{}]".format(i), "byte {0} to {1}".format(field.range_[i][0], field.range_[i][1]),
                                            field.size, field.arraySize, self.objReader[node.id][field.nameOfField], arrayNode)
                    if model.insertRows(0, field.arraySize, model.index(i, 0, model.index(j, 0, index) )) == False:
                        print("Failed to insert array rows to {0}".format(field.nameOfField))
            if model.insertRows(0, self.objReader[node.id].nbFields(), index) == False:
                print("Failed to insert row to {0}".format(model.nodeFromIndex(index).id))

        elif node.typeOfNode == ENUM_TYPE_NODE_OBJECT or node.typeOfNode == ENUM_TYPE_NODE_TYPE_IN_OBJECT:
            logging.debug("Load node {0}".format(node.id))
            self.sidePanelModel[path].setCurrentNodeIndex(index)
            self.tableView.setModel(self.sidePanelModel[path])



    @QtCore.pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex) # signal with arguments
    def setData(self, index, indexEnd):
        """Writes updated data in PAS DDS file """
        path = str(self.tabWidget.tabToolTip(self.tabWidget.currentIndex()))
        node = self.model[path].nodeFromIndex(index)
        id = node.pasTypeOrObject.objectIndex
        data = self.objReader[id].dataString
        if self.objReader[id].isDataValid(data):
            self.ddsParser[path+"/"+id].setData(id, data)
            if node.nodeUpdated:
                self.hasModifToSave[path] = True

    @QtCore.pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex) # signal with arguments
    def repaintViews(self, index, indexEnd):
        """Forces table view and tree view to update when data in model had changed"""
        path = str(self.tabWidget.tabToolTip(self.tabWidget.currentIndex()))
        self.proxyModel[path].layoutChanged.emit()
        self.sidePanelModel[path].layoutChanged.emit()

    @QtCore.pyqtSlot(QtCore.QPoint) # signal with arguments
    def slot_TreeView_customContextMenuRequested(self, point):
        path = str(self.tabWidget.tabToolTip(self.tabWidget.currentIndex()))
        index = self.treeView[path].indexAt(point)
        index = self.proxyModel[path].mapToSource(index)
        if index.isValid():
            contextMenu = QtGui.QMenu("menu", self)
            node = self.model[path].nodeFromIndex(index)
            if node.typeOfNode == ENUM_TYPE_NODE_OBJECT and node.pasTypeOrObject.objectCount > 1:
                actionAdd = QtGui.QAction(tr("Add object"), self)
                actionRemove = QtGui.QAction(tr("Remove object"), self)
                contextMenu.addAction(actionAdd)
                contextMenu.addAction(actionRemove)
                self.actionIndex = index
                self.actionNode = node
                actionAdd.triggered.connect(self.item_addAction)
                actionRemove.triggered.connect(self.item_removeAction)
                contextMenu.exec_(self.treeView[path].mapToGlobal(point))

    def item_addAction(self):
        logging.debug("Add {0}".format(self.actionNode.id))
    def item_removeAction(self):
        logging.debug("Remove {0}".format(self.actionNode.id))

    def closeEvent(self, event):
        #TODO this will only save current tab, create a save event for each tab closing event
        path = str(self.tabWidget.tabToolTip(self.tabWidget.currentIndex()))
        if path in self.hasModifToSave and self.hasModifToSave[path]:
            bSave = QMessageBox.question(self, tr("Save"), tr("Do you want to save data before leaving ?"), QMessageBox.Yes | QMessageBox.No)
            if bSave == QMessageBox.Yes:
                for path,ddsParser in self.ddsParser.items():
                    ddsParser.write()
        print("Bye bye")

    def main(self):
        self.show()

    @QtCore.pyqtSlot(QtCore.QString) # signal with arguments
    def on_lineEdit_textChanged(self, qtText):
        """Called when user edits filters"""
        text = str(qtText)
        path = str(self.tabWidget.tabToolTip(self.tabWidget.currentIndex()))
#        self.proxyModel[path].setFilterWildcard(qtText)
        self.proxyModel[path].setFilterRegExp(qtText)



if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    pasParserMainWindow = PASParserMainWindow()
    pasParserMainWindow.main()
    app.exec_()
