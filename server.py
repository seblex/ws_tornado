import json

import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.httpserver

import pymongo
import socket
import pymysql

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from DataBase import MySQL
from Loger import Loger
from Messages import Messages, MessagesRouter

clients = {}
class SocketServer(WebSocket):

    def handleMessage(self):
		#self.sendMessage(self.data)
		# getting message
		data = json.loads(self.data)
		#getting users id and prefix
		if clients[self] == 0:
			user_id = data['iam']
			prefix = data['prefix']
			employee_id = MySQL.get_employee_id(user_id, prefix)
			clients[self] = employee_id

		count_online = len(clients)	

		responce = MessagesRouter.route(data, count_online)
		#send responce
		if data['type'] == 'ping':
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce')
		if data['type'] == 'online':
			result = json.dumps(responce)
			for client in clients:
				client.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce')
		if data['type'] == 'allusers':
			responce['online'] = count_online
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce')
		if data['type'] == 'sounds':
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce')
		if data['type'] == 'live':
			for client in clients:
				client.sendMessage(u'' + responce)
			Loger.logger(data['type'] + '-responce')
		if data['type'] == 'delMess':
			result = json.dumps(responce)
			for client in clients:
				client.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce')
		if data['type'] == 'firstMessages':
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce')
		if data['type'] == 'comment':
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce')
		if data['type'] == 'showComments':
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce')
		if data['type'] == 'delComm':
			result = json.dumps(responce)
			for client in clients:
				client.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce')
		if data['type'] == 'likecomm':
			result = json.dumps(responce)
			for client in clients:
				client.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce')
		if data['type'] == 'likemess':
			result = json.dumps(responce)
			for client in clients:
				client.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce')
		if data['type'] == 'sound':
			result = json.dumps(responce)
			for client in clients:
				if (client != self): 
					client.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce')

    def handleConnected(self):
    	print(self.address, 'connected')
    	clients[self] = 0;
    	
    def handleClose(self):
    	del clients[self]
    	print(self.address, 'closed')




server = SimpleWebSocketServer('', 8095, SocketServer)
server.serveforever()
