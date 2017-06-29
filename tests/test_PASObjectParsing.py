#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
# lib_path = os.path.abspath(os.path.join('..', '..', '..', 'lib'))
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
lib_path = os.path.abspath('.')
sys.path.append(lib_path)

import unittest
from DataContainers.ObjectDataContainer import *
#from Common.print_debug import *


class Test_ObjectDataContainer(unittest.TestCase):
    def setUp(self):
        self.pasObjContainer = ObjectDataContainer()
        set_debug_flags(0)

    def test_10000(self):

        self.assertEqual( self.pasObjContainer.parseObject("10000")
        , "AA BB CC DD EE EE EE EE EE EE EE EE EE EE EE EE EE EE EE FF GG 000000 HHHHHHHH IIIIII IIIIII IIIIII IIIIII IIIIII IIIIII")

        self.assertEqual(self.pasObjContainer["10000"][0].range_, (0,0))
        self.assertEqual(self.pasObjContainer["10000"][1].range_, (1,1))
        self.assertEqual(self.pasObjContainer["10000"][2].range_, (2,2))
        self.assertEqual(self.pasObjContainer["10000"][3].range_, (3,3))

        self.assertEqual(self.pasObjContainer["10000"][4].arraySize, 15)
        index = 4
        for i in range (0, 15):
            self.assertEqual(self.pasObjContainer["10000"][4].range_[i], (index,index))
            index += 1


        self.assertEqual(self.pasObjContainer["10000"][5].range_, (19,19))
        self.assertEqual(self.pasObjContainer["10000"][6].range_, (20,20))
        self.assertEqual(self.pasObjContainer["10000"][7].range_, (24,27))


        self.assertEqual(self.pasObjContainer["10000"][8].arraySize, 6)
        index = 28
        for i in range (0, 6):
            self.assertEqual(self.pasObjContainer["10000"][8].range_[i], (index,index+2))
            index += 3

        #Data reading
        self.assertEqual(self.pasObjContainer["10000"].readData("1B 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 00 03 000000 0B01010A 010110 000000 000000 000000 000000 000000"),
        {'sub0':'1B',
        'eEquipType':'01',
        'u8Number':'02',
        'xBaseAddress':'0A',
        'eBoard_slot': ['14','0D','09','00','00','00','00','00','00','00','00','00','00','00','00'],
        'xEAES_Used':'00',
        'eVariant':'03',
        'xSNTPMaster':'0B01010A',
        'tSubSlotType':['010110','000000','000000','000000','000000','000000']})

        self.assertEqual(self.pasObjContainer["10000"]['sub0'].value, '1B')
        self.assertEqual(self.pasObjContainer["10000"]['eEquipType'].value, '01')
        self.assertEqual(self.pasObjContainer["10000"]['u8Number'].value, '02')
        self.assertEqual(self.pasObjContainer["10000"]['xBaseAddress'].value, '0A')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][0], '14')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][1], '0D')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][2], '09')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][3], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][4], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][5], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][6], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][7], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][8], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][9], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][10], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][11], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][12], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][13], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][14], '00')
        self.assertEqual(self.pasObjContainer["10000"]['xEAES_Used'].value, '00')
        self.assertEqual(self.pasObjContainer["10000"]['eVariant'].value, '03')
        self.assertEqual(self.pasObjContainer["10000"]['xSNTPMaster'].value, '0B01010A')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][0], '010110')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][1], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][2], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][3], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][4], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][5], '000000')


    def test_11001(self):
        self.assertEqual( self.pasObjContainer.parseObject("11001")
        , "AA BBBBBBBB 00 CCCC DDDD")

        self.assertEqual(self.pasObjContainer['11001'].objectCount, 1)
        self.assertEqual(self.pasObjContainer['11001'].objectName, 'tDDS_Version_t')

    def test_74000(self):
        self.assertEqual( self.pasObjContainer.parseObject("74000")
        , "AA 00 BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB CCCCCCCCCCCCCCCCCCCC")


        self.assertEqual(self.pasObjContainer['74000'].objectCount, 1)
        self.assertEqual(self.pasObjContainer['74000'].objectName, 'tDDS_ELITE_MPE_t')


        self.assertEqual(self.pasObjContainer["74000"][0].range_, (0,0))
        self.assertEqual(self.pasObjContainer["74000"][1].range_, (2,33))
        self.assertEqual(self.pasObjContainer["74000"][2].range_, (34,43))

        self.assertDictEqual(self.pasObjContainer["74000"].readData("02 00 606D0C006054D052584D50463863580260096400D00764003200640001010104 00A41011301068ABE000"),
        {'sub0':'02',
        'xPSEConfig':'606D0C006054D052584D50463863580260096400D00764003200640001010104',
        'xExtBoardPowerConfig':'00A41011301068ABE000'})

        self.assertEqual(self.pasObjContainer["74000"]['sub0'].value, '02')
        self.assertEqual(self.pasObjContainer["74000"]['xPSEConfig'].value, '606D0C006054D052584D50463863580260096400D00764003200640001010104')
        self.assertEqual(self.pasObjContainer["74000"]['xExtBoardPowerConfig'].value, '00A41011301068ABE000')

    def test_71B00(self):
        self.assertEqual( self.pasObjContainer.parseObject("71B00")
            , "AA BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB BB")


        self.assertEqual(self.pasObjContainer['71B00'].objectCount, 500)
        self.assertEqual(self.pasObjContainer['71B00'].objectName, 'tDDS_T_NET_Device_Def_Block_List_t')

        self.assertEqual(self.pasObjContainer["71B00"][0].range_, (0,0))

        self.assertEqual(self.pasObjContainer["71B00"][1].arraySize, 255)
        index = 1
        for i in range (0, 255):
            self.assertEqual(self.pasObjContainer["71B00"][1].range_[i], (index,index))
            index += 1

    def test_30092(self):
        self.assertEqual( self.pasObjContainer.parseObject("30092")
            , "AA BB CCCC DDDD EEEE FF 00 GGGGGGGGGGGGGGGGGGGG HHHH")


        self.assertEqual(self.pasObjContainer['30092'].objectCount, 13)
        self.assertEqual(self.pasObjContainer['30092'].objectName, 'tDDS_SlotInfoM4EVAC_t')

        self.assertEqual(self.pasObjContainer["30092"][0].range_, (0,0))
        self.assertEqual(self.pasObjContainer["30092"][1].range_, (1,1))
        self.assertEqual(self.pasObjContainer["30092"][2].range_, (2,3))
        self.assertEqual(self.pasObjContainer["30092"][3].range_, (4,5))
        self.assertEqual(self.pasObjContainer["30092"][4].range_, (6,7))
        self.assertEqual(self.pasObjContainer["30092"][5].range_, (8,8))
        self.assertEqual(self.pasObjContainer["30092"][6].range_, (10,19))
        self.assertEqual(self.pasObjContainer["30092"][7].range_, (20,21))


    def test_modify_1000(self):
        self.pasObjContainer.parseObject("10000")

        data_10000 = "1B 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 00 03 000000 0B01010A 010110 000000 000000 000000 000000 000000"
        self.pasObjContainer["10000"].readData(data_10000)


        self.assertEqual(self.pasObjContainer['10000'].objectCount, 1)
        self.assertEqual(self.pasObjContainer['10000'].objectName, 'tDDS_EqInfo_t')

        data_10000_modified = self.pasObjContainer["10000"].modifyData("xEAES_Used", "15")
        self.assertEqual(data_10000_modified, "1B 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 15 03 000000 0B01010A 010110 000000 000000 000000 000000 000000")

        self.assertEqual(self.pasObjContainer["10000"]['sub0'].value, '1B')
        self.assertEqual(self.pasObjContainer["10000"]['eEquipType'].value, '01')
        self.assertEqual(self.pasObjContainer["10000"]['u8Number'].value, '02')
        self.assertEqual(self.pasObjContainer["10000"]['xBaseAddress'].value, '0A')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][0], '14')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][1], '0D')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][2], '09')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][3], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][4], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][5], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][6], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][7], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][8], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][9], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][10], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][11], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][12], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][13], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][14], '00')
        self.assertEqual(self.pasObjContainer["10000"]['xEAES_Used'].value, '15')
        self.assertEqual(self.pasObjContainer["10000"]['eVariant'].value, '03')
        self.assertEqual(self.pasObjContainer["10000"]['xSNTPMaster'].value, '0B01010A')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][0], '010110')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][1], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][2], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][3], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][4], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][5], '000000')


        data_10000_modified = self.pasObjContainer["10000"].modifyData("eBoard_slot", "12", 4)
        self.assertEqual(data_10000_modified, "1B 01 02 0A 14 0D 09 00 12 00 00 00 00 00 00 00 00 00 00 15 03 000000 0B01010A 010110 000000 000000 000000 000000 000000")

        self.assertEqual(self.pasObjContainer["10000"]['sub0'].value, '1B')
        self.assertEqual(self.pasObjContainer["10000"]['eEquipType'].value, '01')
        self.assertEqual(self.pasObjContainer["10000"]['u8Number'].value, '02')
        self.assertEqual(self.pasObjContainer["10000"]['xBaseAddress'].value, '0A')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][0], '14')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][1], '0D')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][2], '09')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][3], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][4], '12')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][5], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][6], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][7], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][8], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][9], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][10], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][11], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][12], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][13], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][14], '00')
        self.assertEqual(self.pasObjContainer["10000"]['xEAES_Used'].value, '15')
        self.assertEqual(self.pasObjContainer["10000"]['eVariant'].value, '03')
        self.assertEqual(self.pasObjContainer["10000"]['xSNTPMaster'].value, '0B01010A')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][0], '010110')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][1], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][2], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][3], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][4], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][5], '000000')

        data_10000_modified = self.pasObjContainer["10000"].modifyData("tSubSlotType", "AA", 0)
        self.assertEqual(data_10000_modified, "1B 01 02 0A 14 0D 09 00 12 00 00 00 00 00 00 00 00 00 00 15 03 000000 0B01010A AA0000 000000 000000 000000 000000 000000")

        self.assertEqual(self.pasObjContainer["10000"]['sub0'].value, '1B')
        self.assertEqual(self.pasObjContainer["10000"]['eEquipType'].value, '01')
        self.assertEqual(self.pasObjContainer["10000"]['u8Number'].value, '02')
        self.assertEqual(self.pasObjContainer["10000"]['xBaseAddress'].value, '0A')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][0], '14')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][1], '0D')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][2], '09')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][3], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][4], '12')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][5], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][6], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][7], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][8], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][9], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][10], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][11], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][12], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][13], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][14], '00')
        self.assertEqual(self.pasObjContainer["10000"]['xEAES_Used'].value, '15')
        self.assertEqual(self.pasObjContainer["10000"]['eVariant'].value, '03')
        self.assertEqual(self.pasObjContainer["10000"]['xSNTPMaster'].value, '0B01010A')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][0], 'AA0000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][1], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][2], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][3], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][4], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][5], '000000')

        data_10000_modified = self.pasObjContainer["10000"].modifyData("tSubSlotType", "BAC", 1)
        self.assertEqual(data_10000_modified, "1B 01 02 0A 14 0D 09 00 12 00 00 00 00 00 00 00 00 00 00 15 03 000000 0B01010A AA0000 0BAC00 000000 000000 000000 000000")

        self.assertEqual(self.pasObjContainer["10000"]['sub0'].value, '1B')
        self.assertEqual(self.pasObjContainer["10000"]['eEquipType'].value, '01')
        self.assertEqual(self.pasObjContainer["10000"]['u8Number'].value, '02')
        self.assertEqual(self.pasObjContainer["10000"]['xBaseAddress'].value, '0A')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][0], '14')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][1], '0D')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][2], '09')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][3], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][4], '12')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][5], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][6], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][7], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][8], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][9], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][10], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][11], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][12], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][13], '00')
        self.assertEqual(self.pasObjContainer["10000"]['eBoard_slot'][14], '00')
        self.assertEqual(self.pasObjContainer["10000"]['xEAES_Used'].value, '15')
        self.assertEqual(self.pasObjContainer["10000"]['eVariant'].value, '03')
        self.assertEqual(self.pasObjContainer["10000"]['xSNTPMaster'].value, '0B01010A')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][0], 'AA0000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][1], '0BAC00')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][2], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][3], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][4], '000000')
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][5], '000000')

        self.pasObjContainer["10000"]['u8Number'].value = '45'
        self.pasObjContainer["10000"]['xBaseAddress'] = '10'
        self.assertEqual(self.pasObjContainer["10000"]['u8Number'].value, '45')
        self.assertEqual(self.pasObjContainer["10000"]['xBaseAddress'].value, '10')
        self.pasObjContainer["10000"]['tSubSlotType'][2] = '45'
        self.assertEqual(self.pasObjContainer["10000"]['tSubSlotType'][2], '450000')

    def test_isDataValid(self):
        self.pasObjContainer.parseObject("74000")

        self.assertTrue(self.pasObjContainer._objectXmlReader.isDataValid("74000", "02 00 606D0C006054D052584D50463863580260096400D00764003200640001010104 00A41011301068ABE000"))
        self.assertTrue(self.pasObjContainer._objectXmlReader.isDataValid("74000", "02 00 606D0C006054D052584D50463863580260096400D00764003200640001010104 00A41011301068ABE000"))
        self.assertTrue(self.pasObjContainer._objectXmlReader.isDataValid("74000", "02 00 606D0C006054D052584D50463863580260096400D00764003200640001010104 00A41011301068ABEDC0"))
        self.assertTrue(self.pasObjContainer._objectXmlReader.isDataValid("74000", "af 00 606D0C006054D052584D50463863580260096400D00764003200640001010104 00A41011301068ABE000"))

        #too long
        self.assertFalse(self.pasObjContainer._objectXmlReader.isDataValid("74000", "0200 00 606D0C006054D052584D50463863580260096400D00764003200640001010104 00A41011301068ABE000"))

        #wrong spaces
        self.assertFalse(self.pasObjContainer._objectXmlReader.isDataValid("74000", "02 00  6D0C006054D052584D50463863580260096400D00764003200640001010104 00A41011301068ABE000"))
        self.assertFalse(self.pasObjContainer._objectXmlReader.isDataValid("74000", "02 00 6D0C006054D052584D50463863580260096400D00764003200640001010104 00A41011301068ABE000 "))

        #not hexadecimal
        self.assertFalse(self.pasObjContainer._objectXmlReader.isDataValid("74000", "hg 00 606D0C006054D052584D50463863580260096400D00764003200640001010104 00A41011301068ABE000"))

        #fiels are badly positioned
        self.assertFalse(self.pasObjContainer._objectXmlReader.isDataValid("74000", "021 0 606D0C006054D052584D50463863580260096400D00764003200640001010104 00A41011301068ABE000"))
        self.assertFalse(self.pasObjContainer._objectXmlReader.isDataValid("74000", "02 00 06D0C006054D052584D50463863580260096400D00764003200640001010104 500A41011301068ABE000"))


    def test_addIndexes(self):
        self.pasObjContainer.parseObject("20000")

        with self.assertRaises(PASParsingException) as exception:
            self.pasObjContainer.addIndexToObject("20001", "212165")
            self.assertEqual(exception.message == "ObjectDataContainer.addIndexToObject : start index 212165 do not exist")

        with self.assertRaises(PASParsingException) as exception:
            self.pasObjContainer.addIndexToObject("20000", "20000")
            self.assertEqual(exception.message == "ObjectDataContainer.addIndexToObject : index 20000 already exists")


        with self.assertRaises(PASParsingException) as exception:
            self.pasObjContainer.addIndexToObject("22048", "20000")
            self.assertEqual(exception.message == "Invalid objectIndex : 22048 for object at start_index=20000 : count = 2048)")

        with self.assertRaises(PASParsingException) as exception:
            self.pasObjContainer.addIndexToObject("19000", "20000")
            self.assertEqual(exception.message == "Invalid objectIndex : 19000 for object at start_index=20000 : count = 2048)")

        self.pasObjContainer.addIndexToObject("20004", "20000")

        self.assertEqual(self.pasObjContainer["20004"].spectrum, "AA BB CCCC DD EE FFFF GGGG HHHH II JJ KK LL MMMM NNNN")
        self.assertEqual(self.pasObjContainer["20000"].spectrum, "AA BB CCCC DD EE FFFF GGGG HHHH II JJ KK LL MMMM NNNN")

        with self.assertRaises(KeyError) as exception:
            self.pasObjContainer["20002"]

        with self.assertRaises(KeyError) as exception:
            self.pasObjContainer["20005"]


        data_20000 = "0D 06 0400 48 00 0000 0000 0000 08 00 00 00 0000 0000"

        self.pasObjContainer["20004"].readData(data_20000)

        self.assertEqual(self.pasObjContainer["20004"].dataString, data_20000)
        self.assertEqual(self.pasObjContainer["20000"].dataString, "")

        with self.assertRaises(IndexError) as exception:
            self.pasObjContainer["20004"]["sub4"]

        with self.assertRaises(KeyError) as exception:
            self.pasObjContainer["20004"]["sub4"] = "AA"
            self.assertEqual(exception.message, "Cannot modify field sub4 in object {1}: it does not exist")

        self.pasObjContainer["20004"]["sub0"] = "AA"
        self.assertEqual(self.pasObjContainer["20004"].dataString, "AA 06 0400 48 00 0000 0000 0000 08 00 00 00 0000 0000")

        self.pasObjContainer["20004"]["eCommandParam"] = "EE"
        self.assertEqual(self.pasObjContainer["20004"].dataString, "AA 06 0400 48 00 0000 0000 0000 08 EE 00 00 0000 0000")
        self.assertEqual(self.pasObjContainer["20000"].dataString, "")



    def test_removeIndexes(self):
        self.pasObjContainer.parseObject("20000")

        self.pasObjContainer.removeIndexAt("20000") #remove source index
        with self.assertRaises(KeyError) as exception:
            self.pasObjContainer["20000"]
            self.assertEqual(exception.message, "ObjectDataContainer.removeIndexAt : ObjectIndex 20000 do not exist, cannot remove it")

        # we should be able to add objects even if last object had been removed
        self.pasObjContainer.addIndexToObject("20004", "20000")

        with self.assertRaises(KeyError) as exception:
            self.pasObjContainer.removeIndexAt("20001")
            self.assertEqual(exception.message, "ObjectDataContainer.removeIndexAt : ObjectIndex 20001 do not exist, cannot remove it")

        self.pasObjContainer.removeIndexAt("20004")


        with self.assertRaises(KeyError) as exception:
            self.pasObjContainer["20004"]

        #test the following do not raise execption
        self.pasObjContainer["20000"]
        self.pasObjContainer.removeIndexAt("20000") #the source index should not be removed

        with self.assertRaises(KeyError) as exception:
            self.pasObjContainer["20000"]
            self.assertEqual(exception.message, "ObjectDataContainer.removeIndexAt : ObjectIndex 20000 do not exist, cannot remove it")

    def test_getStartIndexFromObjectIndex(self):
        self.pasObjContainer.parseObject("20000")
        self.assertEqual(self.pasObjContainer["20000"].objectCount, 2048)

        self.assertEqual("20000", self.pasObjContainer._objectXmlReader.getStartIndexFromObjectIndex("20045"))
        self.assertEqual("20000", self.pasObjContainer._objectXmlReader.getStartIndexFromObjectIndex("20111"))
        self.assertEqual("20000", self.pasObjContainer._objectXmlReader.getStartIndexFromObjectIndex("20000"))
        self.assertEqual("20000", self.pasObjContainer._objectXmlReader.getStartIndexFromObjectIndex("20799"))
        self.assertEqual("20000", self.pasObjContainer._objectXmlReader.getStartIndexFromObjectIndex("20047"))


        self.assertEqual("Invalid index", self.pasObjContainer._objectXmlReader.getStartIndexFromObjectIndex("20800"))
