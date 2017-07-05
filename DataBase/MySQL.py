import pymysql

#responce SELECT
def db_select(responce):
	conn = pymysql.connect(host='127.0.0.1', user='root', passwd='050184', db='mkrep5', charset='utf8')
	cur = conn.cursor()
	cur.execute(responce)
	#print(cur.description)
	for row in cur:
		print(row)
	cur.close()
	conn.close()

#responce INSERT

#responce UPDATE

#responce DELETE

#get employee_id
def get_employee_id(user_id, prefix):
	conn = pymysql.connect(host='127.0.0.1', user='root', passwd='050184', db='mkrep5', charset='utf8')
	cur = conn.cursor()
	query = "SELECT id FROM " + prefix + "employee WHERE user_id = " + user_id
	cur.execute(query)
	result = cur.fetchone()
	for i in result:
		employee_id = i
	return employee_id
	

