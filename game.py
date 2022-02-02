# Author: Colin Joss
# Last date updated: 2/2/2022

import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))    # The game window

# Title and icon
pygame.display.set_caption('Dungeon Explorer')
# icon = pygame.image.load("file.png")
# pygame.display.set_icon(icon)

player_img = pygame.image.load('img/player.png')
player_x = 320
player_y = 240


def player():
    screen.blit(player_img, (player_x, player_y))


# The game loop
running = True
while running:

    screen.fill((255, 255, 255))

    for event in pygame.event.get():            # When input is...
        if event.type == pygame.QUIT:           # Exit
            running = False

    player()

    pygame.display.update()



