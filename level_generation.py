import random as rd
import math
from config import *


class MapTree:
    """
    Represents the tree structure of randomly generated game levels.
    """
    def __init__(self):
        self.head = None
        
    def get_head(self):
        """
        Returns the head of the maptree.
        """
        return self.head
    
    def set_head(self, node):
        """
        Sets given node as the head of the maptree.
        """
        self.head = node


class MapNode:
    """
    Represents an individual dungeon room.
    """
    def __init__(self, num, data, dimensions, fruit):
        self.num = num
        self.data = data
        self.dimensions = dimensions
        self.fruit = fruit
        self.bridges = {}
        self.cleared = False
        
    # Getters and setters    
    
    def get_num(self):
        """
        Returns the map number.
        """
        return self.num
    
    def get_data(self):
        """
        Returns map data.
        """
        return self.data
    
    def get_bridges(self):
        """
        Returns bridge data.
        """
        return self.bridges

    def get_fruit_count(self):
        """
        Returns the current fruit count.
        """
        return self.fruit
    
    # Incrementers and decrementers
    
    def decrement_fruit(self):
        """
        Decrements the fruit counter by 1.
        """
        self.fruit -= 1
        
    # Status functions
    
    def is_empty_fruit(self):
        """
        Returns true if no fruit, else false.
        """
        return self.fruit == 0
        
    def is_clear(self):
        """
        Returns true if room cleared, false otherwise.
        """
        return self.cleared


class BridgeNode:
    """
    Represents a link between two dungeon rooms.
    """
    def __init__(self, node, spawn):
        self.node = node
        self.spawn = spawn
        
    def get_node(self):
        """
        Returns the connected node.
        """
        return self.node
    
    def get_spawn(self):
        """
        Returns the player spawn in the connected node.
        """
        return self.spawn


def start_tree():
    """
    Returns map tree object.
    """
    return MapTree()


def generate_starting_maps(game):
    """
    Creates first two maps.
    """
    node_1, door_data_1, player = create_first_node(game)   # First dungeon room
    node_2, door_data_2 = create_second_node(game)          # Second dungeon room
    game.increment_paths()
    bridge_1 = BridgeNode(node_2, door_data_2[1])   # Bridge from door 0 -> 1
    bridge_2 = BridgeNode(node_1, door_data_1[0])   # Bridge from door 1 -> 0
    node_1.bridges[0] = bridge_1
    node_2.bridges[1] = bridge_2
    node_2.bridges[2] = door_data_2[2]  # Set door 2 to spawn coordinates temporarily
    return node_1, player


def generate_next_maps(game, current):
    """
    Creates as many new rooms as are doors in the incoming room.
    """
    game.decrement_paths()
    dead_seed = get_dead_end_probability(game)
    for i, key in enumerate(current.bridges):   # Create as many rooms as there are unlinked doors
        if i == 0:      # Always skip first door - already bridged
            continue
        if game.depth == 99:
            generate_end_room(game, current, key)
            continue
        seed = rd.random() * 100
        if seed > dead_seed:
            dead_end(current, key, game)
            continue

        node, d_num, d_coord, door_data, corners = new_room_with_door(game)
        connect_new_room(node, door_data, d_num, current, key)
        add_doors(node, door_data, corners, game)
    return current


def new_room_with_door(game, dimensions=None, empty=False):
    """
    Creates a new map node with one door.
    """
    if dimensions is None:
        dimensions = get_random_dimensions(game)
    node = new_map(game, dimensions, empty)  # New dungeon
    door_data = {}
    corners = get_corners(node.dimensions)
    d_num, d_coord = create_door(door_data, corners, game)  # First door
    node.data[d_coord[0]][d_coord[1]] = d_num
    game.unopened_doors.pop()
    return node, d_num, d_coord, door_data, corners


def connect_new_room(node, door_data, d_num, current, key):
    """
    Connects a new node to the current node with a bridge.
    """
    bridge_1 = BridgeNode(node, door_data[d_num])  # Connect first door to current room
    ret_spawn = current.bridges[key]
    current.bridges[key] = bridge_1
    bridge_2 = BridgeNode(current, ret_spawn)
    node.bridges[d_num] = bridge_2


def add_doors(node, door_data, corners, game):
    """
    Adds a random number of doors (between 1 -3 more) to the new map node.
    """
    for i in range(0, get_total_doors()):  # Create up to three more doors
        d_num, d_coord = create_door(door_data, corners, game)
        node.data[d_coord[0]][d_coord[1]] = d_num
        node.bridges[d_num] = door_data[d_num]
        game.increment_paths()


def generate_end_room(game, current, key):
    """
    Creates the final map oof the game.
    """
    node, d_num, d_coord, door_data, corners = new_room_with_door(game, (50, 50))
    connect_new_room(node, door_data, d_num, current, key)
    d_num, d_coord = create_door(door_data, corners, game)
    node.data[d_coord[0]][d_coord[1]] = d_num
    node.bridges[d_num] = door_data[d_num]
    game.increment_paths()


def get_dead_end_probability(game):
    """
    Returns inverse probability of dead end depending on currently available paths
    """
    if game.paths < 3:
        return 101
    elif 3 <= game.paths < 5:
        return 90
    elif 5 <= game.paths < 7:
        return 80
    elif 7 <= game.paths < 9:
        return 70
    elif 9 <= game.paths < 11:
        return 60
    else:
        return 50


def dead_end(current, key, game):
    """
    Creates dead end room.
    """
    node = empty_dead_end(current, key, game)
    seed = int(rd.random() * 100)
    if seed < 50:
        treasure_dead_end(node)


