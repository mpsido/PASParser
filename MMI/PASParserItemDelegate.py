
from Common.print_debug import *

from PyQt4.QtGui import QStyledItemDelegate, QComboBox
from PyQt4.QtCore import QModelIndex

from PASParserTreeModel import *
from MMI.PASObjectNode import *

class PASParserItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(PASParserItemDelegate, self).__init__(parent)


    def createEditor(self, parentWidget, option, index):
        #check QItemEditorFactory for help

        if index.isValid():
            sourceIndex = self.proxyModel.mapToSource(index)
            pasType = self.sourceModel.nodeFromIndex(sourceIndex).pasTypeOrObject
            print_debug("PASParserItemDelegate.createEditor objectIndex = {0}".format(pasType.objectIndex), DEBUG_MMI)
            print_debug("PASParserItemDelegate.createEditor nameOfField = {0}".format(pasType.nameOfField), DEBUG_MMI)
            print_debug("PASParserItemDelegate.createEditor typeName    = {0}".format(pasType.typeName), DEBUG_MMI)
            print_debug("PASParserItemDelegate.createEditor cat         = {0}".format(pasType.cat), DEBUG_MMI)

            if pasType.cat == "enum":
                comboBox = QComboBox(parentWidget)
                for enumField in pasType.enumFields:
                    comboBox.addItem(enumField)
                if pasType.arraySize == 1:
                    comboBox.setCurrentIndex(int(pasType.value))
                else:
                    comboBox.setCurrentIndex(int(pasType.value[sourceIndex.row()]))

                return comboBox
            else:
                return super(PASParserItemDelegate, self).createEditor(parentWidget, option, index)


    def setEditorData(self, editor, index):
        sourceIndex = self.proxyModel.mapToSource(index)
        pasType = self.sourceModel.nodeFromIndex(sourceIndex).pasTypeOrObject
        print_debug("PASParserItemDelegate.setEditorData cat         = {0}".format(pasType.cat), DEBUG_MMI)
#        if pasType.cat == "enum" and pasType.arraySize == 1:
#            editor.setCurrentIndex(int(pasType.value))
#        else:
#            super(PASParserItemDelegate, self).setEditorData(editor, index)
        super(PASParserItemDelegate, self).setEditorData(editor, index)

    def setModelData(self, model, index):
        return super(PASParserItemDelegate, self).setModelData(model, index)
