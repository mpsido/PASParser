#!python
# -*- coding: utf-8 -*-

import os, sys
# lib_path = os.path.abspath(os.path.join('..', '..', '..', 'lib'))
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
lib_path = os.path.abspath('.')
sys.path.append(lib_path)

import unittest

from PASDDSParser import *
from PASObjReader import *

class Test_PASDDSParser(unittest.TestCase):
    def setUp(self):
        self.ddsParser = PASDDSObjectParser()
        self.objReader = PASObjReader()

    def test_readFile(self):
        with self.assertRaises(PASDDSFileReadingException) as exception:
            self.ddsParser.open("qsdfq")
            self.assertNotEqual(exception.message, "aef is not a valid file path")
            self.assertEqual(exception.message, "qsdfq is not a valid file path")

        with self.assertRaises(PASDDSFileReadingException) as exception:
            self.ddsParser.open("tests/files/invalid_dds_file")
            self.assertEqual(exception.message, "Apparently file tests/files/invalid_dds_file is not a dds object file")
            self.assertEqual(self.ddsParser.fileName, "")

        self.ddsParser.open("tests/files/74000")
        self.assertEqual(self.ddsParser.fileName, "74000")
        self.assertEqual(self.ddsParser.filePath, "tests/files/74000")

        self.assertListEqual(self.ddsParser.iniBlockNames, ['[ENTETE]', '[MPE_PARAMETERS]', '[PAS_OD_WRITE]', '[PAS_SDO_SEND_DIRECT]',
        '[PAS_PDO_SEND]', '[PAS_SDO_SEND_DIRECT]'])

        self.assertEqual(len(self.ddsParser.iniBlockTexts), len(self.ddsParser.iniBlockNames) )



    def test_data74000(self):
        self.ddsParser.parse("tests/files","74000")
        data_74000 = self.ddsParser.getData()
        self.assertEqual(data_74000,
            '02 00 606D0C006054D052584D50463863580260096400D00764006400F40101010104 00A41011301068ABE000')

        self.objReader["74000"].readData(data_74000)
        data_74000_modified = self.objReader["74000"].modifyData("sub0", "04")

        self.ddsParser.setData(data_74000_modified)

        data_74000 = self.ddsParser.getData()
        self.assertEqual(data_74000,
            '04 00 606D0C006054D052584D50463863580260096400D00764006400F40101010104 00A41011301068ABE000')

        with  self.assertRaises(PASDDSFileReadingException) as exception:
            wrong_data = "0201AF"
            self.ddsParser.setData(wrong_data)

        data_74000 = self.ddsParser.getData()
        self.assertEqual(data_74000,
            '04 00 606D0C006054D052584D50463863580260096400D00764006400F40101010104 00A41011301068ABE000')


        #write in file
        self.ddsParser.write()

        #read file and test modification was written
        self.ddsParser.parse("tests/files","74000")
        data_74000 = self.ddsParser.getData()
        self.assertEqual(data_74000,
            '04 00 606D0C006054D052584D50463863580260096400D00764006400F40101010104 00A41011301068ABE000')

        #remodify data
        data_74000_modified = self.objReader["74000"].modifyData("sub0", "02")
        self.ddsParser.setData(data_74000_modified)
        data_74000 = self.ddsParser.getData()
        self.assertEqual(data_74000,
            '02 00 606D0C006054D052584D50463863580260096400D00764006400F40101010104 00A41011301068ABE000')

        #rewrite file
        self.ddsParser.write()

        #reread and test data is back to normal
        self.ddsParser.parse("tests/files","74000")
        data_74000 = self.ddsParser.getData()
        self.assertEqual(data_74000,
            '02 00 606D0C006054D052584D50463863580260096400D00764006400F40101010104 00A41011301068ABE000')


    def tests_data20000_manyIds(self):
        self.ddsParser.parse("tests/files","20000")
        self.assertEqual(self.ddsParser.nbDataId(), 5)

        data_0 = self.ddsParser.getData()
        self.assertEqual(data_0, "0D 03 0000 40 00 0000 0000 0000 00 00 00 00 0000 0000")

        data_1 = self.ddsParser.getData(1)
        self.assertEqual(data_1, "0D 03 0100 40 00 0000 0000 0000 02 00 00 00 0000 0000")

        data_2 = self.ddsParser.getData(2)
        self.assertEqual(data_2, "0D 00 0200 48 00 0000 2C01 0000 00 00 00 00 0000 0000")

        data_3 = self.ddsParser.getData(3)
        self.assertEqual(data_3, "0D 00 0300 48 00 0000 2C01 0000 00 00 00 00 0000 0000")

        data_4 = self.ddsParser.getData(4)
        self.assertEqual(data_4, "0D 06 0400 48 00 0000 0000 0000 08 00 00 00 0000 0000")

        with self.assertRaises(IndexError) as exception:
            data_5 = self.ddsParser.getData(5)

        data_added = "MOUHAHAH"
        self.ddsParser.insertDataId(data_added, 2)

        self.assertEqual(self.ddsParser.nbDataId(), 6)

        data_0 = self.ddsParser.getData(0)
        self.assertEqual(data_0, "0D 03 0000 40 00 0000 0000 0000 00 00 00 00 0000 0000")

        data_1 = self.ddsParser.getData(1)
        self.assertEqual(data_1, "0D 03 0100 40 00 0000 0000 0000 02 00 00 00 0000 0000")

        data_2 = self.ddsParser.getData(2)
        self.assertEqual(data_2, "MOUHAHAH")

        data_3 = self.ddsParser.getData(3)
        self.assertEqual(data_3, "0D 00 0200 48 00 0000 2C01 0000 00 00 00 00 0000 0000")

        data_4 = self.ddsParser.getData(4)
        self.assertEqual(data_4, "0D 00 0300 48 00 0000 2C01 0000 00 00 00 00 0000 0000")

        data_5 = self.ddsParser.getData(5)
        self.assertEqual(data_5, "0D 06 0400 48 00 0000 0000 0000 08 00 00 00 0000 0000")


        with self.assertRaises(IndexError) as exception:
            self.ddsParser.getData(6)

        self.ddsParser.removeDataId(0)
        self.assertEqual(self.ddsParser.nbDataId(), 5)


        data_0 = self.ddsParser.getData(0)
        self.assertEqual(data_0, "0D 03 0100 40 00 0000 0000 0000 02 00 00 00 0000 0000")

        data_1 = self.ddsParser.getData(1)
        self.assertEqual(data_1, "MOUHAHAH")

        data_2 = self.ddsParser.getData(2)
        self.assertEqual(data_2, "0D 00 0200 48 00 0000 2C01 0000 00 00 00 00 0000 0000")

        data_3 = self.ddsParser.getData(3)
        self.assertEqual(data_3, "0D 00 0300 48 00 0000 2C01 0000 00 00 00 00 0000 0000")

        data_4 = self.ddsParser.getData(4)
        self.assertEqual(data_4, "0D 06 0400 48 00 0000 0000 0000 08 00 00 00 0000 0000")


        with self.assertRaises(IndexError) as exception:
            self.ddsParser.getData(5)




unittest.main()
