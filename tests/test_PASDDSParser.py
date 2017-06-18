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
        self.ddsParser = PASDDSParser()
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


#        self.assertEqual(self.ddsParser['PAS_SDO_SEND_DIRECT']['OPT'], "0004")

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




unittest.main()
