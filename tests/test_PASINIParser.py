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
from PASType import *
from PASObject import *


class Test_PASINIParser(unittest.TestCase):
	def setUp(self):
		self.iniParser = PASINIParser() 
		self.objReader = PASObjReader()


	def test_data74000(self):
		self.iniParser.parse("tests/files","74000")
		data_74000 = self.iniParser.getData()
		self.assertEqual(data_74000, 
			'02 00 606D0C006054D052584D50463863580260096400D00764006400F40101010104 00A41011301068ABE000')

		data_74000_modified = self.objReader["74000"].modifyData(data_74000, "sub0", "04")

		self.iniParser.setData(data_74000_modified)

		data_74000 = self.iniParser.getData()
		self.assertEqual(data_74000, 
			'04 00 606D0C006054D052584D50463863580260096400D00764006400F40101010104 00A41011301068ABE000')


unittest.main()
