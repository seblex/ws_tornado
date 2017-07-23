# coding: utf-8

import smtplib
from email.MIMEText import MIMEText
from Config import Config
from DataBase import Mongo

def sendEmail(message, addresat, frm, subject, prefix):
	# отправитель
	me = 'support.tonics@gmail.com'
	# получатель
	you = 'destination@mail.ru'
	# текст письма
	text = 'Тестовое письмо!\nОтправка письма из python'
	# заголовок письма
	subj = 'Тестовое письмо'

	smtp = Config.getSMTPconfig()

	# SMTP-сервер
	server = "smtp.gmail.com"
	port = 25
	user_name = "support.tonics@gmail.com"
	user_passwd = "password"

	# формирование сообщения
	msg = MIMEText(text, "", "utf-8")
	msg['Subject'] = subj
	msg['From'] = me
	msg['To'] = you

	# отправка
	for adres in addresat:
		employee = Mongo.getEmployee(prefix, adres)
		
	s = smtplib.SMTP(smtp['server'], smtp['port'])
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login(smtp['user_name'], smtp['user_passwd'])
	s.sendmail(me, you, msg.as_string())
	s.quit()