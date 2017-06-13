#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QT_TR_NOOP as tr
import sys
import re

import ui_MainWindow

class PASParserMainWindow(QtGui.QMainWindow, ui_MainWindow.Ui_MainWindow):
	def __init__(self, parent=None):
		super(PASParserMainWindow, self).__init__(parent)
		self.setupUi(self)

	@QtCore.pyqtSlot() # signal with no arguments
	def on_action_Import_triggered(self):
		my_dir = QtGui.QFileDialog.getExistingDirectory(self, tr("Open a folder"), ".", QtGui.QFileDialog.ShowDirsOnly)
		self.tabWidget.setTabText(0, re.split(r'[/\\]', my_dir)[-1] )

	def main(self):
		self.show()

if __name__=='__main__':
	app = QtGui.QApplication(sys.argv)
	pasParserMainWindow = PASParserMainWindow()
	pasParserMainWindow.main()
	app.exec_()
