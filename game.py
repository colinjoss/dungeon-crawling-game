# Author: Colin Joss
# Last date updated: 2/2/2022

import pygame
from PIL import Image
import pygame_menu

pygame.init()


class Game:

    pygame.display.set_caption('Dungeon Explorer')      # Title

    SCREEN = pygame.display.set_mode((640, 480))        # The game window
    TITLE_MENU = pygame_menu.Menu('Welcome', 640, 480)
    PLAYER_IMG = pygame.image.load('img/player.png')    # Player image
    PLAYER_X = 320
    PLAYER_Y = 240

    def __init__(self):
        self.bg = pygame.image.load('img/grid1.png')
        self.map_size = self.bg.get_size()
        self.map_length = self.map_size[0] - 640
        self.map_height = self.map_size[1] - 640
        self.x = 320 - self.round_multiple_32(self.map_length // 2)
        self.y = 240 - self.round_multiple_32(self.map_height // 2)
        self.n_bound = -80
        self.w_bound = 0
        self.s_bound = self.n_bound - self.map_height + 32
        self.e_bound = self.w_bound - self.map_length + 32

        self.start()

    def start(self):
        self.game_loop()

    def game_loop(self):
        running = True
        while running:

            self.SCREEN.blit(self.bg, (self.x, self.y))

            for event in pygame.event.get():  # When input is...

                if event.type == pygame.QUIT:  # Exit
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:      # Left arrow
                        self.x += self.x_boundary(32)
                    if event.key == pygame.K_RIGHT:     # Right arrow
                        self.x += self.x_boundary(-32)
                    if event.key == pygame.K_UP:        # Up arrow
                        self.y += self.y_boundary(32)
                    if event.key == pygame.K_DOWN:      # Down arrow
                        self.y += self.y_boundary(-32)
                    print(self.x, self.y)

            self.player()

            pygame.display.update()

    def player(self):
        self.SCREEN.blit(self.PLAYER_IMG, (self.PLAYER_X, self.PLAYER_Y))

    def x_boundary(self, change):
        if self.x + change < self.e_bound or self.x + change > self.w_bound:
            return 0
        return change

    def y_boundary(self, change):
        if self.y + change > self.n_bound or self.y + change < self.s_bound:
            return 0
        return change

    @staticmethod
    def round_multiple_32(n):
        if n % 32 != 0:
            return n - (n % 32)
        return n


if __name__ == '__main__':
    Game()
