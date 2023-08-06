from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, max_http_buffer_size=10e8)

sid = ""


@socketio.on('connect', namespace='/imgToBB')
def test_connect(auth):
    socketio.emit('my response', {'data': 'Connected'})
    sid = request.sid


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.event
def heartbeat(data):
    print(request.sid)
    sid = request.sid

@socketio.event
def test(data):
    print(data)


@app.route('/', methods=['GET'])
def send_img_to_bb():
    socketio.emit('plugin', {"id": "test"}, room=sid)
    return "Dot get it"


socketio.run(app)
