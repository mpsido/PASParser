import os,re
from Common.PASParsingException import PASParsingException
from DataContainers.ObjectDataContainer import ObjectDataContainer
from DDS.PASDDSParser import PASDDSParser

class DDSReader:
    def __init__(self):
        self.ddsParser = PASDDSParser()
        self.objContainer = ObjectDataContainer()
        self.path = ''
        self._objectIds = []


    def getObjectIds(self):
        return self._objectIds


    def parse(self,  path):

        if os.path.isdir(path) == False:
            raise PASParsingException("DDS.DDSReader : invalid path: {0}".format(path))


        indexes = filter(lambda x: re.match(r'^[0-9A-Fa-f]+$', x), os.listdir(path))

        if len(indexes) == 0:
            raise PASParsingException("DDS.DDSReader : no valid DDS file at path: {0}".format(path))

        self.path = path
        for index in indexes:
            self.ddsParser.parse(path, index)
            for i in range(0, self.ddsParser.getNbObjects(index)):
                id = self.ddsParser.getId(index, i)
                self.objContainer.parseObject( id )
                self._objectIds.append(id)


