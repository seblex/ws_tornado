#mysql config
def getDBConfig(prefix):
	dbconfig = {}
	if(prefix == 'eko_'):
		dbconfig['host'] = '127.0.0.1'
		dbconfig['user'] = 'root'
		dbconfig['passwd'] = '050184'
		dbconfig['db'] = 'mkrep'
		dbconfig['charset'] = 'utf8'
	if(prefix == 'sspb_'):
		dbconfig['host'] = '127.0.0.1'
		dbconfig['user'] = 'root'
		dbconfig['passwd'] = '050184'
		dbconfig['db'] = 'sharikoff'
		dbconfig['charset'] = 'utf8'
	
	return dbconfig

#redis config
def getRedisConfig(prefix):
	redis = {}
	if(prefix == 'eko_'):
		redis['host'] = '127.0.0.1'
		redis['port'] = 6379
		redis['db'] = 0
	if(prefix == 'sspb_'):
		redis['host'] = '127.0.0.1'
		redis['port'] = 6379
		redis['db'] = 0

	return redis

#mongoDB
def getMongoDB(c, prefix):
	if(prefix == 'eko_'):
		db = c.ws_server #mondodb name - ws_server
	if(prefix == 'sspb_'):
		db = c.ws_server_sspb;

	return db

def getMongoAuthInfo(prefix):
	auth_info = {}
	if(prefix == 'eko_'):
		auth_info['user'] = 'admin'
		auth_info['password'] = 'admin'
		auth_info['server'] = '127.0.0.1'
	if(prefix == 'sspb_'):
		auth_info['user'] = 'admin'
		auth_info['password'] = 'admin'
		auth_info['server'] = '127.0.0.1'

	return auth_info

#link to file directory
def getFilePath(prefix):
	if(prefix == 'eko_'):
		filePath = '/var/www/mkrep/backend/web/ws_uploads' #absolute path to directory with files
	if(prefix == 'sspb_'):
		filePath = '/var/www/mkrepcopy2/backend/web/ws_uploads' #absolute path to directory with files

	return filePath

#ws port
def getPort():
	port = 8095
	return port

#SMTP settings
def getSMTPconfig():
	smtp = {}
	smtp['server'] = "smtp.gmail.com"
	smtp['port'] = 25
	smtp['user_name'] = "support.tonics@gmail.com"
	smtp['user_passwd'] = "password"

	return smtp