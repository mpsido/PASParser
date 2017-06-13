#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PASObject import *
from PASType import *

# print(sys.argv)

# if len(sys.argv) < 2:
#     print("Précisez une action en paramètre")
#     sys.exit(1)

# action = sys.argv[1]
# print (action)

# print(objReader.PASObjectsString)



typeReader = PASTypeReader() 
# print(typeReader.PASTypesString)

objReader = PASObjReader()
spectrum = objReader.parseObject("74000", typeReader)
print(spectrum)
spectrum = objReader.parseObject("10000", typeReader)
print(spectrum)
spectrum = objReader.parseObject("10000", typeReader)
print(spectrum)
spectrum = objReader.parseObject("30092", typeReader)
print(spectrum)

data_30092 = "07 01 5B6C 0000 0000 00 00 00000000000000000001 0000"
data_74000 = "02 00 606D0C006054D052584D50463863580260096400D00764003200640001010104 00A41011301068ABE000"
data_10000 = "1B 01 02 0A 14 0D 09 00 00 00 00 00 00 00 00 00 00 00 00 00 03 000000 0B01010A 010110 000000 000000 000000 000000 000000"
# print(objReader.parsedObjects["30092"].readData(data_30092))
# print(objReader.parsedObjects["74000"].readData(data_74000))
# print(objReader.parsedObjects["10000"].readData(data_10000))

print("\nModify data")
data_10000_modified = objReader.parsedObjects["10000"].modifyData(data_10000, "xEAES_Used", "15")
data_10000_modified = objReader.parsedObjects["10000"].modifyData(data_10000_modified, "eBoard_slot", "12", 4)

print(data_10000)
print(data_10000_modified)