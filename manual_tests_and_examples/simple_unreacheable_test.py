from Grid.Grid import Gridmap
from Grid.GridElements import *

grid = Gridmap(5, 5)
p = Passenger('p', 2, 2)
t = Point(name='*', x=0, y=2)
p.destination = t
grid.load_elements([p, t])

grid.build_vertical_wall((1,0), 5)

print(grid.displayMap())

p.path = p.a_star_pathfinding(grid)