#        self.assertEqual("Invalid index", self.pasObjContainer._objectXmlReader.getStartIndexFromObjectIndex("74000"))
        self.assertEqual("Invalid index", self.pasObjContainer._objectXmlReader.getStartIndexFromObjectIndex("1945546"))
        self.assertEqual("Invalid index", self.pasObjContainer._objectXmlReader.getStartIndexFromObjectIndex("220"))


        self.pasObjContainer.parseObject("74000")
        self.assertEqual("74000", self.pasObjContainer._objectXmlReader.getStartIndexFromObjectIndex("74000"))


    def test_getDisplay(self):
        self.pasObjContainer.parseObject("10000")
        self.assertDictEqual(self.pasObjContainer["10000"].readData("1B 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 00 03 000000 0B01010A 010110 000000 000000 000000 000000 000000"),
        {'sub0':'1B',
        'eEquipType':'01',
        'u8Number':'02',
        'xBaseAddress':'0A',
        'eBoard_slot': ['14','0D','09','00','00','00','00','00','00','00','00','00','00','00','00'],
        'xEAES_Used':'00',
        'eVariant':'03',
        'xSNTPMaster':'0B01010A',
        'tSubSlotType':['010110','000000','000000','000000','000000','000000']})

        self.assertEqual(self.pasObjContainer["10000"]['sub0'].getDisplay(), '27')
        self.assertEqual(self.pasObjContainer["10000"]['eVariant'].getDisplay(), 'eEQ_VARIANT_ELITE')

        self.pasObjContainer["10000"]['eVariant'] = "00"
        self.assertEqual(self.pasObjContainer["10000"]['eVariant'].getDisplay(), 'eEQ_VARIANT_NOT_APPLICABLE')
        self.pasObjContainer["10000"]['eVariant'] = "01"
        self.assertEqual(self.pasObjContainer["10000"]['eVariant'].getDisplay(), 'eEQ_VARIANT_CMSI_A')
        self.pasObjContainer["10000"]['eVariant'] = "02"
        self.assertEqual(self.pasObjContainer["10000"]['eVariant'].getDisplay(), 'eEQ_VARIANT_CMSI_B')
        self.pasObjContainer["10000"]['eVariant'] = "03"
        self.assertEqual(self.pasObjContainer["10000"]['eVariant'].getDisplay(), 'eEQ_VARIANT_ELITE')
        self.pasObjContainer["10000"]['eVariant'] = "04"
        self.assertEqual(self.pasObjContainer["10000"]['eVariant'].getDisplay(), '')


        self.assertEqual(self.pasObjContainer.parseObject("50304"), 'AA BB CCCC DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD EE FF GGGG HHHH IIII JJ KK LL LL LL LL LL LL LL LL LL LL LL LL LL LL LL LL MM MM MM MM MM MM MM MM MM MM MM MM MM MM MM MM NN')


        self.assertDictEqual(self.pasObjContainer["50304"].readData("2B 01 0100 4C0059004E0058002D00540032004F0043004F00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 01 07 0000 0000 0000 06 03 01 01 02 02 02 02 06 07 04 05 00 00 00 00 00 00 04 04 04 04 04 04 0E 0D 0F 00 00 00 00 00 00 00 01"),
        {'sub0': '2B',
        'u8IconeID': '01',
        'eDeviceType': '0100',
        'xDeviceName': '4C0059004E0058002D00540032004F0043004F00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        'eInterruptType': '01',
        'u8ChannelCounter': '07',
        'xFunction_RIDX': '0000',
        'xCommand_RIDX': '0000',
        'xBlock_RIDX': '0000',
        'u8InputCounter': '06',
        'u8OutputCounter': '03',
        'eChannelType': ['01','01','02','02','02','02','06','07','04','05','00','00','00','00','00','00'],
        'eIOType': ['04','04','04','04','04','04','0E','0D','0F','00','00','00','00','00','00','00'],
        'bIsbehaviorUsed': '01'})


        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(0), 'eDDS_CHANNEL_ALGO')
        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(1), 'eDDS_CHANNEL_ALGO')
        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(2), 'eDDS_CHANNEL_ANAI')
        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(3), 'eDDS_CHANNEL_ANAI')
        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(4), 'eDDS_CHANNEL_ANAI')
        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(5), 'eDDS_CHANNEL_ANAI')
        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(6), 'eDDS_CHANNEL_LEDS')
        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(7), 'eDDS_CHANNEL_PSUI')
        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(8), 'eDDS_CHANNEL_GENO')
        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(9), 'eDDS_CHANNEL_NOMO')
        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(10), 'eDDS_CHANNEL_UNDEFINED')
        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(11), 'eDDS_CHANNEL_UNDEFINED')
        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(12), 'eDDS_CHANNEL_UNDEFINED')
        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(13), 'eDDS_CHANNEL_UNDEFINED')
        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(14), 'eDDS_CHANNEL_UNDEFINED')
        self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(15), 'eDDS_CHANNEL_UNDEFINED')
        with self.assertRaises(IndexError):
            self.assertEqual(self.pasObjContainer["50304"]['eChannelType'].getDisplay(16), '')


unittest.main()
