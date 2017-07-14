import pymongo
import time

from pymongo import MongoClient
from bson.objectid import ObjectId

def insertToMessages(coll):
	c = MongoClient()
	db = c.ws_server
	
	db.messages.save(coll)

	new_mess = db.messages.find_one({'parent_id':coll['parent_id'], 'to_id': coll['to_id'], 'date': coll['date']})
	
	return new_mess['_id']

def deleteMessage(mess_id):
	c = MongoClient()
	db = c.ws_server

	mess = db.messages.find_one({'_id': ObjectId(mess_id)})
	
	db.messages.remove(mess)

def getFirstMessages():
	c = MongoClient()
	db = c.ws_server

	messages = db.messages.find({'to_id': '0'}).limit(10).sort('date',pymongo.DESCENDING)

	return messages

def getCountAllMessages():
	c = MongoClient()
	db = c.ws_server

	count = db.messages.find({'to_id': '0'}).count()

	return count

def insertNewComment(coll):
	c = MongoClient()
	db = c.ws_server

	db.comments.save(coll)

def getComments(msg_id):
	c = MongoClient()
	db = c.ws_server

	comments = db.comments.find({'msg_id': msg_id}).limit(8).sort('date', pymongo.DESCENDING)

	return comments

def delComm(msg_id):
	c = MongoClient()
	db = c.ws_server

	comm = db.comments.find_one({'_id': ObjectId(msg_id)})
	
	db.comments.remove(comm)

def issetLike(data):
	c = MongoClient()
	db = c.ws_server

	employee_id = data['id']
	message_id = data['msg_id']

	count = db.likes.find({'employee_id': employee_id, 'message_id': message_id}).count()

	if (count == 1):
		like = db.likes.find_one({'employee_id': employee_id, 'message_id': message_id})
	else:
		like = 0

	return like

def commentLike(msg_id):
	c = MongoClient()
	db = c.ws_server

	comment = db.comments.find_one({'_id': ObjectId(msg_id)})
	
	cl = int(comment['like'])
	comment['like'] = cl + 1
	db.comments.save(comment)

	return comment['like']

def setLikeComm(msg_id, e_id):
	c = MongoClient()
	db = c.ws_server

	coll = {}
	coll['employee_id'] = e_id
	coll['message_id'] = msg_id

	db.likes.save(coll)

def minusCommentsLike(msg_id):
	c = MongoClient()
	db = c.ws_server

	comment = db.comments.find_one({'_id': ObjectId(msg_id)})

	cl = comment['like']
	comment['like'] = cl - 1
	db.comments.save(comment)

	return comment['like']

def deleteCommentsLike(data):
	c = MongoClient()
	db = c.ws_server

	employee_id = data['id']
	message_id = data['msg_id']

	like = db.likes.find_one({'employee_id': employee_id, 'message_id': message_id})
	db.likes.remove(like)

def messageLike(msg_id):
	c = MongoClient()
	db = c.ws_server

	message = db.messages.find_one({'_id': ObjectId(msg_id)})
	
	cl = int(message['like'])
	message['like'] = cl + 1
	db.messages.save(message)

	return message['like']

def minusMessagesLike(msg_id):
	c = MongoClient()
	db = c.ws_server

	message = db.messages.find_one({'_id': ObjectId(msg_id)})

	cl = message['like']
	message['like'] = cl - 1
	db.messages.save(message)

	return message['like']

def getChatMessages(data):
	c = MongoClient()
	db = c.ws_server

	parent_id = data['iam']
	to_id = data['user_id']

	query = 'this.parent_id == "'+parent_id+'" || this.parent_id == "'+to_id+'"'
	messages = db.messages.find().where(query).limit(25).sort('date', pymongo.DESCENDING)
	mess_result = []
	
	for mess in messages:
		if (mess['to_id'] == parent_id):
			mess_result.append(mess)
		if(mess['to_id'] == to_id):
			mess_result.append(mess)	

	return mess_result

def setNewChatMessage(data):
	c = MongoClient()
	db = c.ws_server

	coll = {}
	coll['date'] = time.time()
	coll['text'] = data['message']
	coll['parent_id'] = data['user_id']
	coll['to_id'] = data['adresaten']
	coll['isfile'] = 'false'
	coll['annexes'] = ''
	coll['viewed'] = 0
	coll['viewed_time'] = 0

	db.messages.save(coll)

def updateMessageVT(mess):
	c = MongoClient()
	db = c.ws_server

	db.messages.save(mess)

def setDialog(data):
	c = MongoClient()
	db = c.ws_server

	coll = {}
	coll['parent'] = data['user_id']
	coll['adresat'] = data['adresaten']

	dialog = db.dialogs.find_one({'parent': data['user_id'], 'adresat': data['adresaten']})
	if(dialog == None):
		coll['count'] = 1
		db.dialogs.save(coll)
	else:
		count = dialog['count']
		dialog['count'] = count + 1
		db.dialogs.save(dialog)

def getAllDialogs(data):
	c = MongoClient()
	db = c.ws_server

	dialogs = db.dialogs.find({'adresat': data['user_id']})

	return dialogs

def setNullCountDialogs(data):
	c = MongoClient()
	db = c.ws_server

	dialog = db.dialogs.find_one({'adresat': data['adresaten'], 'parent': data['iam']})

	if (dialog != None):
		dialog['count'] = 0
		db.dialogs.save(dialog)

def delMessOnChat(data):
	c = MongoClient()
	db = c.ws_server
	timestamp = str(data['timestamp'])
	timestamp2 = float(timestamp)
	
	message = db.messages.find({'parent_id': data['employee_id'], 'to_id': data['dialoger'], 'text': data['message']})
	timestamp_on = timestamp2 - 60
	timestamp_off = timestamp2 + 60

	for mess in message:
		if(mess['date'] > timestamp_on):
			if(mess['date'] < timestamp_off):
				db.messages.remove(mess)

	return False

def setFileMessage(data):
	c = MongoClient()
	db = c.ws_server

	coll = {}
	coll['text'] = data['fileName']
	coll['parent_id'] = data['user_id']
	coll['to_id'] = data['adresat']
	coll['date'] = time.time()
	coll['isfile'] = 'true'
	coll['annexes'] = ''
	coll['members'] = 'all'
	coll['like'] = 0

	db.messages.save(coll)

	new_mess = db.messages.find_one(coll)
	
	return str(new_mess['_id'])

def setFileMessageFromChat(data):
	c = MongoClient()
	db = c.ws_server

	coll = {}
	coll['text'] = data['fileName']
	coll['parent_id'] = data['user_id']
	coll['to_id'] = data['adresaten']
	coll['date'] = time.time()
	coll['isfile'] = 'true'
	coll['annexes'] = ''
	coll['members'] = 'all'
	coll['like'] = 0
	coll['viewed'] = 0
	coll['viewed_time'] = 0

	db.messages.save(coll)

	new_mess = db.messages.find_one(coll)
	
	return str(new_mess['_id'])

def getEmployees(prefix):
	c = MongoClient()
	db = c.ws_server

	employees = db.employees.find({'prefix': prefix})
	
	return employees