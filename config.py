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

FPS = 60

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
NASTY_GREEN = (181, 230, 29)

MENU_MUSIC = 'sound/menu.mp3'
OVERWORLD_MUSIC = 'sound/overworld.mp3'
CHANGE_OPTION = pygame.mixer.Sound('sound/change_option.wav')
SELECT = pygame.mixer.Sound('sound/select.wav')
WALL = pygame.mixer.Sound('sound/wall.wav')
EAT = pygame.mixer.Sound('sound/bite.wav')
