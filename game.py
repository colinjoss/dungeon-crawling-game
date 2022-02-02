# Author: Colin Joss
# Last date updated: 2/2/2022

import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))    # The game window

# Title and icon
pygame.display.set_caption('Dungeon Explorer')
# pygame.display.set_icon(pygame.image.load("file.png"))

# The game loop
running = True
while running:

    for event in pygame.event.get():            # When input is...
        if event.type == pygame.QUIT:           # Exit
            running = False

    pygame.display.update()



