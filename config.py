import pygame
pygame.init()

IMAGE_PATH = "C:\\Users\Colin\Desktop\Master Folder\Projects\Coding\CS361\dungeon-crawling-game\img\\bg"

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

LIFE = pygame.image.load('img/life.png')
LIFE.set_colorkey(NASTY_GREEN)

PROG = [1, 25, 50, 75, 100, 101]
REG = [-1, -1, 24, 49, 74, 99]

BACKGROUND = ['beach', 'space', 'mountain', 'garden', 'void']
HOME = 'img/bg/shore.jpg'

MENU_MUSIC = 'sound/music/menu.mp3'
OCEAN = 'sound/music/ocean.mp3'
SHOP = 'sound/music/shop.mp3'
HUZZAH = 'sound/music/menu_old.mp3'
MUSIC = ['sound/music/sunset.mp3', 'sound/music/funk.mp3', 'sound/music/wizard.mp3', 'sound/music/garden.mp3', OCEAN]


CHANGE_OPTION = pygame.mixer.Sound('sound/effects/change_option.wav')
SELECT = pygame.mixer.Sound('sound/effects/select.wav')
WALL = pygame.mixer.Sound('sound/effects/wall.wav')
EAT = pygame.mixer.Sound('sound/effects/bite.wav')
DOOR = pygame.mixer.Sound('sound/effects/door3.wav')
DAMAGE = pygame.mixer.Sound('sound/effects/damage.wav')
GAME_OVER = pygame.mixer.Sound('sound/effects/game_over.wav')
CLEAR = pygame.mixer.Sound('sound/effects/clear.wav')
ERROR = pygame.mixer.Sound('sound/effects/error.wav')
PURCHASE = pygame.mixer.Sound('sound/effects/purchase.wav')
VICTORY = pygame.mixer.Sound('sound/effects/clear.wav')
ZIPPERMOUTH = pygame.mixer.Sound('sound/effects/zippermouth.mp3')
TRY_AGAIN = pygame.mixer.Sound('sound/effects/shopkeep.mp3')
SAFE = pygame.mixer.Sound('sound/effects/safe.wav')

TITLE_FONT = pygame.font.Font('font/PressStart2P-Regular.ttf', 36)
TITLE_MENU_FONT = pygame.font.Font('font/PressStart2P-Regular.ttf', 22)
SMALL_FONT = pygame.font.Font('font/PressStart2P-Regular.ttf', 16)

WORLDS = ['desert', 'forest', 'ocean', 'mountain']
ITEM_CODES = ['Ch', 'Ba', 'Me', 'Gr', 'Or', 'Ap']
