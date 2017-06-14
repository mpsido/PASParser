#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import QT_TR_NOOP as tr


class PASObjectNode(object):
	def __init__(self, name, range_, size, nb_elements, value, parent=None):

		self.name = name
		self.range_ = range_
		self.size = size
		self.nb_elements = nb_elements
		self.value = value

		self.parent = parent
		self.children = []

		self.setParent(parent)

	def setParent(self, parent):
		if parent != None:
			self.parent = parent
			self.parent.appendChild(self)
		else:
			self.parent = None

	def appendChild(self, child):
		self.children.append(child)

	def childAtRow(self, row):
		return self.children[row]

	def rowOfChild(self, child):
		for i, item in enumerate(self.children):
			if item == child:
				return i
		return -1

	def removeChild(self, row):
		value = self.children[row]
		self.children.remove(value)

		return True

	def __len__(self):
		return len(self.children)

class PASParserTreeModel(QAbstractItemModel):

	def __init__(self, parent=None):
		super(PASParserTreeModel, self).__init__(parent)

		self.treeView = parent
		self.headers = [tr('Name'),tr('Range'),tr('Size'), tr('Nb elements'), tr('Value')]

		self.nbColumns = 5

		# Create root item
		self.root = PASObjectNode('', '', '', '', '', None)


	def flags(self, index):
		defaultFlags = QAbstractItemModel.flags(self, index)
		return defaultFlags

	def headerData(self, section, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return QVariant(self.headers[section])
		return QVariant()

	def insertRow(self, row, parent):
		return self.insertRows(row, 1, parent)


	def insertRows(self, row, count, parent):
		self.beginInsertRows(parent, row, (row + (count - 1)))
		self.endInsertRows()
		return True


	def removeRow(self, row, parentIndex):
		return self.removeRows(row, 1, parentIndex)


	def removeRows(self, row, count, parentIndex):
		self.beginRemoveRows(parentIndex, row, row)
		node = self.nodeFromIndex(parentIndex)
		node.removeChild(row)
		self.endRemoveRows()

		return True


	def index(self, row, column, parent):
		node = self.nodeFromIndex(parent)
		return self.createIndex(row, column, node.childAtRow(row))


	def data(self, index, role):
		if role == Qt.DecorationRole:
			return QVariant()

		if role == Qt.TextAlignmentRole:
			return QVariant(int(Qt.AlignTop | Qt.AlignLeft))

		if role != Qt.DisplayRole:
			return QVariant()

		node = self.nodeFromIndex(index)

		if index.column() == 0:
			return QVariant(node.name)
		elif index.column() == 1:
			return QVariant(node.range_)
		elif index.column() == 2:
			return QVariant(node.size)
		elif index.column() == 3:
			return QVariant(node.nb_elements)
		elif index.column() == 4:
			return QVariant(node.value)
		else:
			return QVariant()


	def columnCount(self, parent):
		return self.nbColumns


	def rowCount(self, parent):
		node = self.nodeFromIndex(parent)
		if node is None:
			return 0
		return len(node)


	def parent(self, child):
		if not child.isValid():
			return QModelIndex()

		node = self.nodeFromIndex(child)

		if node is None:
			return QModelIndex()

		parent = node.parent

		if parent is None:
			return QModelIndex()

		grandparent = parent.parent
		if grandparent is None:
			return QModelIndex()
		row = grandparent.rowOfChild(parent)

		assert row != - 1
		return self.createIndex(row, 0, parent)

	def isChildOfRoot(self, index):
		return self.parent(index) == QModelIndex()

	def nodeFromIndex(self, index):
		return index.internalPointer() if index.isValid() else self.root

	def changeData(self, index):
		self.dataChanged.emit(index, index)

