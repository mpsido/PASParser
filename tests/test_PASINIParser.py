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


class Test_PASINIParser(unittest.TestCase):
	def setUp(self):
		self.iniParser = PASINIParser() 


	def test_data74000(self):
		self.iniParser.parse("tests/files","74000")
		self.assertEqual(self.iniParser.getData(), 
			'02 00 606D0C006054D052584D50463863580260096400D00764006400F40101010104 00A41011301068ABE000')


unittest.main()