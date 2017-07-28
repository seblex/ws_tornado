# -- coding: utf-8 --
#work with messages
import redis
import json
import pymysql
import datetime
import time
import random
import os
import base64

from Loger import Loger
from Config import Config
from DataBase import MySQL
from DataBase import Mongo
from Notices import Notices

#responce 'ping'
def ping(data):
	responce = {}
	responce['text'] = 'pong'
	responce['type'] = 'ping'
	
	return responce

def viewed_messages(data):
	return data

def annexesfiles(data):
	absp = Config.getFilePath()
	if (os.path.exists(absp) == False):
		os.mkdir(absp)
	file = data['file'].split('base64');
	filetext = file[1]
	filetext1 = base64.b64decode(filetext)
	path_to_file = absp + '/' + data['fileName'] 
	if (os.path.exists(path_to_file) == False):
		f = open(path_to_file, 'w')
		f.write(filetext1)
		f.close()
		#print('OK')

def filelive(data):
	absp = Config.getFilePath()
	if (os.path.exists(absp) == False):
		os.mkdir(absp)
	file = data['file'].split('base64');
	mime = (file[0].split(':'))[1]
	mimes = ['image/jpeg;', 'image/jpg;', 'image/png;']
	for mm in mimes:
		if (mm == mime):
			filetext = file[1]
			filetext1 = base64.b64decode(filetext)
			path_to_file = absp + '/' + data['fileName'] 
			if (os.path.exists(path_to_file) == False):
				f = open(path_to_file, 'w')
				f.write(filetext1)
				f.close()
				#print('OK')
			_id = Mongo.setFileMessage(data)

			message = {}
			message['text'] = data['fileName']
			message['parent_id'] = data['user_id']
			message['to_id'] = data['adresat']
			message['date'] = time.time()
			message['like'] = 0
			message['isfile'] = 'true'
			message['files'] = ''
			message['id'] = _id
			
			outmessage = {}
			outmessage['user'] = data['user_id']
			outmessage['type'] = 'filelive'
			outmessage['messages'] = message
			
			return outmessage	

def file(data, count_online):
	absp = Config.getFilePath()
	if (os.path.exists(absp) == False):
		os.mkdir(absp)
	file = data['file'].split('base64');
	mime = (file[0].split(':'))[1]
	#TO DO - add some formats
	mimes = ['image/jpeg;', 'image/jpg;', 'image/png;']
	#for mm in mimes:
	#	if (mm == mime):
	filetext = file[1]
	filetext1 = base64.b64decode(filetext)
	path_to_file = absp + '/' + data['fileName'] 
	if (os.path.exists(path_to_file) == False):
		f = open(path_to_file, 'w')
		f.write(filetext1)
		f.close()
				
	_id = Mongo.setFileMessageFromChat(data)
			
	outmessage = {}
	outmessage['user'] = data['user_id']
	outmessage['type'] = 'file'
	outmessage['fileName'] = data['fileName']
	outmessage['parent'] = data['user_id']
	outmessage['url'] = '/ws_uploads/' + data['fileName']
			
	return outmessage

def type_message(data):

	outmessage = {}

	outmessage['type'] = data['type']
	outmessage['event'] = data['event']
	outmessage['user'] = data['iam']
	outmessage['adresat'] = data['adresaten']

	return outmessage

def new_message(data):

	Mongo.setNewChatMessage(data)

	outmessage = {}
	outmessage['date'] = time.time()
	outmessage['day'] = 'Сегодня'
	outmessage['text'] = data['message']
	outmessage['parent'] = data['user_id']
	outmessage['user'] = data['user_id']
	outmessage['type'] = 'new_message'

	return outmessage

def setDialog(data):
	Mongo.setDialog(data)
	
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
	outmessage = {}
	outmessage['type'] = data['type']
	outmessage['sound_event'] = data['sound_event']

	return outmessage

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
	message['like'] = 0
	new_mess_id = Mongo.insertToMessages(message)
	message['id'] = str(message['_id'])
	message['_id'] = ''
	message['date'] = date
	message['like'] = message['like']
	message['online'] = count_online
	message['type'] = 'live'

	return json.dumps(message)

