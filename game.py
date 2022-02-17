# Author: Colin Joss
# Last date updated: 2/2/2022

import pygame
from config import *
from sprites import *
import sys
from PIL import Image
import random
from generate_bg import work


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font = ('freesansbold.ttf', 32)
        self.running = True

        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_tilemap()

    def create_tilemap(self):
        for y, row in enumerate(tilemap):
            for x, col in enumerate(row):
                if col == 'B':
                    Block(self, x, y)
                if col == 'P':
                    Player(self, x, y)

    def events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        pass

    def title_screen(self):
        pass

    def instructions_screen(self):
        pass




# class Game_old:
#
#     pygame.display.set_caption('Dungeon Explorer')      # Title
#     SCREEN = pygame.display.set_mode((672, 480))        # The game window
#     INSTRUCTIONS = pygame.image.load('img/instructions.png')
#     # TITLE_FONT = pygame.font.Font('freesansbold.ttf', 32)
#     # TITLE_MENU_FONT = pygame.font.Font('freesansbold.ttf', 28)
#     # BAG_MENU_FONT = pygame.font.Font('freesansbold.ttf', 24)
#     CENTER_SCREEN = (320, 240)
#
#     # MENU_MUSIC = 'sound/menu.mp3'
#     # OVERWORLD_MUSIC = 'sound/overworld.mp3'
#     # MENU_MOVE_SOUND = pygame.mixer.Sound('sound/menu_move_sound.wav')
#     # MENU_SELECT_SOUND = pygame.mixer.Sound('sound/menu_select_sound.wav')
#
#     MAP_THEMES = ['jungle', 'ocean']
#
#     def __init__(self):
#         self.map = self.new_dungeon('ocean600-1', 'img/jewel_blue.png')
#         self.player = Player(self.map.center)
#         self.title_menu()
#
#     def new_dungeon(self, theme, jewel):
#         return Map(theme, jewel)
#
#     def title_menu(self):
#         pygame.mixer.music.load(self.MENU_MUSIC)
#         pygame.mixer.music.play(-1)
#
#         title = self.TITLE_FONT.render('D U N G E O N', True, 'white')
#         title_surface = title.get_rect()
#         title_surface.center = (320, 150)
#
#         start_text = self.TITLE_MENU_FONT.render('start', True, 'red')
#         start_text_surface = start_text.get_rect()
#         start_text_surface.center = (320, 260)
#
#         quit_text = self.TITLE_MENU_FONT.render('quit', True, 'white')
#         quit_text_surface = quit_text.get_rect()
#         quit_text_surface.center = (320, 300)
#
#         start_select = True
#         running = True
#         while running:
#             self.SCREEN.fill((0, 0, 0))
#             self.SCREEN.blit(title, title_surface)
#             self.SCREEN.blit(start_text, start_text_surface)
#             self.SCREEN.blit(quit_text, quit_text_surface)
#
#             for event in pygame.event.get():
#
#                 if event.type == pygame.QUIT:           # Exit
#                     pygame.quit()
#
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_UP:        # Up arrow
#                         pygame.mixer.Sound.play(self.MENU_MOVE_SOUND)
#
#                         start_text = self.TITLE_MENU_FONT.render('start', True, 'red')
#                         start_text_surface = start_text.get_rect()
#                         start_text_surface.center = (320, 260)
#
#                         quit_text = self.TITLE_MENU_FONT.render('quit', True, 'white')
#                         quit_text_surface = quit_text.get_rect()
#                         quit_text_surface.center = (320, 300)
#
#                         start_select = True
#
#                     if event.key == pygame.K_DOWN:      # Down arrow
#                         pygame.mixer.Sound.play(self.MENU_MOVE_SOUND)
#
#                         start_text = self.TITLE_MENU_FONT.render('start', True, 'white')
#                         start_text_surface = start_text.get_rect()
#                         start_text_surface.center = (320, 260)
#
#                         quit_text = self.TITLE_MENU_FONT.render('quit', True, 'red')
#                         quit_text_surface = quit_text.get_rect()
#                         quit_text_surface.center = (320, 300)
#
#                         start_select = False
#
#                     if event.key == pygame.K_z and start_select is True:
#                         pygame.mixer.Sound.play(self.MENU_SELECT_SOUND)
#                         running = False
#
#                     if event.key == pygame.K_z and start_select is False:
#                         pygame.mixer.Sound.play(self.MENU_SELECT_SOUND)
#                         pygame.quit()
#
#                 pygame.display.update()
#
#         self.instructions()
#
#     def instructions(self):
#         running = True
#         while running:
#             self.SCREEN.blit(self.INSTRUCTIONS, (0, 0))
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:  # Exit
#                     pygame.quit()
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_z:
#                         pygame.mixer.Sound.play(self.MENU_SELECT_SOUND)
#                         running = False
#
#             pygame.display.update()
#
#         self.start()
#
#     def start(self):
#         pygame.mixer.music.stop()
#         pygame.mixer.music.load(self.OVERWORLD_MUSIC)
#         pygame.mixer.music.play(-1)
#         self.game_loop()
#
#     def game_loop(self):
#         surface = pygame.Surface([100, 100])
#         bg = pygame.image.load('img/ocean600-1.png')
#         map = bg.get_rect()
#
#
#         new_level = False
#         running = True
#         while running:
#
#             self.SCREEN.fill('white')
#             self.SCREEN.blit(bg, map)
#             self.SCREEN.blit(self.player.get_sprite(), (self.player.get_x(), self.player.get_y()))
#
#             if (self.player.get_x(), self.player.get_y()) == (-2976, -2064):
#                 new_level = True
#                 running = False
#
#             for event in pygame.event.get():  # When input is...
#
#                 # Hitting X button in game window
#                 if event.type == pygame.QUIT:  # Exit
#                     pygame.quit()
#
#                 if event.type == pygame.KEYDOWN:
#
#                     # Player movement
#                     if event.key == pygame.K_LEFT:
#                         self.player.move_left()
#                     if event.key == pygame.K_RIGHT:
#                         self.player.move_right()
#                     if event.key == pygame.K_UP:
#                         self.player.move_up()
#                     if event.key == pygame.K_DOWN:
#                         self.player.move_down()
#
#                     print('player:', self.player.get_x(), self.player.get_y())
#
#                     # Presses x (BAG MENU)
#                     if event.key == pygame.K_x:
#                         if self.bag_menu():
#                             running = False
#
#             pygame.display.update()
#
#         if new_level:
#             self.map = self.new_dungeon('ocean', 'img/jewel_blue.png')
#             self.player = Player((self.map.center[0], self.map.center[1]))
#             self.game_loop()
#         else:
#             self.title_menu()
#
#     def bag_menu(self):
#         items_text = self.BAG_MENU_FONT.render('items', True, 'red')
#         items_text_surface = items_text.get_rect()
#         items_text_surface.center = (320, 140)
#
#         settings_text = self.BAG_MENU_FONT.render('settings', True, 'white')
#         settings_text_surface = settings_text.get_rect()
#         settings_text_surface.center = (320, 200)
#
#         quit_text = self.BAG_MENU_FONT.render('quit game', True, 'white')
#         quit_text_surface = quit_text.get_rect()
#         quit_text_surface.center = (320, 260)
#
#         items_select = True
#         settings_select = False
#         quit_select = False
#         return_to_menu = False
#         running = True
#
#         while running:
#             self.SCREEN.fill((0, 0, 0))
#             self.SCREEN.blit(items_text, items_text_surface)
#             self.SCREEN.blit(settings_text, settings_text_surface)
#             self.SCREEN.blit(quit_text, quit_text_surface)
#
#             for event in pygame.event.get():
#
#                 if event.type == pygame.QUIT:  # Exit
#                     running = False
#
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_UP and quit_select is True:
#                         pygame.mixer.Sound.play(self.MENU_MOVE_SOUND)
#
#                         settings_text = self.BAG_MENU_FONT.render('settings', True, 'red')
#                         settings_text_surface = settings_text.get_rect()
#                         settings_text_surface.center = (320, 200)
#
#                         quit_text = self.BAG_MENU_FONT.render('quit game', True, 'white')
#                         quit_text_surface = quit_text.get_rect()
#                         quit_text_surface.center = (320, 260)
#
#                         settings_select = True
#                         quit_select = False
#
#                         break
#
#                     if event.key == pygame.K_UP and settings_select is True:
#                         pygame.mixer.Sound.play(self.MENU_MOVE_SOUND)
#
#                         items_text = self.BAG_MENU_FONT.render('items', True, 'red')
#                         items_text_surface = items_text.get_rect()
#                         items_text_surface.center = (320, 140)
#
#                         settings_text = self.BAG_MENU_FONT.render('settings', True, 'white')
#                         settings_text_surface = settings_text.get_rect()
#                         settings_text_surface.center = (320, 200)
#
#                         items_select = True
#                         settings_select = False
#
#                         break
#
#                     if event.key == pygame.K_DOWN and items_select is True:
#                         pygame.mixer.Sound.play(self.MENU_MOVE_SOUND)
#
#                         items_text = self.BAG_MENU_FONT.render('items', True, 'white')
#                         items_text_surface = items_text.get_rect()
#                         items_text_surface.center = (320, 140)
#
#                         settings_text = self.BAG_MENU_FONT.render('settings', True, 'red')
#                         settings_text_surface = settings_text.get_rect()
#                         settings_text_surface.center = (320, 200)
#
#                         settings_select = True
#                         items_select = False
#
#                         break
#
#                     if event.key == pygame.K_DOWN and settings_select is True:
#                         pygame.mixer.Sound.play(self.MENU_MOVE_SOUND)
#
#                         settings_text = self.BAG_MENU_FONT.render('settings', True, 'white')
#                         settings_text_surface = settings_text.get_rect()
#                         settings_text_surface.center = (320, 200)
#
#                         quit_text = self.BAG_MENU_FONT.render('quit game', True, 'red')
#                         quit_text_surface = quit_text.get_rect()
#                         quit_text_surface.center = (320, 260)
#
#                         quit_select = True
#                         settings_select = False
#
#                         break
#
#                     if event.key == pygame.K_z and items_select is True:
#                         pygame.mixer.Sound.play(self.MENU_SELECT_SOUND)
#                         print('ITEMS')
#
#                     if event.key == pygame.K_z and settings_select is True:
#                         pygame.mixer.Sound.play(self.MENU_SELECT_SOUND)
#                         print('SETTINGS')
#
#                     if event.key == pygame.K_z and quit_select is True:
#                         pygame.mixer.Sound.play(self.MENU_SELECT_SOUND)
#                         if self.quit_dialogue():
#                             return_to_menu = True
#                             running = False
#
#                     if event.key == pygame.K_ESCAPE:
#                         running = False
#
#                 pygame.display.update()
#
#         return return_to_menu
#
#     def quit_dialogue(self):
#         quit_title = self.TITLE_MENU_FONT.render('ALL PROGRESS WILL BE LOST. QUIT?', True, 'white')
#         quit_title_surface = quit_title.get_rect()
#         quit_title_surface.center = (320, 140)
#
#         yes_text = self.BAG_MENU_FONT.render('Yes', True, 'white')
#         yes_text_surface = yes_text.get_rect()
#         yes_text_surface.center = (320, 200)
#
#         no_text = self.BAG_MENU_FONT.render('No', True, 'Red')
#         no_text_surface = no_text.get_rect()
#         no_text_surface.center = (320, 260)
#
#         quit_select = False
#         running = True
#         while running:
#             self.SCREEN.fill((0, 0, 0))
#             self.SCREEN.blit(quit_title, quit_title_surface)
#             self.SCREEN.blit(yes_text, yes_text_surface)
#             self.SCREEN.blit(no_text, no_text_surface)
#
#             for event in pygame.event.get():
#
#                 if event.type == pygame.QUIT:  # Exit
#                     pygame.quit()
#
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_UP:
#                         pygame.mixer.Sound.play(self.MENU_MOVE_SOUND)
#
#                         yes_text = self.BAG_MENU_FONT.render('Yes', True, 'Red')
#                         yes_text_surface = yes_text.get_rect()
#                         yes_text_surface.center = (320, 200)
#
#                         no_text = self.BAG_MENU_FONT.render('No', True, 'White')
#                         no_text_surface = no_text.get_rect()
#                         no_text_surface.center = (320, 260)
#
#                         quit_select = True
#                         break
#
#                     if event.key == pygame.K_DOWN:
#                         pygame.mixer.Sound.play(self.MENU_MOVE_SOUND)
#
#                         yes_text = self.BAG_MENU_FONT.render('Yes', True, 'white')
#                         yes_text_surface = yes_text.get_rect()
#                         yes_text_surface.center = (320, 200)
#
#                         no_text = self.BAG_MENU_FONT.render('No', True, 'Red')
#                         no_text_surface = no_text.get_rect()
#                         no_text_surface.center = (320, 260)
#
#                         quit_select = False
#                         break
#
#                     if event.key == pygame.K_z:
#                         pygame.mixer.Sound.play(self.MENU_SELECT_SOUND)
#                         running = False
#
#                 pygame.display.update()
#
#         return quit_select
#
#
# class Map_old:
#
#     def __init__(self, theme, jewel):
#         self.bg = self.format_image(self.request_image(theme), jewel)
#         self.width = self.bg.get_size()[0] - 640
#         self.height = self.bg.get_size()[1] - 640
#         self.center = (0 - self.round_multiple_32(self.width//2), -80 - self.round_multiple_32(self.height//2))
#         self.n_bound = -80
#         self.w_bound = 0
#         self.s_bound = self.n_bound - self.height + 32
#         self.e_bound = self.w_bound - self.width + 32
#
#     def get_bg_image(self) -> pygame.image:
#         return self.bg
#
#     def get_width(self) -> int:
#         return self.width
#
#     def get_height(self) -> int:
#         return self.height
#
#     def get_center(self) -> tuple:
#         return self.center
#
#     def request_image(self, keyword):
#         # MICROSERVICE
#         filepath = 'img/' + keyword + '.png'
#         return filepath
#
#     def format_image(self, image, jewel):
#         bg = Image.open(image, 'r')  # Open image
#
#         # Crop image dimensions to multiple of 32
#         new_width = self.round_multiple_32(bg.size[0])
#         new_height = self.round_multiple_32(bg.size[1])  # Adjust dimensions to fit 32x32 grid
#         bg.crop((new_width, new_height, new_width, new_height))
#         bg.resize((new_width, new_height))
#
#         # Add jewel
#         gem = Image.open(jewel, 'r')
#         bg_with_jewel = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
#         bg_with_jewel.paste(bg, (0, 0))
#         bg_with_jewel.paste(gem, (
#             self.round_multiple_32(random.randint(0, new_width)),
#             self.round_multiple_32(random.randint(0, new_height))),
#             mask=gem)
#         gem.close()
#         bg.close()
#
#         # Add a black border
#         final_size = (new_width + 640, new_height + 640)  # Adjust dimensions again for black border
#         bg_with_border = Image.new('RGB', final_size)
#         bg_with_border.paste(bg_with_jewel, ((final_size[0] - new_width) // 2, (final_size[1] - new_height) // 2))
#         bg_with_jewel.close()
#
#         bg_with_border.save(image)
#         return pygame.image.load(image)
#
#     def round_multiple_32(self, n):
#         if n % 32 != 0:
#             return n - (n % 32)
#         return n
#
#     def player_at_x_boundary(self, x_coord):
#         if x_coord < self.e_bound or x_coord > self.w_bound:
#             return True
#         return False
#
#     def player_at_y_boundary(self, y_coord):
#         if y_coord > self.n_bound or y_coord < self.s_bound:
#             return True
#         return False
#
#     def get_random_x(self):
#         return self.round_multiple_32(random.randint(self.e_bound, self.w_bound))
#
#     def get_random_y(self):
#         return self.round_multiple_32(random.randint(self.s_bound, self.n_bound))
#
#
# class Player_old:
#
#     def __init__(self, center):
#         self.sprite = pygame.image.load('img/player1.png')
#         self.x = 32
#         self.y = 32
#         self.health_cap = 1
#         self.health_current = 1
#         self.items = {
#             'gold': 0,
#             'jewel': 0,
#             'potion': 1
#         }
#
#     def get_x(self):
#         return self.x
#
#     def get_y(self):
#         return self.y
#
#     def get_sprite(self):
#         return self.sprite
#
#     def get_current_health(self):
#         return self.health_current
#
#     def get_health_cap(self):
#         return self.health_cap
#
#     def get_items(self):
#         return self.items
#
#     def use_item(self, item):
#         if self.items[item] != 0:
#             self.items[item] -= 1
#
#         # Item effect
#
#     def increase_health(self, n):
#         self.health_current += n
#
#         if self.health_current > self.health_cap:
#             self.health_current = self.health_cap
#
#     def decrease_health(self, n):
#         self.health_current -= n
#
#         if self.health_current < 0:
#             self.health_current = 0
#
#     def increase_health_cap(self, n):
#         self.health_cap += n
#
#     def move_right(self):
#         self.x += 32
#
#     def move_left(self):
#         self.x += -32
#
#     def move_up(self):
#         self.y += -32
#
#     def move_down(self):
#         self.y += 32
#
#
# class Item:
#     def __init__(self, image, description):
#         self.image = pygame.image.load(image)
#         self.description = description
#
#
# class Jewel(Item):
#     def __init__(self, image, x, y):
#         super().__init__(image, 'A valuable jewel')
#         self.x = x
#         self.y = y
#
#     def get_image(self):
#         return self.image
#
#     def description(self):
#         return self.description
#
#     def get_x(self):
#         return self.x
#
#     def get_y(self):
#         return self.y


if __name__ == '__main__':
    game = Game()
    game.title_screen()
    while game.running:
        game.main()
