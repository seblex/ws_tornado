import datetime

def logger(text):
	now = datetime.datetime.now()
	now = str(now)
	print('[' + now + '] ' + text)
	