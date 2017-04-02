import random
from math import floor
from Grid.Queues import PriorityQueue, Queue

# Statuses for passengers
PENDING = 'PENDING'
MOVING = 'MOVING'
LOITERING = 'LOITERING'
QUEUEING = 'QUEUEING'


class Point(object):
    """ A point on the grid map
        Args: name = string; x = int, y = int, cost = int, passable = boolean
    """
    def __init__(self, name='#', x=0, y=0, cost=1, passable=True):
        self.name = name
        self.xpos = x
        self.ypos = y
        self.cost = cost
        self.passable = passable

    def __str__(self):
        return self.name

    def pos(self):
        '''Returns x and y coordinates'''
        return self.xpos, self.ypos

    def __repr__(self):
        return self.name + ' is at ' + str(self.xpos) + ',' + str(self.ypos)

    def __lt__(self, value):
        return (self.xpos + self.ypos) < (value.xpos + value.ypos)

    def __gt__(self, value):
        return (self.xpos + self.ypos) > (value.xpos + value.ypos)
#
#
class Passenger(Point):
    ''' A passenger map element '''
    # pylint: disable=too-many-instance-attributes

    def __init__(self, name='', xpos=0, ypos=0, cost=10, passable=True, patience=5):
        Point.__init__(self, name, xpos, ypos, cost, passable)
        self.destination = None # should be a Point
        self.path = list()
        self.patience = patience
        self.current_patience = patience
        self.list_of_target_dicts = list()
        self.status = PENDING


    def a_star_pathfinding(self, grid):
        '''A* pathfinding to target'''
        frontier = PriorityQueue()

        frontier.put(self, 0)
        came_from = {}
        cost_so_far = {}
        came_from[self] = None
        cost_so_far[self] = 0

        while not frontier.empty():
            current = frontier.get()

            if current.pos() == self.destination.pos():
                break

            for node in grid.get_adjacent_nodes(current.xpos, current.ypos):
                new_cost = cost_so_far[current] + node.cost
                if node not in cost_so_far or new_cost < cost_so_far[node]:
                    cost_so_far[node] = new_cost
                    priority = new_cost + self.heuristic(node)
                    frontier.put(node, priority)
                    came_from[node] = current

        current = grid.get(self.destination.xpos, self.destination.ypos)
        path = [current.pos()]

        # If we cant reach the destination:
        if current not in came_from:
            return None

        while current.pos() != self.pos():
            current = came_from[current]
            path.append(current.pos())

        path.reverse()
        return path[1:]


    def heuristic(self, node):
        '''Not taking into account diagonal distances for now.'''
        ddx = abs(node.xpos - self.destination.xpos)
        ddy = abs(node.ypos - self.destination.ypos)

        return ddx+ddy


    def breath_first_pathfinding(self, grid):
        frontier = Queue()
        frontier.put(self)
        came_from = {}
        came_from[self] = None

        while not frontier.empty():
            current = frontier.get()

            if current.pos() == self.destination.pos():
                print('found')
                break

            for node in grid.get_adjacent_nodes(current.xpos, current.ypos):
                if node not in came_from:
                    frontier.put(node)
                    came_from[node] = current

        current = grid.get(self.destination.xpos, self.destination.ypos)
        path = [current]

        # If we never reached the destination:
        if current not in came_from:
            return None

        while current.pos() != self.pos():
            current = came_from[current]
            path.append(current)

        return path

    def next_move(self, grid):
        ''' Based on the path where should I move next?
            Returns: Next x,y coordinate
            If we're at the end of the path = return same position
            Modifies: self, may create a new path based on patience.
        '''
        if len(self.path) == 0:
            return self.pos()

        if self.status == LOITERING:
            self.loiter_movement(grid)

        next_point_in_path = self.path[0]
        #something else could be at that location since we built the path
        updated_point = grid.get(next_point_in_path[0], next_point_in_path[1])

        if updated_point.passable and not type(updated_point) == Passenger:

            if updated_point.pos() == self.destination.pos() and self.destination.name == '*':
                print('exit')
                self.xpos = -1
                self.ypos = -1
                return (-1, -1)

            # reset patience, passenger moved through
            self.current_patience = self.patience

            self.xpos = next_point_in_path[0]
            self.ypos = next_point_in_path[1]
            try:
                return self.path.pop(0)
            except IndexError:
                # must be at target
                return self.pos()
        else:
            # print(self.name + ' can not pass')
            if self.current_patience <= 0:
                # print(self.name + ' is rerouting')
                self.path = self.a_star_pathfinding(grid)
                self.current_patience = self.patience

            self.current_patience -= 1
            return self.pos()


    # Loitering just causes a block of people to slowly expand
    # doesn't really look like they're loitering
    def start_loitering(self, grid, rounds=100):
        self.status = LOITERING
        self.path = list()
        self.loiter_movement(grid)


    def loiter_movement(self, grid, probability=None):
        tiles = grid.get_adjacent_nodes(self.xpos, self.ypos)
        self.destination = Point(name='*', x=self.xpos, y=self.ypos)

        if probability is None:
            probability = random.random()
            if probability >= 0.7 and len(tiles) > 0:
                t = floor(random.random() * (len(tiles)))
                self.path.append(tiles[t].pos())
            else:
                self.path.append(self.destination.pos())
#
#
class Wall(Point):
    pass
#
#
class Exit(Point):
    pass
#
#
class ShopFloor(Point):
    def __init__(self, x=0, y=0, cost=1):
        Point.__init__(self, name='.', x=x, y=y, cost=cost, passable=True)
#
#
