#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt4 import QtGui, QtCore
import sys

import ui_MainWindow

class PASParserMainWindow(QtGui.QMainWindow, ui_MainWindow.Ui_MainWindow):
	def __init__(self, parent=None):
		super(PASParserMainWindow, self).__init__(parent)
		self.setupUi(self)

	def on_action_Import_triggered(self):
		print("Import")

	def main(self):
		self.show()

if __name__=='__main__':
	app = QtGui.QApplication(sys.argv)
	pasParserMainWindow = PASParserMainWindow()
	pasParserMainWindow.main()
	app.exec_()
