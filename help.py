import random as rd


class MapTree:
    def __init__(self):
        self.head = None


class MapNode:
    def __init__(self, n, data):
        self.room = n
        self.data = data
        self.bridges = {}


class BridgeNode:
    def __init__(self, next, spawn):
        self.next = next
        self.spawn = spawn


tree = MapTree()


def sequence():
    n = 0
    while True:
        yield n
        n += 1


door_count = sequence()
room_count = sequence()


def test():
    tree.head = generate_starting_maps()
    print('ROOM 0')
    print('from:', tree.head.room, 'to:', tree.head.bridges[1].next.room, 'at:', tree.head.bridges[1].spawn)
    # for key in tree.head.bridges[1].next.bridges:
    #     if tree.head.bridges[1].next.bridges[key] is not None:
    #         print(tree.head.bridges[1].next.bridges[key].next.room)
    #     else:
    #         print(tree.head.bridges[1].next.bridges[key])

    print('ROOM 1')
    node = generate_next_maps(tree.head.bridges[1].next)
    for key in node.bridges[2].next.bridges:
        if isinstance(node.bridges[2].next.bridges[key], BridgeNode):
            print(key, node.bridges[2].next.bridges[key].next.room)
        else:
            print(key, node.bridges[2].next.bridges[key])


def generate_starting_maps():

    rows0, columns0 = get_random_dimensions()       # Get random dimensions
    rows1, columns1 = get_random_dimensions()

    matrix0 = generate_room(rows0, columns0)        # Generate matrix for first and second rooms
    matrix1 = generate_room(rows1, columns1)

    door_list_0 = []                                # Place connecting door in first room
    create_door(door_list_0, rows0, columns0, matrix0, 0)

    create_player_spawn(rows0, columns0, matrix0)   # Place player in first room

    door_list_1 = []                                # Place 2 doors in second room
    create_door(door_list_1, rows1, columns1, matrix1, 0)
    create_door(door_list_1, rows1, columns1, matrix1, 1)

    room0 = MapNode(next(room_count), matrix0)      # Create map node for rooms
    room1 = MapNode(next(room_count), matrix1)

    bridge1 = BridgeNode(room1, door_list_1[0])     # Create bridges between first and second rooms
    bridge2 = BridgeNode(room0, door_list_0[0])

    room0.bridges[bridge1.next.room] = bridge1      # Connect rooms with bridges
    room1.bridges[bridge2.next.room] = bridge2

    add_bridge_placeholders(door_list_1, room1)     # Add bridge placeholders in second room

    return room0


def generate_next_maps(next_room):

    for i, key in enumerate(next_room.bridges):

        if i == 0:      # Skip first because it's already done
            continue

        rows, columns = get_random_dimensions()     # Get random dimensions
        matrix = generate_room(rows, columns)       # Create matrix

        door_list = []
        create_door(door_list, rows, columns, matrix, 0)    # Place door connecting to next room in new room

        new_room = MapNode(next(room_count), matrix)        # Create map node for new room

        bridge1 = BridgeNode(new_room, door_list[0])        # Create bridges between old room and new room(s)
        ret_spawn = next_room.bridges[key]
        next_room.bridges[key] = bridge1
        bridge2 = BridgeNode(next_room, ret_spawn)
        new_room.bridges[bridge2.next.room] = bridge2

        j = 1   # Place other doors
        while j < rd.randint(2, 3):
            if create_door(door_list, rows, columns, matrix, j) is False:
                continue
            j += 1

        add_bridge_placeholders(door_list, new_room)    # Add bridge placeholders in second room

        new_room.data = matrix

    return next_room


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


def create_door(door_list, rows, columns, matrix, index):
    d = next(door_count)
    d_coord = (rd.randint(13, rows - 14), rd.randint(13, columns - 14), d)

    for i in range(0, len(door_list)):
        if (d_coord[0], d_coord[1]) == (door_list[i], door_list[i]):
            return False

    door_list.append(d_coord)
    matrix[door_list[index][0]][door_list[index][1]] = d


def create_player_spawn(rows, columns, matrix):
    while True:
        player = (rows // 2), (columns // 2)
        if isinstance(matrix[player[0]][player[1]], int):
            continue
        matrix[player[0]][player[1]] = 'P'
        break


def add_bridge_placeholders(door_list, room):
    for i in range(1, len(door_list)):   # For every door past the first one...
        d = door_list[i][2]  # Get door number
        room.bridges[d] = door_list[i]  # Temporarily store return spawn for this door


# for i in range(0, len(door_list)):  # For every door past the first one...
#     dd = door_list[i][2]  # Get door number
#     new_room.bridges[dd] = door_list[i]  # Temporarily store return spawn for this door

# d = next(door_count)
# d_coord = (rd.randint(13, rows - 14), rd.randint(13, columns - 14), d)
# matrix[d_coord[0]][d_coord[1]] = d

# dd = next(door_count)
# door_list.append((rd.randint(13, rows - 14), rd.randint(13, columns - 14), dd))
#
# if (door_list[j][0], door_list[j][1]) == (d_coord[0], d_coord[1]):
#     continue
#
# matrix[door_list[j][0]][door_list[j][1]] = dd


test()
