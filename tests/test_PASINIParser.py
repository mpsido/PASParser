#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
# lib_path = os.path.abspath(os.path.join('..', '..', '..', 'lib'))
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
lib_path = os.path.abspath('.')
sys.path.append(lib_path)

import unittest

from PASINIParser import *
from PASObjReader import *


class Test_PASINIParser(unittest.TestCase):
    def setUp(self):
        self.iniParser = PASINIParser()
        self.objReader = PASObjReader()


    def test_data74000(self):
        self.iniParser.parse("tests/files","74000")
        data_74000 = self.iniParser.getData()
        self.assertEqual(data_74000,
            '02 00 606D0C006054D052584D50463863580260096400D00764006400F40101010104 00A41011301068ABE000')

        self.objReader["74000"].readData(data_74000)
        data_74000_modified = self.objReader["74000"].modifyData("sub0", "04")

        self.iniParser.setData(data_74000_modified)

        data_74000 = self.iniParser.getData()
        self.assertEqual(data_74000,
            '04 00 606D0C006054D052584D50463863580260096400D00764006400F40101010104 00A41011301068ABE000')

        print(self.iniParser.sections())
        #write in file
        self.iniParser.write()

        #read file and test modification was written
        self.iniParser.parse("tests/files","74000")
        data_74000 = self.iniParser.getData()
        self.assertEqual(data_74000,
            '04 00 606D0C006054D052584D50463863580260096400D00764006400F40101010104 00A41011301068ABE000')

        #remodify data
        data_74000_modified = self.objReader["74000"].modifyData("sub0", "02")
        self.iniParser.setData(data_74000_modified)
        data_74000 = self.iniParser.getData()
        self.assertEqual(data_74000,
            '02 00 606D0C006054D052584D50463863580260096400D00764006400F40101010104 00A41011301068ABE000')

        #rewrite file
        self.iniParser.write()

        #reread and test data is back to normal
        self.iniParser.parse("tests/files","74000")
        data_74000 = self.iniParser.getData()
        self.assertEqual(data_74000,
            '02 00 606D0C006054D052584D50463863580260096400D00764006400F40101010104 00A41011301068ABE000')





unittest.main()
