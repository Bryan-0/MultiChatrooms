from app import join_room, leave_room, Rooms, app, render_template, Response, request, redirect, url_for, session, send, emit, socketio

@app.route("/")
def index_page():
	return render_template('index.html')

@app.route("/chats", methods=['POST', 'GET'])
def chats_page():
	Rooms.reloadRooms()
	session['user'] = {'userName': request.form['userName']}
	return render_template('chats.html', userName = session['user']['userName'], rooms = Rooms.getRoomList())


@socketio.on('connect')
def on_connect():
	pass