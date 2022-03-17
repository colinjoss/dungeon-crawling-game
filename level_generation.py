import random as rd
import math


class MapTree:
    """
    Represents the tree structure of randomly generated game levels.
    """
    def __init__(self):
        self.head = None
        
    def get_head(self):
        return self.head
    
    def set_head(self, head):
        self.head = head


class MapNode:
    """
    Represents an individual dungeon room.
    """
    def __init__(self, num, data, dimensions, fruit, fruit_coords):
        self.num = num
        self.data = data
        self.dimensions = dimensions
        self.fruit = fruit
        self.fruit_coords = fruit_coords
        self.bridges = {}
        self.cleared = False
        
    # Getters and setters    
    
    def get_num(self):
        return self.num
    
    def get_data(self):
        return self.data
    
    def get_bridges(self):
        return self.bridges
    
    # Incrementers and decrementers
    
    def decrement_fruit(self):
        self.fruit -= 1
        
    # Status functions
    
    def is_empty_fruit(self):
        return self.fruit == 0
        
    def is_clear(self):
        return self.cleared
    
    # Modify map
    
    def set_player(self, player):
        pass


class BridgeNode:
    """
    Represents a link between two dungeon rooms.
    """
    def __init__(self, room, spawn):
        self.room = room
        self.spawn = spawn
        
    def get_room(self):
        return self.room
    
    def get_spawn(self):
        return self.spawn


def sequence():
    n = 0
    while True:
        yield n
        n += 1


door_count = sequence()
room_count = sequence()


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

        seed = rd.random() * 100
        if seed > dead_seed:
            dead_end(current, key, game)
            continue

        node = new_map(game, get_random_dimensions(game), False)    # New dungeon
        door_data = {}
        corners = get_corners(node.dimensions)
        d_num, d_coord = create_door(node, door_data, corners, game)    # First door
        node.data[d_coord[0]][d_coord[1]] = d_num
        game.unopened_doors.pop()

        bridge_1 = BridgeNode(node, door_data[d_num])   # Connect first door to current room
        ret_spawn = current.bridges[key]
        current.bridges[key] = bridge_1
        bridge_2 = BridgeNode(current, ret_spawn)
        node.bridges[d_num] = bridge_2

        for i in range(0, get_total_doors()):   # Create up to three more doors
            d_num, d_coord = create_door(node, door_data, corners, game)
            node.data[d_coord[0]][d_coord[1]] = d_num
            node.bridges[d_num] = door_data[d_num]
            game.increment_paths()

    return current


def get_dead_end_probability(game):
    """
    Returns inverse probability of dead end depending on currently available paths
    """
    if game.paths < 3:
        return 101
    elif 3 <= game.paths < 5:
        return 90
    elif 5 <= game.paths < 7:
        return 70
    elif 7 <= game.paths < 9:
        return 50
    elif 9 <= game.paths < 11:
        return 30
    else:
        return 10


def dead_end(current, key, game):
    """
    Creates dead end room.
    """
    node = new_map(game, (5+24, 5+24), True)  # New dungeon
    door_data = {}
    corners = get_corners(node.dimensions)
    d_num, d_coord = create_door(node, door_data, corners, game)  # First door
    node.data[d_coord[0]][d_coord[1]] = d_num
    game.unopened_doors.pop()

    bridge_1 = BridgeNode(node, door_data[d_num])  # Connect first door to current room
    ret_spawn = current.bridges[key]
    current.bridges[key] = bridge_1
    bridge_2 = BridgeNode(current, ret_spawn)
    node.bridges[d_num] = bridge_2


def new_map(game, dimensions, empty):
    """
    Returns new map node with fruit and enemies placed.
    """
    data = generate_room(dimensions[0], dimensions[1])

    if empty:
        fruit = 0
        fruit_coords = []
    else:
        fruit, fruit_coords = place_items(data, dimensions[0], dimensions[1], game)
        place_enemies(data, dimensions[0], dimensions[1])

    return MapNode(next(room_count), data, dimensions, fruit, fruit_coords)


def create_first_node(game):
    """
    Returns first map node in new game along with door data and initial spawn point.
    """
    node = new_map(game, (6 + 24, 8 + 24), True)
    corners = get_corners(node.dimensions)
    node.data[corners[1][0]][corners[1][1]] = 'S'
    door_data = {}
    d_num, d_coord = create_door(node, door_data, [corners[-1]], game)
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
    d_num, d_coord = create_door(node, door_data, [corners[-1]], game)
    node.data[d_coord[0]][d_coord[1]] = d_num
    game.unopened_doors.pop()
    d_num, d_coord = create_door(node, door_data, [corners[-2]], game)
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


def create_door(node, door_data, corners, game):
    """
    Gets new door number and door spawn point.
    """
    d_num = next(door_count)                        # Increment the door count
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
    n = get_total_items()
    items = ['Ch', 'Ba', 'Me', 'Gr', 'Or', 'Ap']
    coords = []
    count = 0
    while count < n:
        r, c = math.floor(rd.random() * (rows - 28)), math.floor(rd.random() * (columns - 28))
        if data[r + 14][c + 14] == '.':
            data[r + 14][c + 14] = items[math.floor(rd.random() * 6)]
            count += 1
            coords.append((r+14, c+14))
    return count, coords


def get_total_items():
    """
    Returns number of items based on current depth (NOT YET IMPLEMENTED)
    """
    return 3


def place_enemies(matrix, rows, columns):
    """
    Randomly places enemies in the dungeon room.
    """
    enemies = ['Efe']
    n = get_total_enemies()
    for i in range(0, n):
        r = math.floor(rd.random() * (rows - 24))
        c = math.floor(rd.random() * (columns - 24))
        if matrix[r + 12][c + 12] == '.':
            matrix[r + 12][c + 12] = enemies[math.floor(rd.random() * 1)]


def get_total_enemies():
    """
    Returns number of enemies based on current depth and level (NOT YET IMPLEMENTED)
    """
    return 1


def get_random_dimensions(game):
    """
    Returns random room dimensions. Size range increases with player depth.
    """
    rows, columns = rd.randint(6, 10) + game.depth, rd.randint(6, 10) + game.depth  # Get random dimensions
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
