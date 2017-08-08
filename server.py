# coding: utf-8
import json
import ssl
import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.httpserver
import pymongo
import socket
import pymysql

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from DataBase import MySQL, Mongo
from Loger import Loger
from Messages import Messages, MessagesRouter
from Config import Config
import BaseHTTPServer, SimpleHTTPServer

clients = {}
clients_copy = {}

class SocketServer(WebSocket):
    def handleMessage(self):
		# getting message
		data = json.loads(self.data)
		print(data)
		prefix = data['prefix']
		user_id = data['iam']
		#print(data)
		Loger.logger(data['type'], str(self.address))
		if prefix in clients:
			clients_prefix = clients[prefix]
			if self in clients_prefix:
				pass
			else:
				employee_id = Mongo.getEmployeeId(prefix, user_id)
				clients_prefix[self] = employee_id
		else:
			clients_prefix = {}
			employee_id = Mongo.getEmployeeId(prefix, user_id)
			clients_prefix[self] = employee_id
		clients[prefix] = clients_prefix
		#getting employees for app_copy
		if prefix in clients_copy:
			clients_copy_app = clients_copy[prefix]
		else:
			clients_copy_app = []
			#clients_copy[prefix] = []

		issetEmployeeInList = False
		for employeeInList in clients_copy_app:
			if employeeInList == user_id:
				issetEmployeeInList = True
		
		if issetEmployeeInList == False:
			clients_copy_app.append(user_id)

		clients_copy[prefix] = clients_copy_app
		count_online = len(clients_copy[prefix])
		print(data['type'])

		responce = MessagesRouter.route(data, count_online)
		#send responce
		if data['type'] == 'ping':
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))
		
		if data['type'] == 'online':
			responce['users'] = clients_copy[prefix]
			responce['online'] = len(clients_copy[prefix])
			result = json.dumps(responce)
			for client in clients[prefix]:
				client.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))
		
		if data['type'] == 'allusers':
			responce['online'] = count_online
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))
		
		if data['type'] == 'sounds':
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))
		
		if data['type'] == 'live':
			for client in clients[prefix]:
				client.sendMessage(u'' + responce)
			Loger.logger(data['type'] + '-responce', str(self.address))
		
		if data['type'] == 'delMess':
			result = json.dumps(responce)
			for client in clients[prefix]:
				client.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))
		
		if data['type'] == 'firstMessages':
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))
		
		if data['type'] == 'comment':
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))
		
		if data['type'] == 'showComments':
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))
		
		if data['type'] == 'delComm':
			result = json.dumps(responce)
			for client in clients[prefix]:
				client.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))
		
		if data['type'] == 'likecomm':
			result = json.dumps(responce)
			for client in clients[prefix]:
				client.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))
		
		if data['type'] == 'likemess':
			result = json.dumps(responce)
			for client in clients[prefix]:
				client.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))
		
		if data['type'] == 'sound':
			result = json.dumps(responce)
			for client in clients[prefix]:
				if (client != self): 
					client.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))
		
		if data['type'] == 'type_message':
			result = json.dumps(responce)
			adresaten = data['adresaten'];
			prefix = data['prefix']
			employee_id = Mongo.getEmployeeA(prefix, adresaten)
			for client in clients[prefix]:
				if(clients[prefix][client] == employee_id):
					client.sendMessage(u'' + result)
					
			Loger.logger(data['type'] + ' -responce', str(self.address))
		
		if data['type'] == 'new_message':
			result = json.dumps(responce)
			adresat_online = False
			adresaten = data['adresaten'];
			prefix = data['prefix']
			employee_id = Mongo.getEmployeeA(prefix, adresaten)
			print(employee_id)
			for client in clients[prefix]:
				print(clients[prefix][client])
				if(clients[prefix][client] == employee_id):
					client.sendMessage(u'' + result)
					adresat_online = True
			if(adresat_online == False):
				Messages.setDialog(data)
			Loger.logger(data['type'] + ' -responce', str(self.address))
		
		if data['type'] == 'allmess':
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))
		
		if data['type'] == 'alldialogs':
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))

		if data['type'] == 'delMessOnChat':
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))

		if data['type'] == 'filelive':
			result = json.dumps(responce)
			for client in clients[prefix]:
				client.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))

		if data['type'] == 'file':
			result = json.dumps(responce)
			adresat_online = False
			adresaten = data['adresaten'];
			prefix = data['prefix']
			employee_id = Mongo.getEmployeeA(prefix, adresaten)
			for client in clients:
				if(clients[prefix][client] == employee_id):
					client.sendMessage(u'' + result)
					adresat_online = True
			if(adresat_online == False):
				Messages.setDialog(data)
			Loger.logger(data['type'] + ' -responce', str(self.address))

		if data['type'] == 'dopmess':
			result = json.dumps(responce)
			self.sendMessage(u'' + result)
			Loger.logger(data['type'] + '-responce', str(self.address))

		if data['type'] == 'onlineNotice':
			action = False
			query = "SELECT * FROM `" + data['prefix'] + "csettings` WHERE `employee_id` = " + data['iam']
			cur = MySQL.db_select(query, data['prefix'])
			for row in cur:
				if data['type_notice'] == 'mess_on_live':
					if row[2] == 1:
						action = True
				if data['type_notice'] == 'like_on_live':
					if row[4] == 1:
						action = True
				if data['type_notice'] == 'comm_on_live':
					if row[3] == 1:
						action = True
			if action == True:	
				result = json.dumps(responce)
				for client in clients[prefix]:
					if (client != self): 
						client.sendMessage(u'' + result)
				Loger.logger(data['type'] + '-responce', str(self.address))

		if data['type'] == 'offer':
			for client in clients[prefix]:
				client.sendMessage(u'' + json.dumps(data['desc']))

		if data['type'] == 'answer':
			for client in clients[prefix]:
				client.sendMessage(u'' + json.dumps(data['desc']))

		if data['type'] == 'ice1':
			for client in clients[prefix]:
				client.sendMessage(u'' + json.dumps(data['desc']))

		if data['type'] == 'ice2':
			for client in clients[prefix]:
				client.sendMessage(u'' + json.dumps(data['desc']))

		if data['type'] == 'hangup':
			for client in clients[prefix]:
				client.sendMessage(u'' + json.dumps(data['desc']))

		notices = Mongo.getNotices(data['prefix'])

		for notice in notices:
			user_id = notice['addresat']
			notice_type = 'onlineNotice'
			outmessage = {}
			outmessage['type'] = notice_type
			mess = {}
			if(notice['title'] != ''):
				mess['title'] = notice['title']
			else:
				mess['title'] = u'Уведомление'
			mess['description'] = notice['description']
			mess['link'] = notice['link']
			outmessage['message'] = mess
			outmessage = json.dumps(outmessage)

			prefix = data['prefix']
			employee_id = Mongo.getEmployeeA(prefix, user_id)
			for client in clients[prefix]:
				if(clients[prefix][client] == employee_id):
					client.sendMessage(u'' + outmessage)
					Loger.logger('notice_from_queue' + '-responce', str(self.address))
					Mongo.deleteNotice(notice, data['prefix'])


    def handleConnected(self):
		print(self.address, 'connected')
		Loger.logger('connected', str(self.address))
		

    def handleClose(self):
    	#delete self
    	for client in clients:
    		for cl in clients[client]:
    			if self in clients[client]:
    				prefix = client
    				user_id = clients[client][self]
    				employee_id = Mongo.getEmployeeIdFromObj(user_id, prefix)
    				for client_app in clients_copy[prefix]:
    					employee = str(employee_id)
    					if client_app == employee:
    						clients_copy[prefix].remove(client_app)
    						
    				del clients[client][self]
    				
    				Loger.logger('closed', str(self.address))
    				print(self.address, 'closed')


port = Config.getPort()
server = SimpleWebSocketServer('', port, SocketServer)
server.serveforever()
# httpd = BaseHTTPServer.HTTPServer(('', port), SimpleHTTPServer.SimpleHTTPRequestHandler)
# httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='./cert.pem', keyfile='./cert.pem', ssl_version=ssl.PROTOCOL_TLSv1)
# httpd.serve_forever()
