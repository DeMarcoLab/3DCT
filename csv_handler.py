#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Title			: csv_handler
# @Project			: 3DCTv2
# @Description		: Import and export PyQt model data from/to csv fles
# @Author			: Jan Arnold
# @Email			: jan.arnold (at) coraxx.net
# @Credits			:
# @Maintainer		: Jan Arnold
# @Date				: 2015/09
# @Version			: 0.2
# @Status			: stable
# @Usage			: import csv_handler
# 					: e.g. import: >>> model = csv_handler.csv2model('test.csv',delimiter="\t",sniff=False,parent=None)
# 					: e.g. export: >>> csv_handler.model2csv(model,'test.csv',delimiter="\t")
# @Notes			:
# @Python_version	: 2.7.10
# @Last Modified	: 2016/02/10 by jan
# ============================================================================

import csv
from PyQt4 import QtCore, QtGui


## read csv/tsv into pyqt model for display in e.g. QTableView
def csv2model(csv_file_in,delimiter="\t",sniff=False,parent=None):
	def main():
		model = QtGui.QStandardItemModel()
		with open(csv_file_in) as csv_file:
			for row in csv.reader(csv_file, delimiter=delimiter):
				items = [QtGui.QStandardItem(field) for field in row]
				model.appendRow(items)
		return model

	## If sniff is set to true, csv.Sniffer attempts to resolve the correct delimiter
	if sniff is True:
		sniffer = csv.Sniffer()
		## Sniff for delimiter
		with open(csv_file_in) as csv_file:
			dialect = sniffer.sniff(csv_file.read())
		## Decide what to do
		if dialect.delimiter == delimiter:
			return main()
		elif dialect.delimiter is not delimiter and parent is None:
			delimiter = dialect.delimiter
			return main()
		elif dialect.delimiter != delimiter and parent:
			# DIALOG Are you sure the delimter is correct? we detected XXX as the correct delimiter and not YYY
			message = (
				"We detected " + repr(dialect.delimiter) +
				" as the correct delimiter. Are you sure it is " +
				repr(delimiter) +
				" ?\n\nClick yes to use: " +
				repr(delimiter) +
				"\nClick no to use: " +
				repr(dialect.delimiter))
			reply = QtGui.QMessageBox.warning(
				parent, 'Warning', message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			if reply == QtGui.QMessageBox.No:
				## Correct delimiter
				delimiter = dialect.delimiter
				return main()
			else:
				return main()
	else:
		return main()


## write model data to csv/tsv file
def model2csv(model,csv_file_out,delimiter="\t"):
	with open(csv_file_out, "wb") as fileOutput:
		writer = csv.writer(fileOutput, delimiter=delimiter,lineterminator='\n')
		for rowNumber in range(model.rowCount()):
			fields = [
				model.data(model.index(rowNumber, columnNumber), QtCore.Qt.DisplayRole).toString()
				for columnNumber in range(model.columnCount())]
			writer.writerow(fields)

if __name__ == "__main__":
	print(
		r"""Please import me and use me like this:
		e.g. import: >>> model = csv_handler.csv2model('test.csv',delimiter="\t",sniff=False,parent=None)
		e.g. export: >>> csv_handler.model2csv(model,'test.csv',delimiter="\t")""")
