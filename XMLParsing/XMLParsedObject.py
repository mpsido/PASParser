
from XMLParsedTypeInObject import *


class XMLParsedObject():
    """This class is a container for XMLParsedTypeInObject objects, it constructs them and store them"""

    def __init__(self):
        self.fields = [] #list of XMLParsedTypeInObject
        self.spectrum = ""
        self.groupName = ""
        self.objectCount = ''


    @staticmethod
    def paddingString(nextbyteCursor, currentCursor):
        strPadding = ""
        padding = nextbyteCursor - currentCursor
        if padding > 0:
            zeroPadding = "{0:"+"<0{0}s".format(padding*2)+"}"
            strPadding = zeroPadding.format("") + " "
        return strPadding



    def __repr__(self):
        """
        Displays a description of the object parsed in this class
        Exemple object with start_index 0x30092
        Object: 30092
        sub0                    : Type: type_0001 at position 0 to 0 size 1
        u8IndexBoard            : Type: type_0001 at position 1 to 1 size 1
        u16DDSCrc                : Type: type_0115 at position 2 to 3 size 2
        xFirstDeviceConfigRIDX    : Type: type_0176 at position 4 to 5 size 2
        u16DeviceTotal            : Type: type_0003 at position 6 to 7 size 2
        eBackupPower            : Type: type_0154 at position 8 to 8 size 1
        xBatteryConfig            : Type: type_0229 at position 10 to 19 size 10
        u16DurationCmd            : Type: type_0003 at position 20 to 21 size 2
        spectrum :     AA BB CCCC DDDD EEEE FF 00 GGGGGGGGGGGGGGGGGGGG HHHH
        data      :    07 01 5B6C 0000 0000 00 00 00000000000000000001 0000
        """
        description = "Object: {0}\n".format(self.startIndex)
        for index in self.fields:
            if index.arraySize == 1:
                description += "{0}\t\t: Type: {1} at position {2} to {3} size {4}\n"\
                .format(index.nameOfField, index.typeName, index.range_[0], index.range_[1], index.size)
            else:
                description += "{0}\t\t: Array {1} elements of type {2} from {3} to {4} each element has a size: {5}\n"\
                .format(index.nameOfField, index.arraySize, index.typeName, index.range_[0][0], index.range_[index.arraySize - 1][1],
                    index.size)
        description += "spectrum :     {0}\n".format(self.spectrum)
        if bool(self.formatedData):
            description += "data     :     {0}".format(self.writeFormatedData(self.formatedData))
        return description

    def addField(self, nameOfField, start_pos, arraySize, pasType):
        """Adds a field in this parsed object """
        xmlParsedType = XMLParsedTypeInObject()
        xmlParsedType.setInfos(self.startIndex, nameOfField, start_pos, arraySize, pasType)
        self.fields.append(xmlParsedType)

    def nbFields(self):
        return len(self.fields)
