from string import ascii_lowercase
from Grid.GridElements import Point, Passenger, ShopFloor

FLOOR = '.'
WALLS = '#'
EXITS = '*'
SHOPS = '$'


def getMapFromFile(file_name):
    f = open(file_name, 'r')
    whole_file = f.readlines()

    for pos in range(0, len(whole_file)):
        whole_file[pos] = whole_file[pos].rstrip()

    grid = Gridmap(width=len(whole_file[0]), height=len(whole_file))

    row_num = 0
    column_num = 0

    for row in whole_file:
        #start of new row, reset column
        column_num = 0

        for e in row:
            if e == FLOOR:
                #floor
                single_floor_tile_list = [Point(name=FLOOR, x=column_num, y=row_num),]
                grid.load_elements(single_floor_tile_list)

            elif e == WALLS:
                single_wall_tile_list = [Point(name=WALLS, x=column_num, y=row_num, passable=False),]
                grid.load_elements(single_wall_tile_list)

            elif e == EXITS:
                single_exit_tile_list = [Point(name=EXITS, x=column_num, y=row_num),]
                grid.load_elements(single_exit_tile_list)

            elif e == SHOPS:
                single_shop_tile_list = [ShopFloor(x=column_num, y=row_num),]
                grid.load_elements(single_shop_tile_list)                

            column_num += 1

        row_num += 1

    f.close()

    return grid


class Gridmap(object):
    ''' A 2d map '''
    def __init__(self, width = 10, height = 10):
        self.w = width
        self.h = height
        self.__map = self.__initMap(width, height)
        self.size = [self.w, self.h]
        self.members = list()
        self.shops = list()
        self.exits = list()

    def __initMap(self, w, h):
        a = list()
        for i in range(0, h):
            b = list()
            for j in range(0, w):
                b.append(Point('.', x=j, y=i))
            a.append(b)

        return a


    def get(self, xpos, ypos):
        """ Get element, x/y coord must be both > 0 """
        if xpos < 0 or ypos < 0:
            raise IndexError
        return self.__map[ypos][xpos]

    def __put(self, element, xpos, ypos):
        """ Put element, x/y coord must be both > 0 """
        if xpos < 0 or ypos < 0 or xpos+1 > self.w or ypos+1 > self.h:
            raise CantPlotOnMap('Position x: ' + str(xpos) + ' y: ' + str(ypos) + \
                ' is out of bounds, remember it is 0 indexed')

        self.__map[ypos][xpos] = element


    def pop(self, xpos, ypos):
        ''' Returns element at that location and replaces it with floor Point
        '''
        element = self.get(xpos, ypos)

        if type(element) == Passenger:
            self.members.remove(element)

        self.__map[ypos][xpos] = Point('.', xpos, ypos)

        return element


    def load_elements(self, elements=None):
        """ Loads elements into the map.
            Args: passengers = list containing elements to be added to the map
        """
        if type(elements) != list:
            raise ValueError('attribute passengers should be a list')

        for p in elements:
            self.pop(p.xpos, p.ypos)
            self.__put(p, p.xpos, p.ypos)

            if type(p) == Passenger:
                self.members.append(p)

            if type(p) == ShopFloor:
                self.shops.append(p)

            if p.name == '*':
                self.exits.append(p)


    def displayMap(self):
        ''' Returns a string representation of the grid and its members '''
        header = '  '
        for x in range(0, self.w):
            if x < 10:
                header += ' 0'+str(x)
            else:
                header += ' '+str(x)
        header += '\n'

        row = 0

        for a in self.__map:
            if row < 10:
                line = '0'+str(row)
            else:
                line = str(row)

            for e in a:
                line += '  '+str(e)
            line += '\n'
            header += line
            row += 1

        return header

    def get_adjacent_nodes(self, x, y):
        tiles = []

        try:
            tile = self.get(x, y-1)
            if tile.passable:
                tiles.append(tile)
        except IndexError as e:
            pass
        try:
            tile = self.get(x-1, y)
            if tile.passable:
                tiles.append(tile)
        except IndexError as e:
            pass
        try:
            tile = self.get(x, y+1)
            if tile.passable:
                tiles.append(tile)
        except IndexError as e:
            pass
        try:
            tile = self.get(x+1, y)
            if tile.passable:
                tiles.append(tile)
        except IndexError as e:
            pass

        return tiles


    def move_all(self):

        moved = list()

        for m in self.members:

            if type(m) == Passenger:
                moved.append(m)

                if m.path is not None:
                    x = m.xpos
                    y = m.ypos
                    step = m.next_move(self) #this updates pos within m !

                    # Has exited the grid, remove:
                    if step == (-1, -1):
                        self.pop(x, y)
                        #TODO:Should I really be returning here?
                        #return moved
                    else:
                        # Replace old tile with a floor tile
                        self.__put(Point('.', x, y), x, y)

                        # Put the passenger in the next move
                        self.__put(m, step[0], step[1])

        return moved


    def add_square_wall(self, top_left, side_length):

        items_to_add = list()

        for i in range(0, side_length):
            wall = self.build_horizontal_wall((top_left[0], top_left[1]+i), side_length)
            items_to_add.extend(wall)

        return items_to_add


    def build_horizontal_wall(self, top_left_position, length):
        walls = list()
        for i in range(0, length):
            wall = Point('#', top_left_position[0]+i, top_left_position[1], passable=False)
            walls.append(wall)

        self.load_elements(walls)
        return walls


    def build_vertical_wall(self, top_left_position, length):
        walls = list()
        for i in range(0, length):
            wall = Point('#', top_left_position[0], top_left_position[1]+i, passable=False)
            walls.append(wall)

        self.load_elements(walls)
        return walls


    def add_passenger_block(self, top_left_position, width, height):
        elements = list()
        pos = 0
        for i in range(0, height):
            for j in range(0, width):
                name = ascii_lowercase[pos % 26]
                pos += 1
                person = Passenger(name=name, xpos=top_left_position[0]+j,\
                    ypos=top_left_position[1]+i, cost=10, passable=True)
                elements.append(person)

        self.load_elements(elements)
        return elements

    def give_target_area(self, top_left_corner, ):
        pass
#
#
class CantPlotOnMap(Exception):
    pass
