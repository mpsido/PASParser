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

from print_debug import *

import ui_MainWindow


set_debug_flags(DEBUG_FLAG_ADD_REMOVE_ELEMENTS | DEBUG_MMI | DEBUG_DDS_OPT_PARSING)

class PASParserMainWindow(QtGui.QMainWindow, ui_MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(PASParserMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.pasDir = []
        self.model = {}
        self.sidePanelModel = {}
        self.proxyModel = {}
        self.treeView = {}
        self.hasModifToSave = {}

        self.ddsParser = {}
        self.objReader = {}

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

        if os.path.isdir(fullPath) == False:
            return

        self.pasDir.append(fullPath)
        shortPath = re.split(r'[/\\]', fullPath)[-1]

        self.objReader[fullPath] = PASObjReader()

        model = PASParserTreeModel(self)
        model.dataChanged.connect(self.repaintViews)
        model.dataChanged.connect(self.writeData)
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
        treeView.clicked.connect(self.constructItemChildrenAndBrothers)

        treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
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
    def constructItemChildrenAndBrothers(self, proxyIndex):
        """Creates the children of an object when we click on it"""
        path = str(self.tabWidget.tabToolTip(self.tabWidget.currentIndex()))
        index = self.proxyModel[path].mapToSource(proxyIndex)
        model = self.model[path]
        node = model.nodeFromIndex(index)
        if model.rowCount(index) == 0 and model.isChildOfRoot(index):
            objectId = node.id
            fullPath = os.sep.join([path,objectId])
            if path not in self.ddsParser:
                self.ddsParser[path] = PASDDSParser()
            self.ddsParser[path].parse(path, objectId)

            for i in range(0, self.ddsParser[path].getNbObjects(objectId)):
                if i > 0: #if the file contains many [PAS_OD_WRITE] fields
                    nodeIdInDDS = self.ddsParser[path].getId(objectId, i)
                    print_debug("nodeIdInDDS {0} for offset {1}, fullPath {2}".format(nodeIdInDDS, i, fullPath), DEBUG_MMI)
                    parsedObj = self.objReader[path].addIndexToObject(nodeIdInDDS, objectId)
                    node = PASObjectNode(nodeIdInDDS, '', '', '', parsedObj, model.root)
                    model.insertRow(index.row() + i, QtCore.QModelIndex())

                data = self.ddsParser[path].getData(objectId, i)

                node.rangeOrObjectName = self.objReader[path][node.id].objectName
                self.objReader[path][node.id].readData(data)
                node.pasTypeOrObject = self.objReader[path][node.id]

                for j, field in enumerate(self.objReader[path][node.id].fields):
                    if field.arraySize == 1:
                        PASObjectNode(field.nameOfField, "byte {0} to {1}".format(field.range_[0], field.range_[1]),
                            field.size, field.arraySize, self.objReader[path][node.id][field.nameOfField], node)
                    else: #in case of array append each field of the array
                        arrayNode = PASObjectNode(field.nameOfField, "byte {0} to {1}".format(field.range_[0][0], field.range_[-1][1]),
                            field.size, field.arraySize, self.objReader[path][node.id][field.nameOfField], node)
                        for i in range(0, field.arraySize):
                            PASObjectNode(field.nameOfField + "[{0}]".format(i), "byte {0} to {1}".format(field.range_[i][0], field.range_[i][1]),
                                                field.size, field.arraySize, self.objReader[path][node.id][field.nameOfField], arrayNode)
                        if model.insertRows(0, field.arraySize, model.index(i, 0, model.index(j, 0, index) )) == False:
                            print("Failed to insert array rows to {0}".format(field.nameOfField))
                if model.insertRows(0, self.objReader[path][node.id].nbFields(), index) == False:
                    print("Failed to insert row to {0}".format(model.nodeFromIndex(index).id))


        elif node.typeOfNode == ENUM_TYPE_NODE_OBJECT or node.typeOfNode == ENUM_TYPE_NODE_TYPE_IN_OBJECT:
            print_debug("Load node {0}".format(node.id), DEBUG_MMI)
            self.sidePanelModel[path].setCurrentNodeIndex(index)
            self.tableView.setModel(self.sidePanelModel[path])



    @QtCore.pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex) # signal with arguments
    def writeData(self, index, indexEnd):
        """Writes updated data in PAS DDS file"""
        path = str(self.tabWidget.tabToolTip(self.tabWidget.currentIndex()))
        node = self.model[path].nodeFromIndex(index)
        id = node.pasTypeOrObject.objectIndex
        data = self.objReader[path][id].dataString
        if self.objReader[path][id].isDataValid(data):
            self.ddsParser[path].setData(id, data)
            if node.nodeUpdated:
                self.hasModifToSave[path] = True
        if self.hasModifToSave[path] == False:
            print_debug("Data at id {0} for path {1} was not modified".format(id, path), DEBUG_MMI)

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
        print_debug("PASParserMainWindow.item_addAction Add after {0}".format(self.actionNode.id), DEBUG_MMI)
        tabIndex = self.tabWidget.currentIndex()
        path = str(self.tabWidget.tabToolTip(tabIndex))
        actionId = int(self.actionNode.id, 16) + 1
        newId = hex(actionId)[2:]
        print_debug("PASParserMainWindow.item_addAction newId = {0}".format(newId), DEBUG_MMI)
        try:
            parsedObj = self.objReader[path].addIndexToObject(newId, self.actionNode.id)
        except PASParsingException as exception:
            print_debug(exception.message, DEBUG_MMI)
        except:
            print_debug("Unexpected error: {0}".format(sys.exc_info()[0]), DEBUG_MMI)
        else:
            print_debug("PASParserMainWindow.item_addAction adding accepted", DEBUG_MMI)
            self.ddsParser[path].appendDataId(self.actionNode.id, newId)
            self.ddsParser[path].parse(path, self.actionNode.id)
            self.ddsParser[path].parse(path, newId)
            node = PASObjectNode(newId, '', '', '', parsedObj, self.model[path].root)
            self.model[path].insertRow(self.actionIndex.row(), QtCore.QModelIndex())
            self.hasModifToSave[path] = True



    def item_removeAction(self):
        print_debug("Remove {0}".format(self.actionNode.id), DEBUG_MMI)
        tabIndex = self.tabWidget.currentIndex()
        path = str(self.tabWidget.tabToolTip(tabIndex))
        actionId = int(self.actionNode.id, 16)
        parsedObj = self.objReader[path].removeIndexAt(self.actionNode.id)
        self.ddsParser[path].removeDataAtId(self.actionNode.id)
        self.model[path].removeRow(self.actionIndex.row(), QtCore.QModelIndex())
        self.hasModifToSave[path] = True


    @QtCore.pyqtSlot(QtCore.QString) # signal with arguments
    def on_lineEdit_textChanged(self, qtText):
        """Called when user edits filters"""
        text = str(qtText)
        path = str(self.tabWidget.tabToolTip(self.tabWidget.currentIndex()))
        self.proxyModel[path].setFilterWildcard(qtText)
        self.proxyModel[path].setFilterRegExp(qtText)

    @QtCore.pyqtSlot(int) # signal with arguments
    def closeTab(self, tabIndex):
        path = str(self.tabWidget.tabToolTip(tabIndex))
        if path in self.hasModifToSave and self.hasModifToSave[path]:
          bSave = QtGui.QMessageBox.question(self, tr("Save"), tr("Do you want to save data in path {0} before leaving ?").format(path),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
          if bSave == QtGui.QMessageBox.Yes:
              for path,ddsParser in self.ddsParser.items():
                  ddsParser.write()
        self.tabWidget.removeTab(tabIndex)
        self.clearViews(path)

    def clearViews(self, path):
        if path in self.pasDir:
            self.pasDir.remove(path)
            self.proxyModel.pop(path).deleteLater()
            self.sidePanelModel.pop(path).deleteLater()
            self.model.pop(path).deleteLater()
            self.treeView.pop(path).deleteLater()
        else:
            print("Path: {0} not in self.pasDir\n{1}".format(path, self.pasDir))

    def closeEvent(self, event):
        for i in range(0, self.tabWidget.count()):
            self.closeTab(0)
        print("Bye bye")




if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    pasParserMainWindow = PASParserMainWindow()
    pasParserMainWindow.show()
    app.exec_()
