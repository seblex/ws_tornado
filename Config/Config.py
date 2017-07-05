def getDBConfig():
	dbconfig = {}
	dbconfig['host'] = '127.0.0.1'
	dbconfig['user'] = 'root'
	dbconfig['passwd'] = '050184'
	dbconfig['db'] = 'mkrep5'
	dbconfig['charset'] = 'utf8'
	
	return dbconfig

def getRedisConfig():
	redis = {}
	redis['host'] = '127.0.0.1'
	redis['port'] = 6379
	redis['db'] = 0

	return redis