import pymongo

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

	count = db.messages.find({'to_id':0}).count()

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