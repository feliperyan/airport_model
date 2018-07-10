# If you're getting errors running locally try
# gunicorn -k gevent -w 1 server_flask_websocket:app


from flask import Flask, render_template, jsonify, request, abort
from flask_socketio import SocketIO, emit
import json
from corsdecorator import crossdomain
import time

from threaded_airport_simulator import *
import kafka_helper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

app.debug = True

threads = list()

@app.route('/')
def hello():
    return render_template('index.html')


@socketio.on('ping')
def handle_my_custom_event(jsonMessage):
    print('received json: ' + str(jsonMessage))
    reply = json.dumps({'message':'Connected to Heroku'})
    emit('pong', reply)


# One Kafka event per second with all movement
# this will create a small number of Kadka events per second.
@socketio.on('start')
def threaded_handle_start(jsonMessage):

    reply = json.dumps({'message':'Starting'})
    emit('Starting', reply)

    for t in threads:
        t.event.set()
    
    tt = TimerClass(socketio, True)
    threads.append(tt)
    
    # The thread itself emits the necessary data to the socket.
    tt.start()


# One Kafka event per "person" movement, this will generate a 
# larger number of Kafka events per second.
@socketio.on('flood')
def threaded_handle_flood(jsonMessage):

    reply = json.dumps({'message':'Starting'})
    emit('Starting - FLOOD', reply)

    for t in threads:
        t.event.set()
    
    tt = TimerClass(socketio, False)
    threads.append(tt)

    # The thread itself emits the necessary data to the socket.
    tt.start()


@socketio.on('stop')
def stop_thread(jsonMessage):
    print('\nStop Thread\n')
    for t in threads:
        t.event.set()


# left in here for example purposes, in case you want to get a POST
# and a json payload and emit a socketio message back to subscribing
# clients.
@app.route('/api/v1.0/scans', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def receive_scan_from_api():
    if not request.json:
        return 'not json...'
    msg = json.dumps(request.json)
    print ('\nJson Received from External Source:')
    print (msg)
    print ('\n') 
    socketio.emit('post', msg)
    return jsonify({'Response':'All ok'}), 201


if __name__ == '__main__':
    socketio.run(app)