#!/usr/bin/python
# -*- coding: utf-8 -*-


"""TODO faire un vrai système de tests automatiques

"""

import re 
import unittest
from PASType import *
from PASObject import *
from print_debug import *


class Test_PASObjReader(unittest.TestCase):
	def setUp(self):
		self.typeReader = PASTypeReader() 
		self.objReader = PASObjReader()
		set_debug_flags(0)

	def test_10000(self):

		self.assertEqual( self.objReader.parseObject("10000", self.typeReader)
		, "AA BB CC DD EE EE EE EE EE EE EE EE EE EE EE EE EE EE EE FF GG 000000 HHHHHHHH IIIIII IIIIII IIIIII IIIIII IIIIII IIIIII")

		self.assertEqual(self.objReader.parsedObjects["10000"][0].range, (0,0))
		self.assertEqual(self.objReader.parsedObjects["10000"][1][0], (1,1))
		self.assertEqual(self.objReader.parsedObjects["10000"][2].range, (2,2))
		self.assertEqual(self.objReader.parsedObjects["10000"][3].range, (3,3))

		self.assertEqual(self.objReader.parsedObjects["10000"][4].arraySize, 15)
		index = 4
		for i in range (0, 15):
			self.assertEqual(self.objReader.parsedObjects["10000"][4][i], (index,index))
			index += 1


		self.assertEqual(self.objReader.parsedObjects["10000"][5].range, (19,19))
		self.assertEqual(self.objReader.parsedObjects["10000"][6].range, (20,20))
		self.assertEqual(self.objReader.parsedObjects["10000"][7].range, (24,27))


		self.assertEqual(self.objReader.parsedObjects["10000"][8].arraySize, 6)
		index = 28
		for i in range (0, 6):
			self.assertEqual(self.objReader.parsedObjects["10000"][8].range[i], (index,index+2))
			index += 3

		#Data reading
		self.assertEqual(self.objReader.parsedObjects["10000"].readData("1B 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 00 03 000000 0B01010A 010110 000000 000000 000000 000000 000000"),
		{'sub0':'1B',
		'eEquipType':'01',
		'u8Number':'02',
		'xBaseAddress':'0A',
		'eBoard_slot': ['14','0D','09','00','00','00','00','00','00','00','00','00','00','00','00'],
		'xEAES_Used':'00',
		'eVariant':'03',
		'xSNTPMaster':'0B01010A',
		'tSubSlotType':['010110','000000','000000','000000','000000','000000']})

	def test_11001(self):
		self.assertEqual( self.objReader.parseObject("11001", self.typeReader)
		, "AA BBBBBBBB 00 CCCC DDDD")

	def test_74000(self):
		self.assertEqual( self.objReader.parseObject("74000", self.typeReader)
		, "AA 00 BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB CCCCCCCCCCCCCCCCCCCC")


		self.assertEqual(self.objReader.parsedObjects["74000"][0].range, (0,0))
		self.assertEqual(self.objReader.parsedObjects["74000"][1].range, (2,33))
		self.assertEqual(self.objReader.parsedObjects["74000"][2].range, (34,43))

		self.assertEqual(self.objReader.parsedObjects["74000"].readData("02 00 606D0C006054D052584D50463863580260096400D00764003200640001010104 00A41011301068ABE000"),
		{'sub0':'02',
		'xPSEConfig':'606D0C006054D052584D50463863580260096400D00764003200640001010104',
		'xExtBoardPowerConfig':'00A41011301068ABE000'})

	def test_71B00(self):
		self.assertEqual( self.objReader.parseObject("71B00", self.typeReader)
			, "AA BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB")

		self.assertEqual(self.objReader.parsedObjects["71B00"][0].range, (0,0))

		self.assertEqual(self.objReader.parsedObjects["71B00"][1].arraySize, 255)
		index = 1
		for i in range (0, 255):
			self.assertEqual(self.objReader.parsedObjects["71B00"][1][i], (index,index))
			index += 1

	def test_30092(self):
		self.assertEqual( self.objReader.parseObject("30092", self.typeReader)
			, "AA BB CCCC DDDD EEEE FF 00 GGGGGGGGGGGGGGGGGGGG HHHH")

		self.assertEqual(self.objReader.parsedObjects["30092"][0].range, (0,0))
		self.assertEqual(self.objReader.parsedObjects["30092"][1][0], (1,1))
		self.assertEqual(self.objReader.parsedObjects["30092"][2].range, (2,3))
		self.assertEqual(self.objReader.parsedObjects["30092"][3].range, (4,5))
		self.assertEqual(self.objReader.parsedObjects["30092"][4].range, (6,7))
		self.assertEqual(self.objReader.parsedObjects["30092"][5].range, (8,8))
		self.assertEqual(self.objReader.parsedObjects["30092"][6].range, (10,19))
		self.assertEqual(self.objReader.parsedObjects["30092"][7].range, (20,21))


	def test_modify_1000(self):
		self.objReader.parseObject("10000", self.typeReader)
		
		data_10000 = "1B 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 00 03 000000 0B01010A 010110 000000 000000 000000 000000 000000"

		data_10000_modified = self.objReader.parsedObjects["10000"].modifyData(data_10000, "xEAES_Used", "15")
		self.assertEqual(data_10000_modified, "1B 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 15 03 000000 0B01010A 010110 000000 000000 000000 000000 000000")

		data_10000_modified = self.objReader.parsedObjects["10000"].modifyData(data_10000_modified, "eBoard_slot", "12", 4)
		self.assertEqual(data_10000_modified, "1B 01 02 0A 14 0D 09 00 12 00 00 00 00 00 00 00 00 00 00 15 03 000000 0B01010A 010110 000000 000000 000000 000000 000000")

		data_10000_modified = self.objReader.parsedObjects["10000"].modifyData(data_10000_modified, "tSubSlotType", "AA", 0)
		self.assertEqual(data_10000_modified, "1B 01 02 0A 14 0D 09 00 12 00 00 00 00 00 00 00 00 00 00 15 03 000000 0B01010A AA0000 000000 000000 000000 000000 000000")

		data_10000_modified = self.objReader.parsedObjects["10000"].modifyData(data_10000_modified, "tSubSlotType", "BAC", 0)
		self.assertEqual(data_10000_modified, "1B 01 02 0A 14 0D 09 00 12 00 00 00 00 00 00 00 00 00 00 15 03 000000 0B01010A 0BAC00 000000 000000 000000 000000 000000")







unittest.main()