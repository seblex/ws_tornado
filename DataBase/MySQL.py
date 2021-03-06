import pymysql

from Config import Config

#responce SELECT
def db_select(responce, prefix):
	config = Config.getDBConfig(prefix)
	conn = pymysql.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'], charset=config['charset'])
	cur = conn.cursor()
	cur.execute(responce)
	result = []
	for row in cur:
		result.append(row)
	cur.close()
	conn.close()

	return result

#get employee_id
def get_employee_id(user_id, prefix):
	config = Config.getDBConfig(prefix)
	conn = pymysql.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'], charset=config['charset'])
	cur = conn.cursor()
	query = "SELECT id FROM " + prefix + "employee WHERE user_id = " + user_id
	cur.execute(query)
	result = cur.fetchone()
	for i in result:
		employee_id = i
	return employee_id
	

