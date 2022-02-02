# Author: Colin Joss
# Last date updated: 2/2/2022

import pygame
pygame.init()

# The game window
screen = pygame.display.set_mode((640, 480))

# Title and icon
pygame.display.set_caption('Dungeon Explorer')
# icon = pygame.image.load("file.png")
# pygame.display.set_icon(icon)

player_img = pygame.image.load('img/player.png')
x = 320
y = 240


def player():
    screen.blit(player_img, (x, y))


# The game loop
running = True
while running:

    screen.fill((255, 255, 255))

    for event in pygame.event.get():            # When input is...

        if event.type == pygame.QUIT:           # Exit
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:      # Left arrow
                x -= 32
            if event.key == pygame.K_RIGHT:     # Right arrow
                x += 32
            if event.key == pygame.K_UP:        # Up arrow
                y -= 32
            if event.key == pygame.K_DOWN:      # Down arrow
                y += 32

    player()

    pygame.display.update()



