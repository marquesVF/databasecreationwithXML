from MySQLInterface import *

class DataBaseFacade():

	MYSQL = "mysql"

	'''
		Inform database information to enable connection
		@name name of the DataBaseManager Interface choosed

		+++++

		The processes of table creation is separated from data insertion
	'''
	def __init__(self, name, host, port, user, password):
		if(name==self.MYSQL):
			self.dbInterface = MySQLInterface(host,port, user, password)

	def testConnection(self):
		if(self.dbInterface.connect()):
			self.dbInterface.disconnect()
			return True
		return False

	def createDatabase(self, databaseName):
		if self.dbInterface.connect():
			self.dbInterface.createDatabase(databaseName)
			return True
		return False

	'''
		Used to tables creation
	'''
	def createTables(self, tables):
		for t in tables:
			self.dbInterface.createTable(t)
		return True

	'''
		Used to data insertion
	'''
	def insertData(self, tablesData):
		rows = dict()
		for d in tablesData:
			if not d["tablename"] in rows:
				rows[d["tablename"]] = dict()
			if not d["rownumber"] in rows[d["tablename"]]:
				rows[d["tablename"]][d["rownumber"]] = list()
			rows[d["tablename"]][d["rownumber"]].append( { "column" : d["columnname"] , "data" : d["columndata"] } )
		if self.dbInterface.insertData(rows):
			return True
		return False

	def closeConnection(self):
		self.dbInterface.disconnect()