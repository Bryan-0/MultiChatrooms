from app import join_room, leave_room, app, render_template, Response, request, redirect, url_for, session, send, emit, socketio

@app.route("/")
def index_page():
	return render_template('index.html')