# mysql config
def getDBConfig():
	dbconfig = {}
	dbconfig['host'] = '127.0.0.1'
	dbconfig['user'] = 'root'
	dbconfig['passwd'] = 'p2ssw0rd'
	dbconfig['db'] = 'mkrep'
	dbconfig['charset'] = 'utf8'
	
	return dbconfig

# redis config
def getRedisConfig():
	redis = {}
	redis['host'] = '127.0.0.1'
	redis['port'] = 6379
	redis['db'] = 0

	return redis

# mongoDB
def getMongoDB(c):
	db = c.ws_server  # mondodb name - ws_server

	return db

def getMongoAuthInfo():
	auth_info = {}
	auth_info['user'] = 'admin'
	auth_info['password'] = 'admin'
	auth_info['server'] = '127.0.0.1'

	return auth_info

# link to file directory
def getFilePath():
	filePath = '/var/www/mkrep/backend/web/uploads'  # absolute path to directory with files
	return filePath


# ws port
def getPort():
	port = 8095
	return port


# SMTP settings
def getSMTPconfig():
	smtp = {}
	smtp['server'] = "smtp.gmail.com"
	smtp['port'] = 25
	smtp['user_name'] = "support.tonics@gmail.com"
	smtp['user_passwd'] = "password"

	return smtp
