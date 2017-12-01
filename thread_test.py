from threading import Thread, Event
from time import sleep
from Grid.Grid import *
import json

import kafka_helper
from random import random
from math import floor


class TimerClass(Thread):
    def __init__(self, socketio, soft):
        Thread.__init__(self)
        self.event = Event()
        self.sock = socketio
        self.soft = soft

        print('\nKafka on Heroku Checks:')

        try:            
            self.producer = kafka_helper.get_kafka_producer()
            print(kafka_helper.get_kafka_ssl_context())
            print(kafka_helper.get_kafka_brokers())            
            
            print('\nRunning on Heroku') 

        except Exception:
            
            # We're not on Heroku, try local running Kafka:            
            from kafka import KafkaProducer
            producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))            
            self.producer = producer

            print('\nRunning Local - so not using kafka_helper')

    def run(self):
        airport = getMapFromFile('sydney_airport.txt')
        i = 0 

        while True:
            if self.event.is_set():
                print('Event Set')
                break

            if i % 15 == 0:
                terminal = floor(3*random())
                new_arrivals = None
                if terminal == 0:
                    new_arrivals = airport.add_passenger_block((35, 33), 12, 2)
                
                elif terminal == 1:
                    new_arrivals = airport.add_passenger_block((92, 8), 12, 2)
                
                else:
                    new_arrivals = airport.add_passenger_block((21, 76), 8, 2)                

                for person in new_arrivals:
                    exits = airport.exits
                    size = len(exits)
                    person.destination = exits[floor(size * random())]
                    person.path = person.a_star_pathfinding(airport)

                i = 1 # just resetting so we don't get a huge i after a while.

            move_list = airport.move_all()
            moves = [ list(m.pos()).append(m.current_patience) for m in move_list ]

            print(moves)

            if not self.soft:
                for m in moves:
                    #prod topic:
                    future = self.producer.send('movement-keyword', value={'move': m})
                    #local test topic
                    #future = self.producer.send('test', value={'move': m})
                    record_metadata = future.get(timeout=10)
                    print(record_metadata.topic)
                    print(record_metadata.partition)
                    print(record_metadata.offset)

            else:
                #prod topic:
                future = self.producer.send('movement-keyword', value={'moves': moves})
                #local topic
                #future = self.producer.send('test', value={'moves': moves})
                record_metadata = future.get(timeout=10)
                print(record_metadata.topic)
                print(record_metadata.partition)
                print(record_metadata.offset)


            #For now also emit socket message:
            self.sock.emit('scan', json.dumps({'message': moves}))

            i += 1
            sleep(0.5)
