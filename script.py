'''
	Author: Vinicius de Figueiredo Marques

	++++++++++++++++++++++++++++++++++++++

	The objective of this script is to load a XML file representing a database structure with some data.
	Then it process this structure and generates SQL instructions to be inserted to a choosen SGBD

'''

from XMLParser import *
from DataBaseFacade import *
from ConfigParser import *

# Load input and database file information
parameters = sys.argv[1:]
if(len(parameters)<2):
	print "Error! You must pass two parameters: the first one should be the input file and second one should be a database info(host, user, password, port) json file"
	sys.exit(1)
for i in range(len(parameters)):
	if i == 0:	# input
		fileInput = parameters[i]
	if i == 1:	# database file information
		config = ConfigParser(parameters[i])

db = DataBaseFacade(name = DataBaseFacade.MYSQL,host = config.host(), user = config.user(), password = config.password(), port = config.port())

x = XMLParser(fileInput)
x.parse()
x.generate()
tablesInfo = x.getTablesInfo();
tablesData = x.getTablesData();

if db.createDatabase(x.getDatabaseName()):
	print "++++	Database Created Sucefully ++++"
if db.createTables(tablesInfo):
	print "++++ Tables Created Sucefully ++++"
if db.insertData(tablesData):
	print "++++ Data Inserted Sucefully ++++"
db.closeConnection()
