#mysql config
def getDBConfig():
	dbconfig = {}
	dbconfig['host'] = '127.0.0.1'
	dbconfig['user'] = 'root'
	dbconfig['passwd'] = '050184'
	dbconfig['db'] = 'mkrep'
	dbconfig['charset'] = 'utf8'
	
	return dbconfig

#redis config
def getRedisConfig():
	redis = {}
	redis['host'] = '127.0.0.1'
	redis['port'] = 6379
	redis['db'] = 0

	return redis

#mongoDB
def getMongoDB(c):
	db = c.ws_server #mondodb name - ws_server

	return db

#link to file directory
def getFilePath():
	filePath = '/var/www/mkrep/backend/web/ws_uploads' #absolute path to directory with files
	return filePath

#ws port
def getPort():
	port = 8095
	return port