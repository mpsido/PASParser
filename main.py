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
print(objReader.parsedObjects["10000"])