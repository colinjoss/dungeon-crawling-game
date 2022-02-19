WIN_WIDTH = 672
WIN_HEIGHT = 480
CENTER = (336, 240)

TILE_SIZE = 32

GROUND_LAYER = 0
BLOCK_LAYER = 1
PLAYER_LAYER = 2

UP = 'U'
DOWN = 'D'
RIGHT = 'R'
LEFT = 'L'

PLAYER_SPEED = 32

FPS = 60

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
NASTY_GREEN = (181, 230, 29)

tilemap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBB........................BBBBBBBBBB',
    'BBBBBBBBBB........................BBBBBBBBBB',
    'BBBBBBBBBB........................BBBBBBBBBB',
    'BBBBBBBBBB........................BBBBBBBBBB',
    'BBBBBBBBBB........................BBBBBBBBBB',
    'BBBBBBBBBB........................BBBBBBBBBB',
    'BBBBBBBBBB........................BBBBBBBBBB',
    'BBBBBBBBBB........................BBBBBBBBBB',
    'BBBBBBBBBB........................BBBBBBBBBB',
    'BBBBBBBBBB................P.......BBBBBBBBBB',
    'BBBBBBBBBB........................BBBBBBBBBB',
    'BBBBBBBBBB........................BBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
]


def generate_random_map(rows, columns, pr, pc):
    rows = rows + 24
    columns = columns + 24
    pr = pr + 12
    pc = pc + 12

    if not 12 <= pr < rows - 12 or not 12 <= pc < columns - 12:
        return False

    map = []
    for r in range(0, rows):

        if r < 12 or r > rows - 13:
            map.append('B' * columns)
        else:
            map.append('BBBBBBBBBBBB' + ('.' * (columns - 24)) + 'BBBBBBBBBBBB')

    map[pr] = map[pr][:pc] + 'P' + map[pr][pc + 1:]

    return map


# map = generate_random_map(5, 5, 4, 4)
# for row in map:
#     print(row)
