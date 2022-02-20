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


def generate_random_map(rows, columns, player=None):
    rows = rows + 24
    columns = columns + 24

    map = []
    for r in range(0, rows):
        if r < 12 or r > rows - 13:
            map.append(['B'] * columns)
        else:
            map.append((['B'] * 12) + (['.'] * (columns - 24)) + (['B'] * 12))

    if player is not None:
        map[player[0] + 12][player[1] + 12] = 'P'

    dr, dc = rd.randint(13, rows - 13), rd.randint(13, columns - 13)
    map[dr][dc] = next(door_count)

    # # West Door
    # map[rows//2][11] = '1'
    # # East Door
    # map[rows//2][columns - 12] = '1'
    # # North Door
    # map[11][columns//2] = '1'
    # # South Door
    # map[rows - 12][columns // 2] = '1'

    for row in map:
        print(row)

    return map
