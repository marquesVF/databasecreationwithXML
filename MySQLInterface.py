# Use pip install MySQL-python to install mysql dependencies
# -*- coding: utf-8 -*-
import MySQLdb as MySql
import sys

class MySQLInterface():
	def __init__(self, host, port, user, password):
		self.host = host
		self.port = port
		self.user = user
		self.password = password
		self.database = ""
		self.table = dict()

	def connect(self):
		try:
			self.connection = MySql.connect(host = self.host, user = self.user, passwd = self.password, port = self.port)
			self.connection.query("SELECT VERSION()")
			result = self.connection.use_result()
			return True
		except MySql.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			sys.exit(1)

	def disconnect(self):
		if self.connection:
			self.connection.close()

	def createDatabase(self, databaseName):
		sql = "CREATE DATABASE IF NOT EXISTS "+databaseName+";"
		cursor = self.connection.cursor()
		cursor.execute(sql)
		self.connection.commit()
		self.database = databaseName

		sql = "USE "+self.database+"; "
		cursor = self.connection.cursor()
		cursor.execute(sql)
		self.connection.commit()

	'''
		@table a dictionary with table names and columns information
	'''
	def createTable(self, table):
		if self.connection:
			sql = self.generateSQLTableCreation(table)
			cursor = self.connection.cursor()
			cursor.execute(sql)
			self.connection.commit()

	def insertData(self, data):
		if self.connection:
			sql = self.generateSQLDataInsertion(data)
			return True
		return False

	def generateSQLTableCreation(self, table):
		# save table information for validation of types later on when insert data
		self.table[table["name"]] = dict()
		# +++++++++++++++++++++++
		foreignkeys = list()
		tableName = table["name"]
		sql = "CREATE TABLE "+tableName+" (id INT AUTO_INCREMENT PRIMARY KEY, "
		# Columns value is a list of dictionaries
		for column in table["columns"]:
			columnName = column["name"]
			columnType = self.convertType(column["type"])
			self.table[tableName][columnName] = column["type"]
			sql = sql + " " + columnName+ " "+ columnType+ ","
			if column["type"]=="foreignkey":
				foreignkeys.append({ "name": column["name"], "reference": column["reference"] })
		sql = sql[:len(sql)-1]
		if len(foreignkeys)==0:
			sql = sql + ");"
		else:
			sql = sql + ","
		for key in foreignkeys:
			sql = sql + " FOREIGN KEY ("+key["name"]+") REFERENCES "+key["reference"]+" (id),"
		if len(foreignkeys)>0:
			sql = sql[:len(sql)-1] + ");"
		return sql

	def generateSQLDataInsertion(self, data):
		# print "Inserindo Dados"
		if self.connection:
			# print data
			sql = ""
			for table in data:
				for row in data[table]:
					sql = "INSERT INTO "+table+" ("
					# copy columns name
					for name in data[table][row]:
						sql = sql + name["column"] + " ,"
					sql = sql[:len(sql)-1] + ") values ("		# remove the last comma
					# copy columns values
					for value in data[table][row]:
						sql = sql + self.getTypeConverted(table, value["column"], value["data"]) + " ,"
					sql = sql[:len(sql)-1] + ") ;"
					cursor = self.connection.cursor()
					cursor.execute(sql)
					self.connection.commit()
			return sql

	def getTypeConverted(self, table, column, value):
		if self.table:
			real_type = self.table[table][column]
			if real_type=="string":
				return "'"+value+"'"
			else:
				return value


	def convertType(self, tpe):
		types = {
			"string" : "VARCHAR(255)",
			"integer": "INT",
			"float": "FLOAT",
			"foreignkey": "INT"
		}	
		return types[tpe]
