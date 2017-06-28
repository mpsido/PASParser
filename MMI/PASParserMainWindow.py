#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt4.QtGui import QMainWindow,QTreeView, QFileDialog, QMenu, QAction
from PyQt4.QtCore import Qt, pyqtSlot
from PyQt4.QtCore import QModelIndex, QPoint, QString
from PyQt4.QtCore import QT_TR_NOOP as tr
import sys
import re
import os
from Common.print_debug import *
from DDS.DDSReader import *
from MMI.PASParserTreeModel import PASParserTreeModel
from MMI.PASParserProxyModel import *
from MMI.SidePanelProxyModel import *
from MMI.PASParserItemDelegate import PASParserItemDelegate


from Common.print_debug import *

import ui_MainWindow

class PASParserMainWindow(QMainWindow, ui_MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(PASParserMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.pasDir = []
        self.model = {}
        self.sidePanelModel = {}
        self.proxyModel = {}
        self.treeView = {}
        self.itemDelegate = {}
        self.hasModifToSave = {}

        self.ddsReader = {}

        self.tableView.setColumnWidth(2, 190)

        #temporary code for tests:
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        my_dir = os.sep.join([cur_dir, '../ECS-ELITE_1_C-1'])

        self.loadDDS(my_dir)

    @pyqtSlot() # signal with no arguments
    def on_action_Import_triggered(self):
        my_dir = QFileDialog.getExistingDirectory(self, tr("Open a folder"), ".", QFileDialog.ShowDirsOnly)

        self.loadDDS(str(my_dir))

    def loadDDS(self, path):
        """Creates a new tab view that represents the DDS in the selected path "path" """
        if path in self.pasDir:
            print("{0}: folder already open".format(path))
            return

        ddsReader = DDSReader()
        ddsReader.parse(path) #raises error if the path do not exist or do not contain DDS

        self.pasDir.append(path)
        shortPath = re.split(r'[/\\]', path)[-1]

        self.ddsReader[path] = ddsReader

        model = PASParserTreeModel(self)
        model.dataChanged.connect(self.repaintViews)
        model.dataChanged.connect(self.updateData)
        self.model[path] = model

        proxyModel = PASParserProxyModel(self)
        proxyModel.setSourceModel(model)
        self.proxyModel[path] = proxyModel

        sidePanelModel = SidePanelProxyModel(self)
        self.sidePanelModel[path] = sidePanelModel
        sidePanelModel.setSourceModel(model)

        itemDelegate = PASParserItemDelegate(self)
        itemDelegate.sourceModel = model
        itemDelegate.proxyModel = sidePanelModel
        self.itemDelegate[path] = itemDelegate

        treeView = QTreeView()
        self.treeView[path] = treeView
        treeView.setModel(proxyModel)
        treeView.setColumnWidth(0, 190)
        treeView.setColumnWidth(1, 190)
        treeView.setColumnWidth(2, 50)
        treeView.setColumnWidth(3, 100)
        treeView.clicked.connect(self.constructItemChildren)
        treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        treeView.customContextMenuRequested.connect(self.slot_TreeView_customContextMenuRequested)

        tabIndex = self.tabWidget.addTab(treeView, shortPath)
        # we save the full path in the toolTip we are gonna need it later (we can also use tabData)
        self.tabWidget.setTabToolTip(tabIndex, path)

        #find files whose name is a hexadecimal number
        indexes = ddsReader.getObjectIds()
        for id in indexes:
            PASObjectNode(id, '', '', '', ObjectData(0, self.ddsReader[path].getObject(id)), model.root)
        model.insertRows(0, len(indexes), QModelIndex())


    @pyqtSlot(QModelIndex) # signal with arguments
    def constructItemChildren(self, proxyIndex):
        """Creates the children of an object when we click on it"""
        path = str(self.tabWidget.tabToolTip(self.tabWidget.currentIndex()))
        index = self.proxyModel[path].mapToSource(proxyIndex)
        model = self.model[path]
        node = model.nodeFromIndex(index)
        if model.rowCount(index) == 0 and model.isChildOfRoot(index):
            objectId = node.id
            self.ddsReader[path].readObject(objectId)
            object = self.ddsReader[path].getObject(objectId)

            for j, field in enumerate(object.fields):
                if field.arraySize == 1:
                    PASObjectNode(field.nameOfField, "byte {0} to {1}".format(field.range_[0], field.range_[1]),
                        field.size, field.arraySize, object[field.nameOfField], node)
                else: #in case of array append each field of the array
                    arrayNode = PASObjectNode(field.nameOfField, "byte {0} to {1}".format(field.range_[0][0], field.range_[-1][1]),
                        field.size, field.arraySize, object[field.nameOfField], node)
                    for i in range(0, field.arraySize):
                        PASObjectNode(field.nameOfField + "[{0}]".format(i), "byte {0} to {1}".format(field.range_[i][0], field.range_[i][1]),
                                            field.size, field.arraySize, object[field.nameOfField], arrayNode)
                    if model.insertRows(0, field.arraySize, model.index(i, 0, model.index(j, 0, index) )) == False:
                        print("Failed to insert array rows to {0}".format(field.nameOfField))
            if model.insertRows(0, object.nbFields(), index) == False:
                print("Failed to insert row to {0}".format(model.nodeFromIndex(index).id))

        elif node.typeOfNode == ENUM_TYPE_NODE_OBJECT or node.typeOfNode == ENUM_TYPE_NODE_TYPE_IN_OBJECT:
            print_debug("Select node {0}".format(node.id), DEBUG_MMI)
            self.sidePanelModel[path].setCurrentNodeIndex(index)
            self.tableView.setModel(self.sidePanelModel[path])
            self.tableView.setItemDelegate(self.itemDelegate[path])
#            self.sidePanelModel[path].sort(0)



    @pyqtSlot(QModelIndex, QModelIndex) # signal with arguments
    def updateData(self, index, indexEnd):
        """Writes updated data in PAS DDS file"""
        path = str(self.tabWidget.tabToolTip(self.tabWidget.currentIndex()))
        node = self.model[path].nodeFromIndex(index)
        id = node.pasTypeOrObject.objectIndex
        self.ddsReader[path].updateObject(id)
        if node.nodeUpdated:
            self.hasModifToSave[path] = True
        if self.hasModifToSave[path] == False:
            print_debug("Data at id {0} for path {1} was not modified".format(id, path), DEBUG_MMI)

    @pyqtSlot(QModelIndex, QModelIndex) # signal with arguments
    def repaintViews(self, index, indexEnd):
        """Forces table view and tree view to update when data in model had changed"""
        path = str(self.tabWidget.tabToolTip(self.tabWidget.currentIndex()))
        self.proxyModel[path].layoutChanged.emit()
        self.sidePanelModel[path].layoutChanged.emit()

    @pyqtSlot(QPoint) # signal with arguments
    def slot_TreeView_customContextMenuRequested(self, point):
        path = str(self.tabWidget.tabToolTip(self.tabWidget.currentIndex()))
        index = self.treeView[path].indexAt(point)
        index = self.proxyModel[path].mapToSource(index)
        print_debug("PASParserMainWindow.slot_TreeView_customContextMenuRequested at row: {0}".format(index.row()), DEBUG_MMI)
        if index.isValid():
            contextMenu = QMenu("menu", self)
            node = self.model[path].nodeFromIndex(index)
            print_debug("PASParserMainWindow.slot_TreeView_customContextMenuRequested {0}".format(node.id), DEBUG_MMI)
            print_debug("PASParserMainWindow.slot_TreeView_customContextMenuRequested count: {0}".format(node.pasTypeOrObject.objectCount), DEBUG_MMI)
            if node.typeOfNode == ENUM_TYPE_NODE_OBJECT and node.pasTypeOrObject.objectCount > 1:
                actionAdd = QAction(tr("Add object"), self)
                actionRemove = QAction(tr("Remove object"), self)
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

        newId = self.ddsReader[path].copyObject(self.actionNode.id)

        print_debug("PASParserMainWindow.item_addAction newId = {0}".format(newId), DEBUG_MMI)

        node = PASObjectNode(newId, '', '', '', self.ddsReader[path].getObject(newId), self.model[path].root)
        self.model[path].insertRow(self.actionIndex.row(), QModelIndex())
        self.hasModifToSave[path] = True


    def item_removeAction(self):
        print_debug("Remove {0}".format(self.actionNode.id), DEBUG_MMI)
        tabIndex = self.tabWidget.currentIndex()
        path = str(self.tabWidget.tabToolTip(tabIndex))
        self.ddsReader[path].removeObject(self.actionNode.id)
        self.model[path].removeRow(self.actionIndex.row(), QModelIndex())
        self.hasModifToSave[path] = True
        # TODO: bug à la sauvegarde quand on remove tous les objects


    @pyqtSlot(QString) # signal with arguments
    def on_lineEdit_textChanged(self, qtText):
        """Called when user edits filters"""
        text = str(qtText)
        path = str(self.tabWidget.tabToolTip(self.tabWidget.currentIndex()))
        self.proxyModel[path].setFilterWildcard(qtText)
        self.proxyModel[path].setFilterRegExp(qtText)

    @pyqtSlot(int) # signal with arguments
    def closeTab(self, tabIndex):
        path = str(self.tabWidget.tabToolTip(tabIndex))
        if path in self.hasModifToSave and self.hasModifToSave[path]:
          bSave = QMessageBox.question(self, tr("Save"), tr("Do you want to save data in path {0} before leaving ?").format(path),
                    QMessageBox.Yes | QMessageBox.No)
          if bSave == QMessageBox.Yes:
              self.ddsReader[path].writeData()
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
    app = QApplication(sys.argv)
    pasParserMainWindow = PASParserMainWindow()
    pasParserMainWindow.show()
    app.exec_()
