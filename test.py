#!/usr/bin/python
# -*- coding: utf-8 -*-


"""TODO faire un vrai système de tests automatiques

"""

import re 
import unittest
from PASType import *
from PASObject import *


class Test_PASObjReader(unittest.TestCase):
	def setUp(self):
		self.typeReader = PASTypeReader() 
		self.objReader = PASObjReader()

	def test_Spectrum(self):
		self.assertEqual( self.objReader.getDataSpectrum("10000", self.typeReader)
		, "AA BB CC DD EE EE EE EE EE EE EE EE EE EE EE EE EE EE EE FF GG 000000 HHHHHHHH IIIIII IIIIII IIIIII IIIIII IIIIII IIIIII")


		self.assertEqual( self.objReader.getDataSpectrum("11001", self.typeReader)
		, "AA BBBBBBBB 00 CCCC DDDD")


		self.assertEqual( self.objReader.getDataSpectrum("74000", self.typeReader)
		, "AA 00 BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB CCCCCCCCCCCCCCCCCCCC")


		self.assertEqual( self.objReader.getDataSpectrum("71B00", self.typeReader)
			, "AA BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB")


unittest.main()