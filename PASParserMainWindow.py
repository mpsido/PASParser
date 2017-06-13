#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from PyQt4 import QtGui, QtCore
import sys

import ui_MainWindow

class Hello(QtGui.QMainWindow, ui_MainWindow.Ui_MainWindow):
	def __init__(self, parent=None):
		super(Hello, self).__init__(parent)
		self.setupUi(self)

	def main(self):
		self.show()

if __name__=='__main__':
	app = QtGui.QApplication(sys.argv)
	imageViewer = Hello()
	imageViewer.main()
	app.exec_()
