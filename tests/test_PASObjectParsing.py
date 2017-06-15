#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
# lib_path = os.path.abspath(os.path.join('..', '..', '..', 'lib'))
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
lib_path = os.path.abspath('.')
sys.path.append(lib_path)

import unittest
from PASType import *
from PASObject import *
from print_debug import *


class Test_PASObjReader(unittest.TestCase):
    def setUp(self):
        self.objReader = PASObjReader()
        set_debug_flags(0)

    def test_10000(self):

        self.assertEqual( self.objReader.parseObject("10000")
        , "AA BB CC DD EE EE EE EE EE EE EE EE EE EE EE EE EE EE EE FF GG 000000 HHHHHHHH IIIIII IIIIII IIIIII IIIIII IIIIII IIIIII")

        self.assertEqual(self.objReader["10000"][0].range_, (0,0))
        self.assertEqual(self.objReader["10000"][1].range_, (1,1))
        self.assertEqual(self.objReader["10000"][2].range_, (2,2))
        self.assertEqual(self.objReader["10000"][3].range_, (3,3))

        self.assertEqual(self.objReader["10000"][4].arraySize, 15)
        index = 4
        for i in range (0, 15):
            self.assertEqual(self.objReader["10000"][4].range_[i], (index,index))
            index += 1


        self.assertEqual(self.objReader["10000"][5].range_, (19,19))
        self.assertEqual(self.objReader["10000"][6].range_, (20,20))
        self.assertEqual(self.objReader["10000"][7].range_, (24,27))


        self.assertEqual(self.objReader["10000"][8].arraySize, 6)
        index = 28
        for i in range (0, 6):
            self.assertEqual(self.objReader["10000"][8].range_[i], (index,index+2))
            index += 3

        #Data reading
        self.assertEqual(self.objReader["10000"].readData("1B 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 00 03 000000 0B01010A 010110 000000 000000 000000 000000 000000"),
        {'sub0':'1B',
        'eEquipType':'01',
        'u8Number':'02',
        'xBaseAddress':'0A',
        'eBoard_slot': ['14','0D','09','00','00','00','00','00','00','00','00','00','00','00','00'],
        'xEAES_Used':'00',
        'eVariant':'03',
        'xSNTPMaster':'0B01010A',
        'tSubSlotType':['010110','000000','000000','000000','000000','000000']})

        self.assertEqual(self.objReader["10000"]['sub0'].value, '1B')
        self.assertEqual(self.objReader["10000"]['eEquipType'].value, '01')
        self.assertEqual(self.objReader["10000"]['u8Number'].value, '02')
        self.assertEqual(self.objReader["10000"]['xBaseAddress'].value, '0A')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][0], '14')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][1], '0D')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][2], '09')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][3], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][4], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][5], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][6], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][7], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][8], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][9], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][10], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][11], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][12], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][13], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][14], '00')
        self.assertEqual(self.objReader["10000"]['xEAES_Used'].value, '00')
        self.assertEqual(self.objReader["10000"]['eVariant'].value, '03')
        self.assertEqual(self.objReader["10000"]['xSNTPMaster'].value, '0B01010A')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][0], '010110')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][1], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][2], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][3], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][4], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][5], '000000')

    def test_11001(self):
        self.assertEqual( self.objReader.parseObject("11001")
        , "AA BBBBBBBB 00 CCCC DDDD")

    def test_74000(self):
        self.assertEqual( self.objReader.parseObject("74000")
        , "AA 00 BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB CCCCCCCCCCCCCCCCCCCC")


        self.assertEqual(self.objReader["74000"][0].range_, (0,0))
        self.assertEqual(self.objReader["74000"][1].range_, (2,33))
        self.assertEqual(self.objReader["74000"][2].range_, (34,43))

        self.assertEqual(self.objReader["74000"].readData("02 00 606D0C006054D052584D50463863580260096400D00764003200640001010104 00A41011301068ABE000"),
        {'sub0':'02',
        'xPSEConfig':'606D0C006054D052584D50463863580260096400D00764003200640001010104',
        'xExtBoardPowerConfig':'00A41011301068ABE000'})

        self.assertEqual(self.objReader["74000"]['sub0'].value, '02')
        self.assertEqual(self.objReader["74000"]['xPSEConfig'].value, '606D0C006054D052584D50463863580260096400D00764003200640001010104')
        self.assertEqual(self.objReader["74000"]['xExtBoardPowerConfig'].value, '00A41011301068ABE000')

    def test_71B00(self):
        self.assertEqual( self.objReader.parseObject("71B00")
            , "AA BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB")

        self.assertEqual(self.objReader["71B00"][0].range_, (0,0))

        self.assertEqual(self.objReader["71B00"][1].arraySize, 255)
        index = 1
        for i in range (0, 255):
            self.assertEqual(self.objReader["71B00"][1].range_[i], (index,index))
            index += 1

    def test_30092(self):
        self.assertEqual( self.objReader.parseObject("30092")
            , "AA BB CCCC DDDD EEEE FF 00 GGGGGGGGGGGGGGGGGGGG HHHH")

        self.assertEqual(self.objReader["30092"][0].range_, (0,0))
        self.assertEqual(self.objReader["30092"][1].range_, (1,1))
        self.assertEqual(self.objReader["30092"][2].range_, (2,3))
        self.assertEqual(self.objReader["30092"][3].range_, (4,5))
        self.assertEqual(self.objReader["30092"][4].range_, (6,7))
        self.assertEqual(self.objReader["30092"][5].range_, (8,8))
        self.assertEqual(self.objReader["30092"][6].range_, (10,19))
        self.assertEqual(self.objReader["30092"][7].range_, (20,21))


    def test_modify_1000(self):
        self.objReader.parseObject("10000")

        data_10000 = "1B 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 00 03 000000 0B01010A 010110 000000 000000 000000 000000 000000"
        self.objReader["10000"].readData(data_10000)

        data_10000_modified = self.objReader["10000"].modifyData("xEAES_Used", "15")
        self.assertEqual(data_10000_modified, "1B 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 15 03 000000 0B01010A 010110 000000 000000 000000 000000 000000")

        self.assertEqual(self.objReader["10000"]['sub0'].value, '1B')
        self.assertEqual(self.objReader["10000"]['eEquipType'].value, '01')
        self.assertEqual(self.objReader["10000"]['u8Number'].value, '02')
        self.assertEqual(self.objReader["10000"]['xBaseAddress'].value, '0A')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][0], '14')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][1], '0D')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][2], '09')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][3], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][4], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][5], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][6], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][7], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][8], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][9], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][10], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][11], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][12], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][13], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][14], '00')
        self.assertEqual(self.objReader["10000"]['xEAES_Used'].value, '15')
        self.assertEqual(self.objReader["10000"]['eVariant'].value, '03')
        self.assertEqual(self.objReader["10000"]['xSNTPMaster'].value, '0B01010A')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][0], '010110')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][1], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][2], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][3], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][4], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][5], '000000')


        data_10000_modified = self.objReader["10000"].modifyData("eBoard_slot", "12", 4)
        self.assertEqual(data_10000_modified, "1B 01 02 0A 14 0D 09 00 12 00 00 00 00 00 00 00 00 00 00 15 03 000000 0B01010A 010110 000000 000000 000000 000000 000000")

        self.assertEqual(self.objReader["10000"]['sub0'].value, '1B')
        self.assertEqual(self.objReader["10000"]['eEquipType'].value, '01')
        self.assertEqual(self.objReader["10000"]['u8Number'].value, '02')
        self.assertEqual(self.objReader["10000"]['xBaseAddress'].value, '0A')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][0], '14')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][1], '0D')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][2], '09')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][3], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][4], '12')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][5], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][6], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][7], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][8], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][9], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][10], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][11], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][12], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][13], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][14], '00')
        self.assertEqual(self.objReader["10000"]['xEAES_Used'].value, '15')
        self.assertEqual(self.objReader["10000"]['eVariant'].value, '03')
        self.assertEqual(self.objReader["10000"]['xSNTPMaster'].value, '0B01010A')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][0], '010110')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][1], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][2], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][3], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][4], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][5], '000000')

        data_10000_modified = self.objReader["10000"].modifyData("tSubSlotType", "AA", 0)
        self.assertEqual(data_10000_modified, "1B 01 02 0A 14 0D 09 00 12 00 00 00 00 00 00 00 00 00 00 15 03 000000 0B01010A AA0000 000000 000000 000000 000000 000000")

        self.assertEqual(self.objReader["10000"]['sub0'].value, '1B')
        self.assertEqual(self.objReader["10000"]['eEquipType'].value, '01')
        self.assertEqual(self.objReader["10000"]['u8Number'].value, '02')
        self.assertEqual(self.objReader["10000"]['xBaseAddress'].value, '0A')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][0], '14')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][1], '0D')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][2], '09')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][3], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][4], '12')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][5], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][6], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][7], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][8], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][9], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][10], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][11], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][12], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][13], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][14], '00')
        self.assertEqual(self.objReader["10000"]['xEAES_Used'].value, '15')
        self.assertEqual(self.objReader["10000"]['eVariant'].value, '03')
        self.assertEqual(self.objReader["10000"]['xSNTPMaster'].value, '0B01010A')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][0], 'AA0000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][1], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][2], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][3], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][4], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][5], '000000')

        data_10000_modified = self.objReader["10000"].modifyData("tSubSlotType", "BAC", 1)
        self.assertEqual(data_10000_modified, "1B 01 02 0A 14 0D 09 00 12 00 00 00 00 00 00 00 00 00 00 15 03 000000 0B01010A AA0000 0BAC00 000000 000000 000000 000000")

        self.assertEqual(self.objReader["10000"]['sub0'].value, '1B')
        self.assertEqual(self.objReader["10000"]['eEquipType'].value, '01')
        self.assertEqual(self.objReader["10000"]['u8Number'].value, '02')
        self.assertEqual(self.objReader["10000"]['xBaseAddress'].value, '0A')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][0], '14')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][1], '0D')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][2], '09')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][3], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][4], '12')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][5], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][6], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][7], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][8], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][9], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][10], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][11], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][12], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][13], '00')
        self.assertEqual(self.objReader["10000"]['eBoard_slot'][14], '00')
        self.assertEqual(self.objReader["10000"]['xEAES_Used'].value, '15')
        self.assertEqual(self.objReader["10000"]['eVariant'].value, '03')
        self.assertEqual(self.objReader["10000"]['xSNTPMaster'].value, '0B01010A')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][0], 'AA0000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][1], '0BAC00')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][2], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][3], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][4], '000000')
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][5], '000000')

        self.objReader["10000"]['u8Number'].value = '45'
        self.objReader["10000"]['xBaseAddress'] = '10'
        self.assertEqual(self.objReader["10000"]['u8Number'].value, '45')
        self.assertEqual(self.objReader["10000"]['xBaseAddress'].value, '10')
        self.objReader["10000"]['tSubSlotType'][2] = '45'
        self.assertEqual(self.objReader["10000"]['tSubSlotType'][2], '450000')



unittest.main()