def empty_dead_end(current, key, game):
    """
    Creates an empty dead end room.
    """
    node, d_num, d_coord, door_data, corners = new_room_with_door(game, (5 + 24, 5 + 24), True)
    connect_new_room(node, door_data, d_num, current, key)
    return node


def treasure_dead_end(node):
    """
    Fills an empty dead end room with fruit.
    """
    for i, row in enumerate(node.data):
        for j, col in enumerate(node.data):
            if node.data[i][j] == '.':
                node.data[i][j] = ITEM_CODES[math.floor(rd.random() * 6)]


def new_map(game, dimensions, empty):
    """
    Returns new map node with fruit and enemies placed.
    """
    data = generate_room(dimensions[0], dimensions[1])

    if empty:
        fruit = 0
    else:
        fruit = place_items(data, dimensions[0], dimensions[1], game)
        place_enemies(data, dimensions[0], dimensions[1], game)

    return MapNode(next(game.room_count), data, dimensions, fruit)


def create_first_node(game):
    """
    Returns first map node in new game along with door data and initial spawn point.
    """
    node = new_map(game, (6 + 24, 8 + 24), True)
    corners = get_corners(node.dimensions)
    node.data[corners[1][0]][corners[1][1]] = 'S'
    door_data = {}
    d_num, d_coord = create_door(door_data, [corners[-1]], game)
    node.data[d_coord[0]][d_coord[1]] = d_num
    player = create_player_spawn(node)
    return node, door_data, player


def create_second_node(game):
    """
    Returns second map node in new game along with door data.
    """
    node = new_map(game, get_random_dimensions(game), True)
    corners = get_corners(node.dimensions)
    door_data = {}
    d_num, d_coord = create_door(door_data, [corners[-1]], game)
    node.data[d_coord[0]][d_coord[1]] = d_num
    game.unopened_doors.pop()
    d_num, d_coord = create_door(door_data, [corners[-2]], game)
    node.data[d_coord[0]][d_coord[1]] = d_num
    return node, door_data


def get_total_doors():
    """
    Returns total number of doors for the new room.
    """
    seed = int(rd.random() * 100)
    doors = 1           # 100% chance of second door
    if seed >= 50:      # 50% chance of third door
        doors += 1
    if seed >= 85:      # 15% chance of fourth door
        doors += 1
    return doors


def create_door(door_data, corners, game):
    """
    Gets new door number and door spawn point.
    """
    d_num = next(game.door_count)                        # Increment the door count
    index = math.floor(rd.random() * len(corners))  # Randomly get index
    d_coord = corners[index]                        # Get corner coord
    door_data[d_num] = d_coord                      # Save coordinate
    del corners[index]                              # Delete coordinate from corners

    if d_num != 0:
        game.locked_doors.append(d_num)
    game.unopened_doors.append(d_num)

    return d_num, d_coord


def generate_room(rows, columns):
    """
    Creates the data for new dungeon in form of 2D matrix.
    """
    matrix = []
    for r in range(0, rows):
        if r < 12 or r > rows - 13:
            matrix.append(['B'] * columns)
        else:
            floor = (['.'] * (columns - 24))
            matrix.append((['B'] * 12) + floor + (['B'] * 12))
    return matrix


def place_items(data, rows, columns, game):
    """
    Randomly places items in the dungeon room.
    """
    n = get_total_items(game)
    items = ['Ch', 'Ba', 'Me', 'Gr', 'Or', 'Ap']
    count = 0
    while count < n:
        r, c = math.floor(rd.random() * (rows - 28)), math.floor(rd.random() * (columns - 28))
        if data[r + 14][c + 14] == '.':
            data[r + 14][c + 14] = items[math.floor(rd.random() * 6)]
            count += 1
    return count


def get_total_items(game):
    """
    Returns number of items based on current depth (NOT YET IMPLEMENTED)
    """
    return 1 + (game.depth // 5)


def place_enemies(matrix, rows, columns, game):
    """
    Randomly places enemies in the dungeon room.
    """
    i = 0
    while i < get_total_enemies(game):
        r = math.floor(rd.random() * (rows - 24))
        c = math.floor(rd.random() * (columns - 24))
        if matrix[r + 14][c + 14] == '.':
            matrix[r + 14][c + 14] = get_enemy(game)
            i += 1


def get_enemy(game):
    """
    Returns a random enemy code with probabilities based on the current player level.
    """
    probability = {}
    if game.level == 1:
        probability = LV1_ENEMY
    elif game.level == 2:
        probability = LV2_ENEMY
    elif game.level == 3:
        probability = LV3_ENEMY
    elif game.level == 4:
        probability = LV4_ENEMY

    for key in probability:
        if int(rd.random() * 100) <= key:
            return probability[key]
    return '.'


def get_total_enemies(game):
    """
    Returns number of enemies based on current depth and level (NOT YET IMPLEMENTED)
    """
    return 1 + (game.depth // 4)


def get_random_dimensions(game):
    """
    Returns random room dimensions. Size range increases with player depth.
    """
    rows, columns = rd.randint(6, 10) + game.depth // 4, rd.randint(6, 10) + game.depth // 4  # Get random dimensions
    rows, columns = rows + 24, columns + 24  # Adjust rows/columns for border
    return rows, columns


def get_corners(dimensions):
    """
    Returns the coordinates of a dungeon room's corners.
    """
    n, e, s, w = get_room_edge(dimensions[0], dimensions[1])
    return [(n+1, w+1), (n+1, e-1), (s-1, e-1), (s-1, w+1)]


def create_player_spawn(node):
    """
    Returns the coordinates of a player's spawn point.
    """
    player = (node.dimensions[0] // 2), (node.dimensions[1] // 2)
    return player


def get_room_edge(rows, columns):
    """
    Returns the edges of a given room.
    """
    return 12, columns-13, rows-13, 12
