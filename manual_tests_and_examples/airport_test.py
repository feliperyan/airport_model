from Grid import Gridmap
from GridElements import Passenger, Point

airport = Gridmap(70, 70)

target = Point('x', 0, 69)

airport.build_horizontal_wall((0,4), 70)
door1 = [ Point('.', 10, 4), Point('#', 9, 5, 1, False), Point('#', 11, 5, 1, False)] 
door2 = [ Point('.', 50, 4), Point('#', 49, 5, 1, False), Point('#', 51, 5, 1, False) ]

# Shop 1
airport.build_vertical_wall((15,15), 15)
airport.build_vertical_wall((30,15), 15)
airport.build_horizontal_wall((15,30), 16)
airport.build_horizontal_wall((25,15), 5)

# Exit
airport.build_horizontal_wall((0,60), 70)

door3 = [ Point('.', 50, 60), Point('#', 49, 59, 1, False), Point('#', 51, 59, 1, False) ] 
door4 = [ Point('.', 52, 60), Point('#', 51, 59, 1, False), Point('#', 53, 59, 1, False) ] 
door5 = [ Point('.', 54, 60), Point('#', 53, 59, 1, False), Point('#', 55, 59, 1, False) ] 
door6 = [ Point('.', 56, 60), Point('#', 55, 59, 1, False), Point('#', 57, 59, 1, False) ]

elements = []
elements.extend(door1)
elements.extend(door2)
elements.extend(door3)
elements.extend(door4)
elements.extend(door5)
elements.extend(door6)
elements.append(target)

airport.load_elements(elements)

people = airport.add_passenger_block((4,0), 10, 4)

for p in people:
    p.destination = target
    p.path = p.a_star_pathfinding(airport)


print(airport.displayMap())
