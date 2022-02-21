from game import *
from config import *
import pygame
import random as rd


def sequence():
    n = 0
    while True:
        yield n
        n += 1


door_count = sequence()
room_count = sequence()


def generate_random_map(game, rows, columns, starting, door):
    rows = rows + 24
    columns = columns + 24

    map = []
    for r in range(0, rows):
        if r < 12 or r > rows - 13:
            map.append(['B'] * columns)
        else:
            map.append((['B'] * 12) + (['.'] * (columns - 24)) + (['B'] * 12))

    if starting:
        dr, dc = rd.randint(13, rows - 14), rd.randint(13, columns - 14)
        map[dr][dc] = next(door_count)
        player = (rows // 2), (columns // 2)
        if isinstance(map[player[0] + 12][player[1] + 12], int):
            player[0] - 1
    else:
        dr, dc = rd.randint(13, rows - 14), rd.randint(13, columns - 14)
        map[dr][dc] = next(door_count)
        player = dr+1, dc

    map[player[0]][player[1]] = 'P'

    game.room = next(room_count)
    game.maps[game.room] = []
    game.maps[game.room].append(map)
    game.maps[game.room].append([player[0], player[1]])

    for key in game.maps:
        print(game.maps[key])
    print('\n\n\n')

    return map
