# -- coding: utf-8 --
#work with messages
import redis
import json
import pymysql
import datetime
import time
import random

from Loger import Loger
from Config import Config
from DataBase import MySQL
from DataBase import Mongo

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
	query = "SELECT * FROM `" + data['prefix'] + "csettings` WHERE `employee_id` = " + data['iam']
	cur = MySQL.db_select(query)
	for row in cur:
		res = row
	
	sounds = {}
	if res[9] == 1:
		sounds['sound_mess_on_live'] = res[13]
	if res[10] == 1:
		sounds['sound_comm_on_live'] = res[14]
	if res[11] == 1:
		sounds['sound_like_on_live'] = res[15]
	if res[12] == 1:
		sounds['sound_mess_on_chat'] = res[16]
	
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

def live(data, count_online):
	#print(data)
	message = {}
	message['parent_id'] = data['user_id']
	message['text'] = data['message']
	message['to_id'] = data['adresat']
	message['annexes'] = data['files']
	message['isfile'] = 'false'
	date = time.time()
	message['date'] = date
	new_mess_id = Mongo.insertToMessages(message)
	date_message = datetime.datetime.fromtimestamp(date).strftime('%d %b %Y %H:%M:%S')
	message['id'] = str(message['_id'])
	message['_id'] = ''#str(new_mess_id)
	message['date'] = date_message
	message['like'] = 0
	message['online'] = count_online
	message['type'] = 'live'
	
	return json.dumps(message)

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
	config = Config.getRedisConfig()
	for employee in employees:
		r = redis.StrictRedis(host=config['host'], port=config['port'], db=config['db'])
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
	query = "SELECT * FROM `" + data['prefix'] + "dialogs` WHERE `adresat` = '" + data['user_id'] + "' AND `name` = 'NULL'"
	result = MySQL.db_select(query)
	for row in result:
		print(row)

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

def delmess(data, count_online):
	mess_id = data['id']
	Mongo.deleteMessage(mess_id)

	outmessage = {}
	outmessage['online'] = count_online
	outmessage['msg_id'] = mess_id
	outmessage['type'] = 'delmess'

	return outmessage

def closeChat(data):
	return data

def getEmployeeCache():
	config = Config.getRedisConfig()
	r = redis.StrictRedis(host=config['host'], port=config['port'], db=config['db'])
	result = r.get('employee_id_list')
	return json.loads(result)