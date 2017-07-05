#work with messages
import redis
import json
import pymysql

#responce 'ping'
def ping(data):
	responce = {}
	responce['text'] = 'pong'
	responce['type'] = 'ping'

	return responce

def viewed_messages(data):
	return data

def annexesfiles(data):
	return data

def filelive(data):
	return data

def file(data):
	return data

def type_message(data):
	return data

def new_message(data):
	return data

def sounds(data):
	conn = pymysql.connect(host='127.0.0.1', user='root', passwd='050184', db='mkrep5', charset='utf8')
	cur = conn.cursor()
	query = "SELECT * FROM `" + data['prefix'] + "csettings` WHERE `employee_id` = " + data['iam']
	cur.execute(query)
	
	for row in cur:
		res = row
	
	cur.close()
	conn.close()

	sounds = {}
	if res[9] == 1:
		sounds['sound_mess_on_live'] = res[13]
	if res[10] == 1:
		sounds['sound_comm_on_live'] = res[14]
	if res[11] == 1:
		sounds['sound_like_on_live'] = res[15]
	if res[12] == 1:
		sounds['sound_mess_on_chat'] = res[16]
	#for ind in res:
	responce = {}
	responce['type'] = 'sounds'
	responce['sounds'] = sounds

	return responce

def sound(data):
	return data

def online(data, count_online):
	responce = {}
	responce['online'] = count_online
	responce['type'] = 'online'
	
	return responce

def live(data):
	return data

def comment(data):
	return data

def likemess(data):
	return data

def likecomm(data):
	return data

def showComments(data):
	return data

def dialog(data):
	return data

def mess(data):
	return data

def allusers(data):
	employees = getEmployeeCache()
	all_employees = []
	for employee in employees:
		r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
		result_e = json.loads(r.hget('employee', employee))
		all_employees.append(result_e)
	
	usr = []
	subdivisions = {}
	count_users = 0

	for emp in all_employees:
		if emp['user_id'] != 1:
			arr = {}
			arr['id'] = emp['id']
			arr['avatar'] = emp['avatar']
			arr['username'] = emp['firstname'] + ' ' + emp['lastname']
			usr.append(arr)
			count_users += 1

	count_cols = count_users / 3
	start_cols = 1
	start_cols_1 = 1
	start_cols_2 = (count_users / 3) + 1
	start_cols_3 = ((count_users/3) * 2) + 1

	user_cols_1 = []
	user_cols_2 = []
	user_cols_3 = []

	for user in usr:
		if start_cols < start_cols_2:
			user_cols_1.append(user)
		if start_cols < start_cols_3:
			if start_cols >= start_cols_2:
				user_cols_2.append(user)
		if start_cols >= start_cols_3:
			user_cols_3.append(user)
		start_cols += 1
	
	responce = {}
	responce['type'] = 'allusers'
	responce['users'] = usr
	responce['users_1'] = user_cols_1
	responce['users_2'] = user_cols_2
	responce['users_3'] = user_cols_3
	responce['count_users'] = count_users

	return responce

def alldialogs(data):
	conn = pymysql.connect(host='127.0.0.1', user='root', passwd='050184', db='mkrep5', charset='utf8')
	cur = conn.cursor()
	query = "SELECT * FROM `" + data['prefix'] + "dialogs` WHERE `adresat` = '" + data['user_id'] + "' AND `name` = 'NULL'"
	#print query
	cur.execute(query)
	#print(cur.description)
	for row in cur:
		print(row)

	cur.close()
	conn.close()
	#return data

def notice(data):
	return data

def onlineNotice(data):
	return data

def offer(data):
	return data

def answer(data):
	return data

def ice1(data):
	return data

def ice2(data):
	return data

def hangup(data):
	return data

def dopmess(data):
	return data

def delComm(data):
	return data

def delmess(data):
	return data

def closeChat(data):
	return data

def getEmployeeCache():
	r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
	result = r.get('employee_id_list')
	return json.loads(result)