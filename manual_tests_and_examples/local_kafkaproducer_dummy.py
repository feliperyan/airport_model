from Grid.Grid import Gridmap
from Grid.GridElements import Passenger, Point
import time

from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))

producer.send('test', {'Just': 'Connected'})


airport = Gridmap(50, 50)

target = Point('x', 0, 39)

airport.build_horizontal_wall((0,4), 50)
door1 = [ Point('.', 10, 4), Point('#', 9, 5, 1, False), Point('#', 11, 5, 1, False)] 
door2 = [ Point('.', 35, 4), Point('#', 34, 5, 1, False), Point('#', 36, 5, 1, False) ]

# # Shop 1
airport.build_vertical_wall((15,15), 15)
airport.build_vertical_wall((30,15), 15)
airport.build_horizontal_wall((15,30), 16)
airport.build_horizontal_wall((25,15), 5)

# # Exit
airport.build_horizontal_wall((0,35), 50)

door3 = [ Point('.', 35, 35), Point('#', 34, 34, 1, False), Point('#', 36, 34, 1, False) ] 
door4 = [ Point('.', 37, 35), Point('#', 36, 34, 1, False), Point('#', 38, 34, 1, False) ] 
door5 = [ Point('.', 39, 35), Point('#', 38, 34, 1, False), Point('#', 40, 34, 1, False) ] 
door6 = [ Point('.', 41, 35), Point('#', 40, 34, 1, False), Point('#', 42, 34, 1, False) ]

elements = []
elements.extend(door1)
elements.extend(door2)
elements.extend(door3)
elements.extend(door4)
elements.extend(door5)
elements.extend(door6)
elements.append(target)

airport.load_elements(elements)

people = airport.add_passenger_block((4, 0), 10, 4)

for p in people:
    p.destination = target
    p.path = p.a_star_pathfinding(airport)


while True:
    command = input('Hit n for next round q to stop\n')
    if command != 'n' and command != 'q':
        continue

    elif command == 'q':
        break

    elif command == 'n':
        moved = airport.move_all()
        for m in moved:
            producer.send('test', {m.name: str(m.pos())})
