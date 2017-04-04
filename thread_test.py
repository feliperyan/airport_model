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
        airport = getMapFromFile('sydney_airport.txt')
        i = 0 

        while True:
            if self.event.is_set():
                print('Event Set')
                break

            if i % 50 == 0:
                terminal = floor(3*random())
                new_arrivals = None
                if terminal == 0:
                    new_arrivals = airport.add_passenger_block((35, 35), 12, 2)
                elif terminal == 1:
                    new_arrivals = airport.add_passenger_block((84, 8), 7, 4)
                else:
                    new_arrivals = airport.add_passenger_block((17, 93), 9, 5)

                for person in new_arrivals:
                    exits = airport.exits
                    size = len(exits)
                    person.destination = exits[floor(size * random())]
                    person.path = person.a_star_pathfinding(airport)

            move_list = airport.move_all()
            moves = [m.pos() for m in move_list]

            print(moves)

            future = self.producer.send('topic1', value={'moves': moves})
            record_metadata = future.get(timeout=10)
            print(record_metadata.topic)
            print(record_metadata.partition)
            print(record_metadata.offset)

            #For now also emit socket message:
            self.sock.emit('scan', json.dumps({'message': moves}))

            i += 1
            sleep(1)
