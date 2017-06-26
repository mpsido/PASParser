#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
from MMI.PASParserMainWindow import *


lib_path = os.path.abspath('.')
sys.path.append(lib_path)


lib_path = os.path.abspath('XMLParsing')
sys.path.append(lib_path)

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    pasParserMainWindow = PASParserMainWindow()
    pasParserMainWindow.show()
    app.exec_()
