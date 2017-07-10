import Messages

def route(data, count_online):
	if(data['type'] == 'firstMessages'):
		responce = Messages.first_messages(data, count_online)

	if(data['type'] == 'ping'):
		responce = Messages.ping(data)

	if(data['type'] == 'viewed_messages'):
		responce = Messages.viewed_messages(data)

	if(data['type'] == 'annexesfiles'):
		responce = Messages.annexesfiles(data)

	if(data['type'] == 'filelive'):
		responce = Messages.filelive(data)

	if(data['type'] == 'file'):
		responce = Messages.file(data)

	if(data['type'] == 'type_message'):
		responce = Messages.type_message(data)

	if(data['type'] == 'new_message'):
		responce = Messages.new_message(data)

	if(data['type'] == 'sounds'):
		responce = Messages.sounds(data)

	if(data['type'] == 'sound'):
		responce = Messages.sound(data)

	if(data['type'] == 'online'):
		responce = Messages.online(data, count_online)

	if(data['type'] == 'live'):
		responce = Messages.live(data, count_online)

	if(data['type'] == 'comment'):
		responce = Messages.comment(data, count_online)

	if(data['type'] == 'likemess'):
		responce = Messages.likemess(data, count_online)

	if(data['type'] == 'likecomm'):
		responce = Messages.likecomm(data, count_online)

	if(data['type'] == 'showComments'):
		responce = Messages.showComments(data, count_online)

	if(data['type'] == 'dialog'):
		responce = Messages.dialog(data)

	if(data['type'] == 'mess'):
		responce = Messages.mess(data)

	if(data['type'] == 'allusers'):
		responce = Messages.allusers(data)

	if(data['type'] == 'alldialogs'):
		responce = Messages.alldialogs(data)

	if(data['type'] == 'notice'):
		responce = Messages.notice(data)

	if(data['type'] == 'onlineNotice'):
		responce = Messages.onlineNotice(data)

	if(data['type'] == 'offer'):
		responce = Messages.offer(data)

	if(data['type'] == 'answer'):
		responce = Messages.answer(data)

	if(data['type'] == 'ice1'):
		responce = Messages.ice1(data)

	if(data['type'] == 'ice2'):
		responce = Messages.ice2(data)

	if(data['type'] == 'hangup'):
		responce = Messages.hangup(data)

	if(data['type'] == 'dopmess'):
		responce = Messages.dopmess(data)

	if(data['type'] == 'delComm'):
		responce = Messages.delComm(data, count_online)

	if(data['type'] == 'delMess'):
		responce = Messages.delmess(data, count_online)

	if(data['type'] == 'closeChat'):
		responce = Messages.closeChat(data)

	return responce