def first_messages(data, count_online):
	messages = Mongo.getFirstMessages()

	outmessages = []
	for mess in messages:
		message = {}
		message['text'] = mess['text']
		message['to_id'] = mess['to_id']
		message['parent_id'] = mess['parent_id']
		message['date'] = mess['date']
		message['id'] = str(mess['_id'])
		message['isfile'] = mess['isfile']
		message['annexes'] = mess['annexes']
		message['like'] = mess['like']
		outmessages.append(message)
	count_messages = Mongo.getCountAllMessages()
	outmessage = {}
	outmessage['type'] = 'firstMessages'
	outmessage['count_online'] = count_online
	outmessage['messages'] = outmessages
	outmessage['count'] = count_messages
			
	return outmessage

def comment(data, count_online):

	coll = {}
	coll['text'] = data['message']
	coll['parent_id'] = data['user_id']
	coll['msg_id'] = data['message_id']
	coll['date'] = time.time()
	coll['like'] = 0

	Mongo.insertNewComment(coll)

	comments = Mongo.getComments(data['message_id'])

	comm = []
	for comment in comments:
		c = {}
		c['id'] = str(comment['_id'])
		c['text'] = comment['text']
		c['parent_id'] = comment['parent_id']
		c['date'] = comment['date']
		c['like'] = comment['like']
		comm.append(c)

	outmessage = {}
	outmessage['online'] = count_online
	outmessage['messages'] = comm
	outmessage['msg_id'] = data['message_id']
	outmessage['type'] = 'comment'

	return outmessage

def likemess(data, count_online):
	like = Mongo.issetLike(data)
	if (like == 0):
		likes = Mongo.messageLike(data['msg_id'])
		Mongo.setLikeComm(data['msg_id'], data['id'])
	else:
		likes = Mongo.minusMessagesLike(data['msg_id'])
		Mongo.deleteCommentsLike(data)
	outmessage = {}
	outmessage['msg_id'] = data['msg_id']
	outmessage['likes'] = likes
	outmessage['employee_id'] = data['id']
	outmessage['type'] = 'likemess'
	outmessage['online'] = count_online

	return outmessage

def likecomm(data, count_online):
	like = Mongo.issetLike(data)
	if (like == 0):
		likes = Mongo.commentLike(data['msg_id'])
		Mongo.setLikeComm(data['msg_id'], data['id'])
	else:
		likes = Mongo.minusCommentsLike(data['msg_id'])
		Mongo.deleteCommentsLike(data)

	outmessage = {}
	outmessage['msg_id'] = data['msg_id']
	outmessage['likes'] = likes
	outmessage['employee_id'] = data['id']
	outmessage['type'] = 'likecomm'
	outmessage['online'] = count_online

	return outmessage	

def showComments(data, count_online):

	comments = Mongo.getComments(data['msg_id'])

	comm = []
	for comment in comments:
		c = {}
		c['id'] = str(comment['_id'])
		c['text'] = comment['text']
		c['parent_id'] = comment['parent_id']
		c['date'] = comment['date']
		c['like'] = comment['like']
		comm.append(c)

	outmessage = {}
	outmessage['online'] = count_online
	outmessage['messages'] = comm
	outmessage['msg_id'] = data['msg_id']
	outmessage['type'] = 'showComments'

	return outmessage

def allmess(data, count_online):

	messages = Mongo.getChatMessages(data)
	count = Mongo.getCountAllChatMessages(data)
	now = time.time()
	viewed_messages = {}

	messages_res = []

	count_messages = 0

	for mess in messages:
		count_messages += 1
		rd = now - mess['date']
		if(rd > 86400):
			if(rd < 172800):
				day = 'Вчера'
				mess['day'] = day
		else:
			day = 'Сегодня'
			mess['day'] = day
		
		mess_id = str(mess['_id'])
		viewed_messages[mess_id] = mess['viewed_time']
		coll ={}
		coll['date'] = mess['date']
		coll['text'] = mess['text']
		coll['parent_id'] = mess['parent_id']
		coll['to_id'] = mess['to_id']
		coll['isfile'] = mess['isfile']
		coll['annexes'] = mess['annexes']
		coll['viewed'] = mess['viewed']
		if(mess['viewed'] == 0):
			mess['viewed_time'] = time.time()
			Mongo.updateMessageVT(mess)
		coll['viewed_time'] = mess['viewed_time']
		coll['id'] = str(mess['_id'])
		day = 0
		if(rd > 86400):
			if(rd < 172800):
				day = 'Вчера'
				mess['day'] = day
		else:
			day = 'Сегодня'
			mess['day'] = day
		messages_res.append(coll)

	if count_messages == 25:
		dop_flag = 'true'
	else:
		dop_flag = 'false'

	messages_res.reverse()

	outmessage = {}
	outmessage['dop_flag'] = dop_flag
	outmessage['viewed_message'] = viewed_messages
	outmessage['messages'] = messages_res
	outmessage['online'] = count_online
	outmessage['type'] = 'mess'
	outmessage['parent'] = data['iam']
	outmessage['adresat'] = data['user_id']
	outmessage['count'] = data['count']

	return outmessage

