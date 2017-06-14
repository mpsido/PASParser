#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QT_TR_NOOP as tr
import sys
import re
import os
from PASObject import *
from PASType import *
from PASParserTreeModel import PASParserTreeModel,PASObjectNode

import ui_MainWindow

class PASParserMainWindow(QtGui.QMainWindow, ui_MainWindow.Ui_MainWindow):
	def __init__(self, parent=None):
		super(PASParserMainWindow, self).__init__(parent)
		self.setupUi(self)
		self.pasDir = []
		self.model = PASParserTreeModel(self)
		self.treeView.setModel(self.model)
		self.treeView.activated.connect(self.on_itemActivated)

		self.typeReader = PASTypeReader()
		self.objReader = PASObjReader()

	@QtCore.pyqtSlot() # signal with no arguments
	def on_action_Import_triggered(self):
		my_dir = QtGui.QFileDialog.getExistingDirectory(self, tr("Open a folder"), ".", QtGui.QFileDialog.ShowDirsOnly)

		self.pasDir.append(my_dir)
		self.tabWidget.setTabText(0, re.split(r'[/\\]', my_dir)[-1] )

		#find files whose name is a hexadecimal number
		objects = filter(lambda x: re.match(r'^[0-9A-Fa-f]+$', x), os.listdir(my_dir))
		print (objects)
		for obj in objects:
			PASObjectNode(obj, '', '', '', self.model.root)
		self.model.insertRows(0, len(objects), QtCore.QModelIndex())

	@QtCore.pyqtSlot(QtCore.QModelIndex) # signal with arguments
	def on_itemActivated(self, index):
		node = self.model.nodeFromIndex(index)
		spectrum = self.objReader.parseObject(node.name, self.typeReader)
		node.name = spectrum
		self.model.changeData(index)



	def main(self):
		self.show()

if __name__=='__main__':
	app = QtGui.QApplication(sys.argv)
	pasParserMainWindow = PASParserMainWindow()
	pasParserMainWindow.main()
	app.exec_()
