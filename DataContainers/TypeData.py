
from XMLParsing.XMLParsedTypeInObject import XMLParsedTypeInObject

class TypeData(object):

    def __init__(self, xmlParsedTypeInObject, motherObject): #must be initialized with an ObjectData AND a XMLParsedTypeInObject
        self.xmlParsedTypeInObject = xmlParsedTypeInObject
        self._motherObject = motherObject

    def _get_value(self):
        return self._motherObject.formatedData[self.xmlParsedTypeInObject.nameOfField]

    def _set_value(self, value):
        self._motherObject.modifyData(self.xmlParsedTypeInObject.nameOfField, value)

    value = property(fget=_get_value, fset=_set_value)

    def _get_objectIndex(self):
        return self._motherObject.objectIndex
    objectIndex = property(fget=_get_objectIndex)


    @property
    def nameOfField(self):
        return self.xmlParsedTypeInObject.nameOfField


    @property
    def size(self):
        return self.xmlParsedTypeInObject.size


    @property
    def arraySize(self):
        return self.xmlParsedTypeInObject.arraySize

    @property
    def range_(self):
        return self.xmlParsedTypeInObject.range_


    def __setitem__(self, index, newValue):
        if self.xmlParsedTypeInObject.arraySize > 1:
            self._motherObject.modifyData(self.xmlParsedTypeInObject.nameOfField, newValue, index)
        else:
            raise IndexError("Trying to set data {0} of type {1} but {4} is not an array in object {3}"
                .format(index, self.xmlParsedTypeInObject.typeName, self.xmlParsedTypeInObject.startIndex, self.xmlParsedTypeInObject.nameOfField))

    def __getitem__(self, index):
        dataValue = ""
        if self.xmlParsedTypeInObject.arraySize > 1:
            dataValue = self._motherObject.formatedData[self.xmlParsedTypeInObject.nameOfField][index]
        else:
            raise IndexError("Trying to read data {0} of type {1} but {4} is not an array in object {3}"
                .format(index, self.xmlParsedTypeInObject.typeName, self.xmlParsedTypeInObject.startIndex, self.xmlParsedTypeInObject.nameOfField))
        return dataValue
