#!python
# -*- coding: utf-8 -*-


import os, sys
# lib_path = os.path.abspath(os.path.join('..', '..', '..', 'lib'))
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
lib_path = os.path.abspath('.')
sys.path.append(lib_path)

import unittest


from DDS.DDSReader import DDSReader
from XMLParsing.XMLObjectReader import XMLObjectReader
from Common.print_debug import *
from Common.PASParsingException import PASParsingException
from DDS.PASDDSParser import PASDDSFileReadingException


class Test_PASDDSParser(unittest.TestCase):
    def setUp(self):
        set_debug_flags(0)
        self.ddsReader = DDSReader()
        self.xmlReader = XMLObjectReader()

    def test_displayValue(self):
        self.ddsReader.parse("ECS-ELITE_1_C-1")

        self.ddsReader.readObject("11002")
        obj11002 = self.ddsReader.getObject("11002")
        self.assertEqual(obj11002['xWindowSession'].getDisplay(), 'mbenthaier')
        self.assertEqual(obj11002['xWindowSession'].convertDisplayToValue('mbenthaier'), '6D00620065006E00740068006100690065007200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

        self.assertEqual(obj11002['xWindowSession'].convertDisplayToValue('coucou'),     '63006F00750063006F0075000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        obj11002['xWindowSession'] = obj11002['xWindowSession'].convertDisplayToValue('coucou')
        self.assertEqual(obj11002['xWindowSession'].getDisplay(), 'coucou')

    def test_dataParsing(self):
        self.ddsReader.parse("ECS-ELITE_1_C-1")

        with self.assertRaises(KeyError):
            self.assertEqual(self.ddsReader.getObject("50508")['sub0'].value, '0D')

        with self.assertRaises(KeyError):
            self.ddsReader.getObject("50508")['eIOType'][0]

        self.ddsReader.readObject("50508")
        self.assertEqual(self.ddsReader.getObject("50508")['eIOType'][0], '00')
        self.assertEqual(self.ddsReader.getObject("50508")['sub0'].value, '0D')

        fieldNames = ['sub0', 'eEquipType', 'u8Number', 'xBaseAddress', 'eBoard_slot', 'xEAES_Used', 'eVariant', 'xSNTPMaster', 'tSubSlotType']
        for j, field in enumerate(self.ddsReader.getObject("10000").fields):
            self.assertEqual(field.nameOfField, fieldNames[j])

        for j, field in enumerate(self.ddsReader.getObject("10000").fields):
            self.ddsReader.getObject("10000")[field.nameOfField]

        self.assertEqual(self.ddsReader.getObject("20000").objectCount, 2048)


    def test_readData(self):
        with self.assertRaises(KeyError):
            self.ddsReader.getObject("10000")

        with self.assertRaises(KeyError):
            self.ddsReader.getObject("74000")

        self.ddsReader.parse("ECS-ELITE_1_C-1")

        self.assertEqual(self.ddsReader.objContainer["10000"].dataString, "")
        self.assertEqual(self.ddsReader.getObject("10000").readData("AA 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 00 03 000000 0B01010A 010110 000000 000000 000000 000000 00000F"),
        {'sub0':'AA',
        'eEquipType':'01',
        'u8Number':'02',
        'xBaseAddress':'0A',
        'eBoard_slot': ['14','0D','09','00','00','00','00','00','00','00','00','00','00','00','00'],
        'xEAES_Used':'00',
        'eVariant':'03',
        'xSNTPMaster':'0B01010A',
        'tSubSlotType':['010110','000000','000000','000000','000000','00000F']})

        self.assertEqual( self.ddsReader.objContainer["10000"].dataString, "AA 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 00 03 000000 0B01010A 010110 000000 000000 000000 000000 00000F")

        with self.assertRaises(PASDDSFileReadingException) as exception:
            #writing an invalid data
            self.ddsReader.setDataInObject("10000","ACA 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 00 03 000000 0B01010A 010110 000000 000000 000000 0000 00000F")
            self.assertEqual(exception.message, "Data is invalid :\nDATA     = ACA 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 00 03 000000 0B01010A 010110 000000 000000 000000 0000 00000F\nSPECTRUM = AA BB CC DD EE EE EE EE EE EE EE EE EE EE EE EE EE EE EE FF GG 000000 HHHHHHHH IIIIII IIIIII IIIIII IIIIII IIIIII IIIIII")


        self.assertEqual(self.ddsReader.objContainer["10000"].dataString, "AA 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 00 03 000000 0B01010A 010110 000000 000000 000000 000000 00000F")

        self.ddsReader.readObject("10000")

        self.assertEqual(self.ddsReader.objContainer["10000"].dataString, "1B 01 01 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 00 03 000000 0B01010A 010110 000000 000000 000000 000000 000000")

        self.assertEqual( self.ddsReader.objContainer["74000"].spectrum
        , "AA 00 BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB CCCCCCCCCCCCCCCCCCCC")


        self.assertEqual( self.ddsReader.getObject("74000").dataString, "")


        self.assertEqual( self.ddsReader.getObject("93000").dataString, "")
        self.assertEqual( self.ddsReader.getObject("93001").dataString, "")

        self.ddsReader.readObject("93001")

        self.assertEqual( self.ddsReader.getObject("93000").dataString, "")
        self.assertEqual( self.ddsReader.getObject("93001").dataString, "05 01 02 00 4D00340045005600410043005F0031005F004500430053002D0045004C004900540045005F0031005F0043002D0031000000000000000000000000000000000000000000000000000000000000000000 4D0034004500560041004300000000000000")

        self.ddsReader.readObject("93000")
        self.assertEqual( self.ddsReader.getObject("93000").dataString, "05 01 01 00 4D00500045005F0031005F004500430053002D0045004C004900540045005F0031005F0043002D0031000000000000000000000000000000000000000000000000000000000000000000000000000000 4D0050004500000000000000000000000000")
        self.assertEqual( self.ddsReader.getObject("93001").dataString, "05 01 02 00 4D00340045005600410043005F0031005F004500430053002D0045004C004900540045005F0031005F0043002D0031000000000000000000000000000000000000000000000000000000000000000000 4D0034004500560041004300000000000000")


    def test_fileList(self):

        with self.assertRaises(PASParsingException) as exception:
            self.ddsReader.parse("qsdffsdq")
            self.assertEqual(exception.message, "DDS.DDSReader : invalid path: qsdffsdq")

        self.ddsReader.parse("ECS-ELITE_1_C-1")

        self.assertEqual(self.ddsReader.path, "ECS-ELITE_1_C-1")
        self.assertListEqual(self.ddsReader.getObjectIds(), ['10000',
        '10010',
        '11000', '11001', '11002',
        '12000',
        '12010',
        '13003',
        '20000', '20001', '20002', '20003', '20004', '21000', '21001', '21002', '21003',
        '24000', '24001', '24002', '24003',
        '27000', '27001', '27002', '27003', '27004', '27005', '27006',
        '30092',
        '50200', '50201',
        '50300', '50301', '50302', '50303', '50304', '50305', '50306', '50307', '50308', '50309', '5030a', '5030b', '5030c', '5030d', '5030e', '50311', '50312', '50314', '50315', '50316',
        '50500', '50501', '50502', '50503', '50504', '50505', '50506', '50507', '50508', '50509', '5050a', '5050b', '5050c', '5050d', '5050e', '5050f', '50510', '50511', '50512', '50513', '50514', '50515', '50516', '50517', '50518', '50519', '5051a', '5051b', '5051c', '5051d', '5051e', '5051f', '50520', '50521', '50522',
        '51000', '51001',
        '55000', '55001',
        '66000', '66001', '66002', '66003', '66004', '66005', '66006', '66007',
        '70011', '71700', '71701', '71702', '71703', '71704', '71705', '71706', '71707', '71708', '71709', '7170a', '7170b', '7170c', '7170d', '7170e', '71711', '71712', '71714', '71715', '71716',
        '71900', '71901', '71902', '71903', '71904', '71905', '71906', '71907', '71908', '71909', '7190a', '7190b', '7190c', '7190d', '7190e', '71911', '71912', '71914', '71915', '71916',
        '71b00', '71b01', '71b02', '71b03', '71b04', '71b05', '71b06', '71b07', '71b08', '71b09', '71b0a', '71b0b', '71b0c', '71b0d', '71b0e', '71b11', '71b12', '71b14', '71b15', '71b16',
        '74000',
        '74010',
        '74100',
        '74310',
        '76000', '76001',
        '90000', '90001', '90002', '90003',
        '92000', '92001', '92002', '92003', '92004', '92005',
        '93000', '93001', '93002']
        )

        for id in self.ddsReader.getObjectIds():
            self.assertTrue(self.xmlReader.objectExist(id))




unittest.main()
