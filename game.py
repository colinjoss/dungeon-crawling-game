# Author: Colin Joss
# Last date updated: 2/2/2022

import pygame
from config import *
from sprites import *
import sys
import random
from generate_bg import work
import level_generation as level
import rpyc


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
        self.npc_sheet = SpriteSheet('img/npc_sheet.png')
        self.terrain_sheet = SpriteSheet('img/terrain_sheet.png')
        self.door_sheet = SpriteSheet('img/door_sheet.png')
        self.items_sheet = SpriteSheet('img/items_sheet.png')

        self.life = pygame.image.load('img/life.png')
        self.life.set_colorkey(NASTY_GREEN)
        self.lives = 3
        self.fruit_count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

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
        self.change = False
        self.progression = [1, 20, 40, 60, 80, 100]
        self.regression = [-1, -1, 19, 39, 59, 79]

        self.home = False
        self.shop = False
        self.challenge = False

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
        self.home = True

        tree = level.start_tree()
        tree.head, player = level.generate_starting_maps(self)
        self.loc = tree.head
        self.load_room(self.loc, player)

    def load_room(self, room, player):
        print(game.paths)
        self.loc = room
        room.data[player[0]+1][player[1]] = 'P'

        for y, row in enumerate(room.data):
            for x, col in enumerate(row):
                if col == 'B':
                    Block(self, x, y)
                elif col == 'P':
                    self.player = Player(self, x, y)
                elif col == 'S':
                    ShopKeep(self, x, y)
                elif col == 'Eb':
                    Blue(self, x, y)
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
                elif col == '..':
                    Ground(self, x, y, 1)
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

    def kill_map(self):
        for sprite in self.all_sprites:
            sprite.kill()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.change_level_by_depth()

        self.screen.blit(self.bg, (0, 0))
        self.all_sprites.draw(self.screen)

        self.blit_lives()
        self.blit_fruit_count()

        self.clock.tick(FPS)
        pygame.display.update()

    def change_level_by_depth(self):

        if self.home:
            self.bg = pygame.image.load(HOME)
            pygame.mixer.music.load(OCEAN)
            pygame.mixer.music.play(-1)
            self.home = False

        elif self.depth == 1 and self.level == 0:
            self.bg = pygame.image.load(BACKGROUND[self.level])
            pygame.mixer.music.load(MUSIC[self.level])
            pygame.mixer.music.play(-1)
            self.level += 1

        elif self.depth == self.progression[self.level]:
            # conn = rpyc.connect("IP", 18861)
            # image = conn.root.exposed_get_image("Forest", "C:\\Temp")
            self.bg = pygame.image.load(BACKGROUND[self.level])
            pygame.mixer.music.load(MUSIC[self.level])
            pygame.mixer.music.play(-1)
            self.level += 1

        elif self.depth == self.regression[self.level]:
            self.bg = pygame.image.load(BACKGROUND[self.level-2])
            pygame.mixer.music.load(MUSIC[self.level-2])
            pygame.mixer.music.play(-1)
            self.level -= 1


    def blit_lives(self):
        # Blit lives to top left
        x = 0
        for life in range(0, self.lives):
            self.screen.blit(self.life, (x, 0))
            x += 32

    def blit_fruit_count(self):
        # Blit fruit to top left
        x1, x2 = 0, 160
        for fruit in range(0, 6):
            self.screen.blit(self.items_sheet.get_sprite(x1, 0, 32, 32), (x2, 0))
            x1 += 32
            x2 += 80

        # Blit fruit counts to top left
        x = 192
        for i in range(0, 6):
            count = self.fruit_count[i]
            ones = count % 10
            tens = count // 10
            hunds = count // 100

            t = SMALL_FONT.render(str(hunds) + str(tens) + str(ones), True, 'white')
            t_rect = t.get_rect()
            t_rect.center = (x, 0)

            self.screen.blit(t, (x, 9))
            x += 80

    def main(self):
        while self.playing:
            self.button_events()
            self.update()
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
