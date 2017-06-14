#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PASParserMainWindow import *


if __name__=='__main__':
	app = QtGui.QApplication(sys.argv)
	pasParserMainWindow = PASParserMainWindow()
	pasParserMainWindow.main()
	app.exec_()
