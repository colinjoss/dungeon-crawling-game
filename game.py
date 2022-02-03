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
px = 320
py = 240

bg_img = pygame.image.load('img/grid2.png')


def round_multiple_32(n):
    if n % 32 != 0:
        return n - (n % 32)
    return n


map_size = bg_img.get_size()
x = 320 - round_multiple_32(map_size[0] // 2)
y = 240 - round_multiple_32(map_size[1] // 2)
n_bound = 240
w_bound = 320
s_bound = n_bound - map_size[1] + 32
e_bound = w_bound - map_size[0] + 32
print(f"N: {n_bound} E: {e_bound} S: {s_bound} W: {w_bound}")
print(x, y)


def player():
    screen.blit(player_img, (px, py))


def x_boundary(x, change):
    if x + change < e_bound or x + change > w_bound:
        return 0
    return change


def y_boundary(y, change):
    if y + change > n_bound or y + change < s_bound:
        return 0
    return change


# The game loop
running = True
while running:

    screen.blit(bg_img, (x, y))

    for event in pygame.event.get():            # When input is...

        if event.type == pygame.QUIT:           # Exit
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:      # Left arrow
                x += x_boundary(x, 32)
            if event.key == pygame.K_RIGHT:     # Right arrow
                x += x_boundary(x, -32)
            if event.key == pygame.K_UP:        # Up arrow
                y += y_boundary(y, 32)
            if event.key == pygame.K_DOWN:      # Down arrow
                y += y_boundary(y, -32)
            print(x, y)

    player()

    pygame.display.update()



