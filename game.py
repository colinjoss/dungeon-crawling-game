# Author: Colin Joss
# Last date updated: 2/2/2022

import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))    # The game window

running = True
while running:     # The game loop
    for event in pygame.event.get():        # When input is...
        if event.type == pygame.QUIT:       # Exit
            running = False

