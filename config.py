import pygame
import random as rd
pygame.init()

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
ENEMY_SPEED = 1

FPS = 60

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
NASTY_GREEN = (181, 230, 29)

BACKGROUND = ['img/bg/sunset.jpg', 'img/bg/space.jpg', 'img/bg/snow.jpg', 'img/bg/garden.jpg']
MUSIC = ['sound/music/sunset.mp3', 'sound/music/funk.mp3', 'sound/music/wizard.mp3', 'sound/music/garden.mp3']

MENU_MUSIC = 'sound/music/menu.mp3'

CHANGE_OPTION = pygame.mixer.Sound('sound/effects/change_option.wav')
SELECT = pygame.mixer.Sound('sound/effects/select.wav')
WALL = pygame.mixer.Sound('sound/effects/wall.wav')
EAT = pygame.mixer.Sound('sound/effects/bite.wav')
DOOR = pygame.mixer.Sound('sound/effects/door3.wav')
DAMAGE = pygame.mixer.Sound('sound/effects/damage.wav')
GAME_OVER = pygame.mixer.Sound('sound/effects/game_over.wav')

TITLE_FONT = pygame.font.Font('font/PressStart2P-Regular.ttf', 36)
TITLE_MENU_FONT = pygame.font.Font('font/PressStart2P-Regular.ttf', 22)
SMALL_FONT = pygame.font.Font('font/PressStart2P-Regular.ttf', 16)
