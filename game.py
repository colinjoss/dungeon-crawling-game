# Author: Colin Joss
# Last date updated: 2/2/2022

import pygame
from config import *
from sprites import *
import sys
import random
from generate_bg import work
import level_generation as level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False

        self.bg = None
        self.music = None

        self.character_sheet = SpriteSheet('img/player_sheet.png')
        self.enemy_sheet = SpriteSheet('img/enemy_sheet.png')
        self.terrain_sheet = SpriteSheet('img/terrain_sheet.png')
        self.door_sheet = SpriteSheet('img/door_sheet.png')
        self.items_sheet = SpriteSheet('img/items_sheet.png')

        self.life = pygame.image.load('img/life.png')
        self.life.set_colorkey(NASTY_GREEN)
        self.lives = 3

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.all_sprites_not_player = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.player = None
        self.loc = None
        self.visited = [0]
        self.unvisited = 0
        self.depth = 0
        self.level = 0
        self.worlds = [0, 5, 10, 15, 20]
        self.paths = 0
        self.used_doors = []

    def start(self):
        self.lives = 3
        self.visited = [0]
        self.unvisited = 0
        self.depth = 0
        self.level = 0
        self.paths = 0
        self.used_doors = []

        tree = level.start_tree()
        tree.head, player = level.generate_starting_maps(self)
        self.loc = tree.head
        self.load_room(self.loc, player)

    def load_room(self, room, player):
        self.loc = room
        room.data[player[0]+1][player[1]] = 'P'

        for y, row in enumerate(room.data):
            for x, col in enumerate(row):
                if col == 'B':
                    Block(self, x, y)
                elif col == 'P':
                    self.player = Player(self, x, y)
                elif col == 'Eb':
                    Balloon(self, x, y)
                elif col == 'Ch':
                    Cherry(self, x, y)
                elif col == 'Ba':
                    Banana(self, x, y)
                elif col == 'Me':
                    Melon(self, x, y)
                elif col == 'Gr':
                    Grape(self, x, y)
                elif col == 'Or':
                    Orange(self, x, y)
                elif col == 'Ap':
                    Apple(self, x, y)
                elif isinstance(col, int):
                    if col in self.used_doors:
                        Door(self, x, y, col, True)
                    else:
                        Door(self, x, y, col, False)
                # elif col == '..':
                #     Ground(self, x, y, 1)
                else:
                    Ground(self, x, y, 0)

        room.data[player[0]+1][player[1]] = '.'

        # Shift room over by players location (puts player in corner)
        for sprite in self.all_sprites:
            sprite.rect.x -= player[1] * TILE_SIZE
            sprite.rect.y -= player[0] * TILE_SIZE

        # Shift room so player is in middle
        for sprite in self.all_sprites:
            sprite.rect.x += 10 * TILE_SIZE
            sprite.rect.y += 7 * TILE_SIZE

    def button_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def step_events(self):
        pass

    def kill_map(self):
        for sprite in self.all_sprites:
            sprite.kill()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        if self.depth == 20:
            pygame.quit()

        if self.depth == self.worlds[self.level]:
            self.bg = pygame.image.load(BACKGROUND[self.level])
            pygame.mixer.music.load(MUSIC[self.level])
            pygame.mixer.music.play(-1)
            self.level += 1

        self.screen.blit(self.bg, (0, 0))
        self.all_sprites.draw(self.screen)

        x = 0
        for life in range(0, self.lives):
            self.screen.blit(self.life, (x, 0))
            x += 32

        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.button_events()
            self.update()
            self.step_events()
            self.draw()

    def game_over(self):
        title = TITLE_FONT.render('GAME OVER', True, 'RED')
        title_rect = title.get_rect()
        title_rect.center = (336, 150)

        self.screen.fill((0, 0, 0))
        self.screen.blit(title, title_rect)
        pygame.display.update()
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(GAME_OVER)
        pygame.time.delay(5000)

        self.playing = False

    def title_screen(self):
        self.running = True

        pygame.mixer.music.load('sound/music/menu.mp3')
        pygame.mixer.music.play(-1)

        start_color = 'red'
        quit_color = 'white'

        menu = True
        while menu:

            title = TITLE_FONT.render('D U N G E O N', True, 'blue')
            title_rect = title.get_rect()
            title_rect.center = (336, 150)

            start_text = TITLE_MENU_FONT.render('START', True, start_color)
            start_text_rect = start_text.get_rect()
            start_text_rect.center = (336, 260)

            quit_text = TITLE_MENU_FONT.render('QUIT', True, quit_color)
            quit_text_rect = quit_text.get_rect()
            quit_text_rect.center = (336, 300)

            self.screen.fill((0, 0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(start_text, start_text_rect)
            self.screen.blit(quit_text, quit_text_rect)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:  # Exit
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:  # Up arrow
                        pygame.mixer.Sound.play(CHANGE_OPTION)
                        start_color = 'red'
                        quit_color = 'white'

                    if event.key == pygame.K_DOWN:  # Down arrow
                        pygame.mixer.Sound.play(CHANGE_OPTION)
                        start_color = 'white'
                        quit_color = 'red'

                    if event.key == pygame.K_z and quit_color == 'red':
                        pygame.mixer.Sound.play(SELECT)
                        menu = False
                        self.running = False

                    if event.key == pygame.K_z and start_color == 'red':
                        pygame.mixer.Sound.play(SELECT)
                        self.playing = True
                        return

            pygame.display.update()

    def select(self, text, text_rect):
        pass

    def unselect(self, text_rect):
        pass

    def instructions_screen(self):
        pass


if __name__ == '__main__':
    game = Game()
    while game.running:
        game.title_screen()
        if game.playing is True:
            game.start()
        while game.playing:
            game.main()
