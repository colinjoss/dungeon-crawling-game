import random as rd
import math


class MapTree:
    def __init__(self):
        self.head = None


class MapNode:
    def __init__(self, num, data):
        self.num = num
        self.data = data
        self.bridges = {}


class BridgeNode:
    def __init__(self, room, spawn):
        self.room = room
        self.spawn = spawn


def sequence():
    n = 0
    while True:
        yield n
        n += 1


door_count = sequence()
room_count = sequence()


def start_tree():
    return MapTree()


def generate_starting_maps(game):

    rows0, columns0 = 9+24, 9+24                          # Get random dimensions
    rows1, columns1 = get_random_dimensions()

    matrix0 = generate_room(rows0, columns0)        # Generate matrix for first and second rooms
    matrix1 = generate_room(rows1, columns1)

    randomize_items(matrix0, rows0, columns0)
    randomize_items(matrix1, rows1, columns1)
    randomize_enemies(matrix1, rows1, columns1)

    door_nums_0, door_coords_0 = [], []             # Place connecting door in first room
    corners = get_door_coordinates(rows0, columns0)
    create_door(door_nums_0, door_coords_0, corners, matrix0)

    player = create_player_spawn(rows0, columns0, matrix0)   # Place player in first room

    door_nums_1, door_coords_1 = [], []                      # Place 2 doors in second room
    corners = get_door_coordinates(rows1, columns1)
    create_door(door_nums_1, door_coords_1, corners, matrix1)
    game.used_doors.append(door_nums_1[0])
    create_door(door_nums_1, door_coords_1, corners, matrix1)
    game.paths += 1

    room0 = MapNode(next(room_count), matrix0)      # Create map node for rooms
    room1 = MapNode(next(room_count), matrix1)

    bridge1 = BridgeNode(room1, door_coords_1[0])     # Create bridges between first and second rooms
    bridge2 = BridgeNode(room0, door_coords_0[0])

    room0.bridges[door_nums_0[0]] = bridge1         # Connect rooms with bridges
    room1.bridges[door_nums_1[0]] = bridge2

    add_bridge_placeholders(door_nums_1, door_coords_1, room1)     # Add bridge placeholders in second room

    return room0, player


def generate_next_maps(game, room):
    game.paths -= 1

    for i, key in enumerate(room.bridges):

        if i == 0:      # Skip first because it's already done
            continue

        rows, columns = get_random_dimensions()     # Get random dimensions
        matrix = generate_room(rows, columns)       # Create matrix

        randomize_items(matrix, rows, columns)      # Place items
        randomize_enemies(matrix, rows, columns)

        door_nums, door_coords = [], []
        corners = get_door_coordinates(rows, columns)
        create_door(door_nums, door_coords, corners, matrix)    # Place door connecting in new room
        game.used_doors.append(door_nums[0])

        new_room = MapNode(next(room_count), matrix)    # Create map node for new room

        bridge1 = BridgeNode(new_room, door_coords[0])  # Create bridge to new room
        ret_spawn = room.bridges[key]   # Save coord in cur room
        room.bridges[key] = bridge1

        bridge2 = BridgeNode(room, ret_spawn)
        new_room.bridges[door_nums[0]] = bridge2

        for i in range(0, get_total_doors()):
            create_door(door_nums, door_coords, corners, matrix)
            game.paths += 1

        add_bridge_placeholders(door_nums, door_coords, new_room)    # Add bridge placeholders in second room

        new_room.data = matrix

    return room


def get_total_doors():
    seed = int(rd.random() * 100)
    doors = 1           # 100% chance of second door
    if seed >= 50:      # 50% chance of third door
        doors += 1
    if seed >= 85:      # 15% chance of fourth door
        doors += 1
    return doors


def generate_room(rows, columns):
    # Generate the matrix
    matrix = []
    for r in range(0, rows):
        if r < 12 or r > rows - 13:
            matrix.append(['B'] * columns)
        else:
            # floor = (['.'] * (columns - 24))
            floor = randomize_floor(columns - 24)
            matrix.append((['B'] * 12) + floor + (['B'] * 12))

    return matrix


def randomize_floor(length):
    ground = ['.', '..']
    result = []
    for i in range(0, length):
        result.append(ground[math.floor(2 * rd.random())])
    return result


def randomize_items(matrix, rows, columns):
    res = rd.random()
    n = 0
    if res > 0.99:      # Ten items
        n = 5
    elif res > 0.90:    # Five items
        n = 3
    elif res > 0.70:    # Three items
        n = 2
    elif res > 0.50:    # One item
        n = 1
    place_items(matrix, rows, columns, n)


def place_items(matrix, rows, columns, n):
    items = ['Ch', 'Ba', 'Me', 'Gr', 'Or', 'Ap']
    for i in range(0, n):
        r = math.floor(rd.random() * (rows - 24))
        c = math.floor(rd.random() * (columns - 24))
        if matrix[r+12][c+12] == '.' or matrix[r+12][c+12] == '..':
            matrix[r+12][c+12] = items[math.floor(rd.random() * 6)]


def randomize_enemies(matrix, rows, columns):
    res = int(rd.random() * 100)
    n = 1
    if res > 90:        # Four enemies
        n = 4
    elif res > 80:      # Three enemies
        n = 3
    elif res > 50:      # Two enemies
        n = 2
    place_enemies(matrix, rows, columns, n)


def place_enemies(matrix, rows, columns, n):
    enemies = ['Eb']
    for i in range(0, n):
        r = math.floor(rd.random() * (rows - 24))
        c = math.floor(rd.random() * (columns - 24))
        if matrix[r + 12][c + 12] == '.' or matrix[r + 12][c + 12] == '..':
            matrix[r + 12][c + 12] = enemies[math.floor(rd.random() * 1)]


def get_random_dimensions():
    rows, columns = rd.randint(10, 16), rd.randint(10, 16)  # Get random dimensions
    rows, columns = rows + 24, columns + 24  # Adjust rows/columns for border
    return rows, columns


def create_door(door_nums, door_coords, corners, matrix):
    d_num = next(door_count)                        # Increment the door count
    door_nums.append(d_num)                         # Save door number

    index = math.floor(rd.random() * len(corners))  # Randomly get index
    d_coord = corners[index]                        # Get corner coord
    door_coords.append(d_coord)                     # Save coordinate
    del corners[index]                              # Delete coordinate from corners

    matrix[d_coord[0]][d_coord[1]] = d_num          # Assign door to map


def get_door_coordinates(rows, columns):
    n, e, s, w = get_room_edge(rows, columns)
    return [(n+1, w+1), (n+1, e-1), (s-1, e-1), (s-1, w+1)]


def create_player_spawn(rows, columns, matrix):
    while True:
        player = (rows // 2), (columns // 2)
        if isinstance(matrix[player[0]][player[1]], int):
            continue
        break
    return player


def add_bridge_placeholders(door_nums, door_coords, room):
    for i in range(1, len(door_nums)):      # For every door past the first one...
        d_num = door_nums[i]                # Get door
        d_coord = door_coords[i]
        room.bridges[d_num] = d_coord       # Temporarily store return spawn for this door


def get_room_edge(rows, columns):
    return 12, columns-13, rows-13, 12
