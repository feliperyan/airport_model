import time
from Grid.Grid import Gridmap
from Grid.GridElements import Passenger, Point


airport = Gridmap(50, 50)

target = Point('*', 20, 39)

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

def add_block():
    people = airport.add_passenger_block((4, 0), 10, 4)
    for p in people:
        p.destination = target
        p.path = p.a_star_pathfinding(airport)


#print(airport.displayMap())


def start():
    for i in range(1, 1000):
        time.sleep(0.1)
        if i % 50 == 0:
            add_block()
            time.sleep(1)
            print('Members: ', len(airport.members))
        print(airport.displayMap())
        airport.move_all()






