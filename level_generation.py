import random as rd


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


# def test():
#     tree = start_tree()
#     tree.head, player = generate_starting_maps()
#
#     node = generate_next_maps(tree.head.bridges[0].room)
#     print('sdfsdf')

    # for key in node.bridges[2].next.bridges:
    #     if isinstance(node.bridges[2].next.bridges[key], BridgeNode):
    #         print(key, node.bridges[2].next.bridges[key].next.room)
    #     else:
    #         print(key, node.bridges[2].next.bridges[key])


def start_tree():
    return MapTree()


def generate_starting_maps():

    rows0, columns0 = get_random_dimensions()       # Get random dimensions
    rows1, columns1 = get_random_dimensions()

    matrix0 = generate_room(rows0, columns0)        # Generate matrix for first and second rooms
    matrix1 = generate_room(rows1, columns1)

    door_nums_0, door_coords_0 = [], []             # Place connecting door in first room
    create_door(door_nums_0, door_coords_0, rows0, columns0, matrix0)

    player = create_player_spawn(rows0, columns0, matrix0)   # Place player in first room

    door_nums_1, door_coords_1 = [], []                      # Place 2 doors in second room
    create_door(door_nums_1, door_coords_1, rows1, columns1, matrix1)
    create_door(door_nums_1, door_coords_1, rows1, columns1, matrix1)

    room0 = MapNode(next(room_count), matrix0)      # Create map node for rooms
    room1 = MapNode(next(room_count), matrix1)

    bridge1 = BridgeNode(room1, door_coords_1[0])     # Create bridges between first and second rooms
    bridge2 = BridgeNode(room0, door_coords_0[0])

    room0.bridges[door_nums_0[0]] = bridge1         # Connect rooms with bridges
    room1.bridges[door_nums_1[0]] = bridge2

    add_bridge_placeholders(door_nums_1, door_coords_1, room1)     # Add bridge placeholders in second room

    return room0, player


def generate_next_maps(room):

    for i, key in enumerate(room.bridges):
        if i == 0:      # Skip first because it's already done
            continue

        rows, columns = get_random_dimensions()     # Get random dimensions
        matrix = generate_room(rows, columns)       # Create matrix

        door_nums, door_coords = [], []
        create_door(door_nums, door_coords, rows, columns, matrix)  # Place door connecting in new room

        new_room = MapNode(next(room_count), matrix)        # Create map node for new room

        bridge1 = BridgeNode(new_room, door_coords[0])    # Create bridge to new room
        ret_spawn = room.bridges[key]   # Save coord in cur room
        room.bridges[key] = bridge1

        bridge2 = BridgeNode(room, ret_spawn)
        new_room.bridges[door_nums[0]] = bridge2

        for i in range(0, rd.randint(1, 2)):
            create_door(door_nums, door_coords, rows, columns, matrix)

        add_bridge_placeholders(door_nums, door_coords, new_room)    # Add bridge placeholders in second room

        new_room.data = matrix

    return room


def generate_room(rows, columns):
    # Generate the matrix
    matrix = []
    for r in range(0, rows):
        if r < 12 or r > rows - 13:
            matrix.append(['B'] * columns)
        else:
            matrix.append((['B'] * 12) + (['.'] * (columns - 24)) + (['B'] * 12))
    return matrix


def get_random_dimensions():
    rows, columns = rd.randint(10, 21), rd.randint(10, 21)  # Get random dimensions
    rows, columns = rows + 24, columns + 24  # Adjust rows/columns for border
    return rows, columns


def create_door(door_nums, door_coords, rows, columns, matrix):
    d_num = next(door_count)
    d_coord = (rd.randint(13, rows - 14), rd.randint(13, columns - 14))

    # Make sure coordinate is acceptable
    i = 0
    while i < len(door_coords):
        if d_coord == door_coords[i]:
            continue
        i += 1

    # or 2 > abs(d_coord[0] - door_coords[i][0]) or 2 > abs(d_coord[1] - door_coords[i][1])

    door_nums.append(d_num)
    door_coords.append(d_coord)

    matrix[d_coord[0]][d_coord[1]] = d_num


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
