#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QT_TR_NOOP as tr
import sys
import re
import os
from PASObject import *
from PASType import *
from PASINIParser import *
from PASParserTreeModel import PASParserTreeModel,PASObjectNode

import ui_MainWindow

class PASParserMainWindow(QtGui.QMainWindow, ui_MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(PASParserMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pasDir = {}
        self.model = PASParserTreeModel(self)
        self.treeView.setModel(self.model)
        self.treeView.setColumnWidth(0, 190)
        self.treeView.setColumnWidth(1, 130)
        self.treeView.setColumnWidth(2, 50)
        self.treeView.setColumnWidth(3, 100)
        self.treeView.clicked.connect(self.on_itemActivated)

        self.iniParser = PASINIParser()
        self.objReader = PASObjReader()

        #temporary code for tests:
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        my_dir = os.sep.join([cur_dir, 'ECS-ELITE_1_C-1'])

        self.pasDir[self.tabWidget.currentIndex()] = my_dir
        self.tabWidget.setTabText(0, re.split(r'[/\\]', my_dir)[-1] )
        objects = filter(lambda x: re.match(r'^[0-9A-Fa-f]+$', x), os.listdir(my_dir))
        for obj in objects:
            PASObjectNode(obj, '', '', '', '', self.model.root)
        self.model.insertRows(0, len(objects), QtCore.QModelIndex())


    @QtCore.pyqtSlot() # signal with no arguments
    def on_action_Import_triggered(self):
        my_dir = QtGui.QFileDialog.getExistingDirectory(self, tr("Open a folder"), ".", QtGui.QFileDialog.ShowDirsOnly)

        self.pasDir[self.tabWidget.currentIndex()] = my_dir
        self.tabWidget.setTabText(0, re.split(r'[/\\]', my_dir)[-1] )

        #find files whose name is a hexadecimal number
        objects = filter(lambda x: re.match(r'^[0-9A-Fa-f]+$', x), os.listdir(my_dir))
        for obj in objects:
            PASObjectNode(obj, '', '', '', self.model.root)
        self.model.insertRows(0, len(objects), QtCore.QModelIndex())

    @QtCore.pyqtSlot(QtCore.QModelIndex) # signal with arguments
    def on_itemActivated(self, index):
        if self.model.rowCount(index) == 0 and self.model.isChildOfRoot(index):
            node = self.model.nodeFromIndex(index)
            self.iniParser.parse(self.pasDir[self.tabWidget.currentIndex()], node.name)
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
                    self.model.insertRows(0, field.arraySize, self.model.index(i, 0, self.model.index(j, 0, index) ))
            self.model.insertRows(0, self.objReader[node.name].nbFields(), index)




    def main(self):
        self.show()

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    pasParserMainWindow = PASParserMainWindow()
    pasParserMainWindow.main()
    app.exec_()
