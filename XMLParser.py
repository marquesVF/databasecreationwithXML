# -*- coding: utf-8 -*-
from xml.etree import ElementTree

class XMLParser():

	'''
		This class is responsable to extract informations from a xml file representing a data base structure
		with some data (optional)

		@filename xml file name
	'''
	def __init__(self, fileName):
		self.file = fileName
		self.databaseName = ""

		self.rows = list()
		self.tables = list()

	'''
		Load and store the xml tree structure
	'''
	def parse(self):
		with open(self.file, 'rt') as f:
			self.tree = ElementTree.parse(f)

	'''
		Used to generate a structure with table and data informations to be processed and inserted
	'''
	def generate(self):
		self.databaseName = self.tree.getroot().attrib["name"]
		if self.tree:
			# tables data to be used in tables creation
			tables = list()
			# rows data to be inserted after tables creation
			rows = list()
			for table in self.tree.findall('.//table'):
				t = dict()
				table_info = table.attrib
				# add table name
				t["name"] =  table_info["name"]
				# add table dependecies if it has one
				if "dependencies" in table_info:
					t["dependencies"] =  table_info["dependencies"].split()
				column_data = list()
				row_number = 0
				for column in table.findall(".//column"):
					c = dict()
					column_info = column.attrib
					c["name"] = column_info["name"]
					c["type"] = column_info["type"]
					if "reference" in column_info:
						c["reference"] = column_info["reference"]
					column_data.append(c)
					#
					row_number = 0
					for row in column.findall(".//row"):
						r = dict()	# row info
						r["tablename"] = table_info["name"]
						r["columnname"] = column_info["name"]
						r["columndata"] = row.text
						r["rownumber"] = row_number
						rows.append(r)
						row_number = row_number + 1
				# add rows 
				t["columns"] = column_data
				tables.append(t)
			self.tables = tables
			self.rows = rows
			# # DEBUG
			# print "Tables"
			# for t in tables:
			# 	print t
			# print "Data"
			# for r in rows:
			# 	print r

	def getTablesInfo(self):
		return self.tables

	def getTablesData(self):
		return self.rows
				
	def getDatabaseName(self):
		return self.databaseName
