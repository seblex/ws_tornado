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