def nullmess(data):
	Mongo.setNullCountDialogs(data)
	
def plusdialog(data):

	return data

def dialog(data):
	return data

def allusers(data):
	all_employees = getEmployeeCache(data['prefix'])

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

def alldialogs(data, count_online):

	dialogs = Mongo.getAllDialogs(data)

	for dialog in dialogs:
		parent = dialog['parent']
		if(data['dialogs'].get(parent) != None):
			data['dialogs'][parent] = int(dialog['count']) + int(data['dialogs'][parent])
		else:
			data['dialogs'][parent] = dialog['count']
			
	all_employees = getEmployeeCache(data['prefix'])

	employees = {}

	for em in all_employees:
		employees[em['id']] = em 

	users = []
	emps = data['dialogs'].keys()
	
	for employee in emps:
		coll = {}
		employee = int(employee)
		coll['id'] = employees[employee]['id']
		coll['avatar'] = employees[employee]['avatar']
		coll['name'] = employees[employee]['firstname'] + ' ' + employees[employee]['lastname']
		users.append(coll)
	


	outmessage = {}
	outmessage['type'] = 'alldialogs'
	outmessage['users'] = users
	outmessage['dialogs'] = data['dialogs']
	outmessage['online'] = count_online

	return outmessage

def notice(data):

	user_id = data['address'];



	return data

def onlineNotice(data):
	mtype = data['type']
	outmessage = {}
	outmessage['type'] = mtype
	message = {}
	message['title'] = data['title']
	message['description'] = data['description']
	message['link'] = data['link']
	outmessage['message'] = message 

	return outmessage

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
	messages = Mongo.getDopMessageForChat(data)
	dop_flag = 0
	viewed_messages = {}
	mess_2 = []
	now = time.time()
	for mess in messages:
		dop_flag += 1
		rd = now - mess['date']
		if(rd > 86400):
			if(rd < 172800):
				day = 'Вчера'
		else:
			day = 'Сегодня'
		mess['day'] = day
		if(mess['viewed'] == 0):
			mess['viewed_time'] = time.time()
			Mongo.updateMessageVT(mess)
		else:
			mess['viewed_time'] = 0 

		mess_to_client = {}
		mess_to_client['viewed_time'] = mess['viewed_time']
		mess_to_client['text'] = mess['text']
		mess_to_client['day'] = mess['day']
		mess_to_client['to_id'] = mess['to_id']
		mess_to_client['id'] = str(mess['_id'])
		mess_to_client['parent_id'] = mess['parent_id']
		mess_to_client['date'] = mess['date']
		mess_to_client['isfile'] = mess['isfile']
		mess_to_client['annexes'] = mess['annexes']
		mess_to_client['viewed'] = mess['viewed']
		
		mess_2.append(mess_to_client)

		mess_id = str(mess['_id'])
		viewed_messages[mess_id] = mess['viewed_time']

	if(dop_flag == 25):
		dop_flag = 'true'
	else:
		dop_flag = 'false'	

	outmessage = {}
	outmessage['dop_flag'] = dop_flag
	outmessage['viewed_messages'] = viewed_messages
	outmessage['messages'] = mess_2
	outmessage['type'] = 'dopmess'
	outmessage['adresat'] = data['user_id']
	outmessage['parent'] = data['iam']
	outmessage['count'] = data['count']

	return outmessage


def delComm(data, count_online):

	Mongo.delComm(data['id'])

	outmessage = {}
	outmessage['type'] = 'delComm'
	outmessage['id'] = data['id']

	return outmessage

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

def delMessOnChat(data, count_online):
	mess_id = Mongo.delMessOnChat(data)

	dat = {}
	dat['count'] = 0;
	dat['iam'] = data['employee_id']
	dat['user_id'] = data['dialoger']
	dat['adresat'] = 'user'
	dat['prefix'] = data['prefix']
	dat['type'] = 'allmess'

	outmessage = {}

	outmessage['type'] = 'delMessOnChat'
	outmessage['mess_id'] = mess_id

	return outmessage

def getEmployeeCache(prefix):
	employees = Mongo.getEmployees(prefix)
	return employees