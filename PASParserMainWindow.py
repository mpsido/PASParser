#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QT_TR_NOOP as tr
import sys
import re
import os
from PASObjReader import *
from PASINIParser import *
from PASParserTreeModel import PASParserTreeModel,PASObjectNode

import ui_MainWindow

class PASParserMainWindow(QtGui.QMainWindow, ui_MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(PASParserMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pasDir = []
        self.model = {}
        self.treeView = {}

        self.iniParser = PASINIParser()
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
        if fullPath in self.pasDir:
            print("{0}: folder already open".format(fullPath))
            return

        self.pasDir.append(fullPath)
        shortPath = re.split(r'[/\\]', fullPath)[-1]

        model = PASParserTreeModel(self)
        self.model[fullPath] = model
        treeView = QtGui.QTreeView()
        self.treeView[fullPath] = treeView

        treeView.setModel(self.model[fullPath])
        treeView.setColumnWidth(0, 190)
        treeView.setColumnWidth(1, 130)
        treeView.setColumnWidth(2, 50)
        treeView.setColumnWidth(3, 100)
        treeView.clicked.connect(self.on_itemActivated)

        tabIndex = self.tabWidget.addTab(treeView, shortPath)
        # we save the full path in the toolTip we are gonna need it later (we can also use tabData)
        self.tabWidget.setTabToolTip(tabIndex, fullPath)

        #find files whose name is a hexadecimal number
        objects = filter(lambda x: re.match(r'^[0-9A-Fa-f]+$', x), os.listdir(fullPath))
        for obj in objects:
            PASObjectNode(obj, '', '', '', None, model.root)
        model.insertRows(0, len(objects), QtCore.QModelIndex())


    @QtCore.pyqtSlot(QtCore.QModelIndex) # signal with arguments
    def on_itemActivated(self, index):
        path = str(self.tabWidget.tabToolTip(self.tabWidget.currentIndex()))
        model = self.model[path]
        if model.rowCount(index) == 0 and model.isChildOfRoot(index):
            node = model.nodeFromIndex(index)
            self.iniParser.parse(path, node.name)
            data = self.iniParser.getData()
            self.objReader[node.name].readData(data)

            for j, field in enumerate(self.objReader[node.name].fields):
                if field.arraySize == 1:
                    PASObjectNode(field.nameOfField, "byte {0} to {1}".format(field.range_[0], field.range_[1]),
                        field.size, field.arraySize, self.objReader[node.name][field.nameOfField], node)
                else: #in case of array append each field of the array
                    arrayNode = PASObjectNode(field.nameOfField, "byte {0} to {1}".format(field.range_[0][0], field.range_[-1][1]),
                        field.size, field.arraySize, self.objReader[node.name][field.nameOfField], node)
                    for i in range(0, field.arraySize):
                        PASObjectNode(field.nameOfField + "[{}]".format(i), "byte {0} to {1}".format(field.range_[i][0], field.range_[i][1]),
                                            field.size, field.arraySize, self.objReader[node.name][field.nameOfField], arrayNode)
                    model.insertRows(0, field.arraySize, model.index(i, 0, model.index(j, 0, index) ))
            model.insertRows(0, self.objReader[node.name].nbFields(), index)



    def closeEvent(self, event):
        print("Bye bye")

    def main(self):
        self.show()

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    pasParserMainWindow = PASParserMainWindow()
    pasParserMainWindow.main()
    app.exec_()
