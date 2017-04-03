from threading import Thread, Event
from time import sleep
from Grid.Grid import *
import json

import kafka_helper
from random import random
from math import floor


class TimerClass(Thread):
    def __init__(self, socketio, rounds):
        Thread.__init__(self)
        self.event = Event()
        self.sock = socketio
        self.rounds = rounds

        try:
            self.producer = kafka_helper.get_kafka_producer()
            print('\nKafka on Heroku Checks:')
            print(kafka_helper.get_kafka_ssl_context())
            print(kafka_helper.get_kafka_brokers())
            print('\n')

        except RuntimeError:
            # We're not on Heroku, try local running Kafka:
            print('Thread for Kafka running local Kafka')
            from kafka import KafkaProducer
            producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
            producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
            self.producer = producer


    def run(self):
        airport = getMapFromFile('map.txt')    
        i = 0 

        while True:
            if self.event.is_set():
                print('Event Set')
                break

            if i % 20 == 0:
                airport.add_passenger_block((0,0), 2,2)                
                for person in airport.members:
                    exits = airport.exits
                    size = len(exits)
                    person.destination = exits[floor(size * random())]
                    person.path = person.a_star_pathfinding(airport)

            move_list = airport.move_all()
            moves = [m.pos() for m in move_list]
            
            print(moves)

            future = self.producer.send('topic1', value={'moves': moves})                        
            record_metadata = future.get(timeout=10)
            print (record_metadata.topic)
            print (record_metadata.partition)
            print (record_metadata.offset)            

            i += 1
            sleep(1)


def move_world(socketio, rounds=300, producer=None):
    for i in range(1, 30):
        time.sleep(1)

        if i % 50 == 0:
            add_block()
            time.sleep(1)
            add_passenger_block

        move_list = airport.move_all()
        moves = [m.pos() for m in move_list]

        print(i)

        producer.send('test', value={'k': 'v'})

        #socketio.emit('scan', json.dumps({'message': moves}))
