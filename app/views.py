from app import join_room, leave_room, Rooms, app, render_template, Response, request, redirect, url_for, session, send, emit, socketio

@app.route("/")
def index_page():
	return render_template('index.html')

@app.route("/chats", methods=['POST'])
def chats_page():
	Rooms.reloadRooms()
	session['user'] = {'userName': request.form['userName'], 'userColor': Rooms.setRandomColor(), 'currentChatroom': "None", 'sid': 0}
	return render_template('chats.html', userName = session['user']['userName'], rooms = Rooms.getRoomList())

@socketio.on('connect')
def on_connect():
	session['user']['sid'] = request.sid
	print(session['user'])

@socketio.on('userJoinedChatroom')
def chatroom_join(data):
	join_room(data['roomName'])
	session['user']['currentChatroom'] = data['roomName']
	Rooms.addUserToRoom(data['roomName'], data['userName'], session['user']['userColor'])
	currentUsers = Rooms.readRoomInformation(data['roomName'])
	print(currentUsers)
	emit('getUsersList', {'userName': currentUsers['usersConnected']}, room = data['roomName'])

@socketio.on('roomMessage')
def room_message(data):
	emit('showMessage', {'userName': data['userName'], 'userColor': session['user']['userColor'], 'userMessage': data['userMessage']}, room = data['roomName'], broadcast = True)

@socketio.on('command')
def get_command(command):
	cmds = ["/createchatroom", "/deletechatroom", "/help"]

	splitCommand = str(command['userCommand']).split(" ")

	if len(splitCommand) >= 2:
		if splitCommand[0] in cmds:
			if splitCommand[0] == "/createchatroom":
				splitCommand.remove("/createchatroom")
				roomName = "".join([text + " " for text in splitCommand])[:-1]
				Rooms.createRoom(roomName)
				emit('commandResponse', {'response': f'Chatroom created: {roomName}. (click reload chatrooms button on chatrooms page to see it)'})
			elif splitCommand[0] == "/deletechatroom":
				splitCommand.remove("/deletechatroom")
				roomName = "".join([text + " " for text in splitCommand])[:-1]
				Rooms.deleteRoom(roomName)
				emit('commandResponse', {'response': f'Chatroom deleted: {roomName}. (click reload chatrooms button on chatrooms page to see it)'})

		else:
			emit('commandResponse', {'response': f'Command {splitCommand[0]} not found. Try /help'})
	else:
		if splitCommand[0] == "/createchatroom":
			emit('commandResponse', {'response': f'Command Usage {splitCommand[0]} <roomname>'})
		elif splitCommand[0] == "/deletechatroom":
			emit('commandResponse', {'response': f'Command Usage {splitCommand[0]} <roomname>'})
		elif splitCommand[0] == "/help":
			emit('commandResponse', {'response': f'Existing commands: /createchatroom <roomname>, /deletechatroom <roomname>'})
		else:
			emit('commandResponse', {'response': f'Command {splitCommand[0]} not found. Try /help'})
		

@socketio.on('userLeftChatroom')
def chatroom_left(data):
	leave_room(data['roomName'])
	session['user']['currentChatroom'] = "None"
	Rooms.removeUserFromRoom(data['roomName'], data['userName'], session['user']['userColor'])
	currentUsers = Rooms.readRoomInformation(data['roomName'])
	print(currentUsers)
	emit('getUsersList', {'userName': currentUsers['usersConnected']}, room = data['roomName'], broadcast = True)

@socketio.on('disconnect')
def on_disconnect():
	if session['user']['currentChatroom'] != "None":
		Rooms.removeUserFromRoom(session['user']['currentChatroom'], session['user']['userName'], session['user']['userColor'])
		currentUsers = Rooms.readRoomInformation(session['user']['currentChatroom'])
		print(currentUsers)
		emit('getUsersList', {'userName': currentUsers['usersConnected']}, room = session['user']['currentChatroom'], broadcast = True)

	session.pop('user', None)