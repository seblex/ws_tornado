import datetime
from DataBase import Mongo

def logger(text, emp_id):
	now = datetime.datetime.now()
	now = str(now)
	log = '[' + now + '] ' + ' : ' + emp_id + ' - ' + text
	print(log)
	#Mongo.setLog(log, prefix)
	