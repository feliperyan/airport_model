from flask import Flask, render_template, jsonify, request, abort
from flask_socketio import SocketIO, emit
import json
from corsdecorator import crossdomain

from small_airport import *
import time

from thread_test import *

import kafka_helper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

app.debug = True


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/api/v1.0/scans', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def receive_scan_from_api():
    if not request.json:
        return 'not json...'

    msg = json.dumps(request.json)

    print ('\nJson Received from External Source:')
    print (msg)
    print ('\n')
    
    socketio.emit('scan', msg)

    return jsonify({'Response':'All ok'}), 201


# Actual Socket Events
@socketio.on('ping')
def handle_my_custom_event(jsonMessage):
    print('received json: ' + str(jsonMessage))
    reply = json.dumps({'message':'You are connected'})
    emit('pong', reply)


# Actual Socket Events
@socketio.on('go')
def handle_start(jsonMessage):
    print('received json: ' + str(jsonMessage))
    reply = json.dumps({'message':'Starting'})
    emit('Starting', reply)

    for i in range(1, 300):
        time.sleep(1)
        
        if i % 50 == 0:
            add_block()
            time.sleep(1)
        
        move_list = airport.move_all()
        moves = [m.pos() for m in move_list]

        print(i)

        socketio.emit('scan', json.dumps({'message': moves}))
#
#
@socketio.on('start')
def threaded_handle_start(jsonMessage):

    reply = json.dumps({'message':'Starting'})
    emit('Starting', reply)
    global tt
    tt = TimerClass(socketio, 50)
    tt.start()    

    # for i in range(1, 5):
    #     socketio.emit('scan', json.dumps({'message': 'aloha mahalo'}))

@socketio.on('stop')
def stop_thread(jsonMessage):
    print('\nStop Thread\n')
    # if tt and tt.isAlive():
    tt.event.set()


if __name__ == '__main__':
    socketio.run(app)