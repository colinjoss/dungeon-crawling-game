# Author: Colin Joss
# Last date updated: 2/2/2022

import pygame
from PIL import Image
import pygame_menu

pygame.init()


class Game:

    pygame.display.set_caption('Dungeon Explorer')      # Title

    SCREEN = pygame.display.set_mode((640, 480))        # The game window
    TITLE_FONT = pygame.font.Font('freesansbold.ttf', 32)
    TITLE_MENU_FONT = pygame.font.Font('freesansbold.ttf', 28)
    BAG_MENU_FONT = pygame.font.Font('freesansbold.ttf', 24)


    PLAYER_IMG = pygame.image.load('img/player1.png')    # Player image
    PLAYER_X = 320
    PLAYER_Y = 240

    def __init__(self):
        self.bg = self.get_new_bg()
        self.map_size = self.get_map_size()
        self.map_width = self.map_size[0] - 640
        self.map_height = self.map_size[1] - 640
        self.x = 320 - self.round_multiple_32(self.map_width // 2)
        self.y = 240 - self.round_multiple_32(self.map_height // 2)
        self.n_bound = -80
        self.w_bound = 0
        self.s_bound = self.n_bound - self.map_height + 32
        self.e_bound = self.w_bound - self.map_width + 32

        self.title_menu()

    def title_menu(self):
        title = self.TITLE_FONT.render('D U N G E O N', True, 'white')
        title_surface = title.get_rect()
        title_surface.center = (320, 150)

        start_text = self.TITLE_MENU_FONT.render('start', True, 'red')
        start_text_surface = start_text.get_rect()
        start_text_surface.center = (320, 260)

        quit_text = self.TITLE_MENU_FONT.render('quit', True, 'white')
        quit_text_surface = quit_text.get_rect()
        quit_text_surface.center = (320, 300)

        start_select = True
        running = True
        while running:
            self.SCREEN.fill((0, 0, 0))
            self.SCREEN.blit(title, title_surface)
            self.SCREEN.blit(start_text, start_text_surface)
            self.SCREEN.blit(quit_text, quit_text_surface)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:           # Exit
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:        # Up arrow
                        start_text = self.TITLE_MENU_FONT.render('start', True, 'red')
                        start_text_surface = start_text.get_rect()
                        start_text_surface.center = (320, 260)

                        quit_text = self.TITLE_MENU_FONT.render('quit', True, 'white')
                        quit_text_surface = quit_text.get_rect()
                        quit_text_surface.center = (320, 300)

                        start_select = True

                    if event.key == pygame.K_DOWN:      # Down arrow
                        start_text = self.TITLE_MENU_FONT.render('start', True, 'white')
                        start_text_surface = start_text.get_rect()
                        start_text_surface.center = (320, 260)

                        quit_text = self.TITLE_MENU_FONT.render('quit', True, 'red')
                        quit_text_surface = quit_text.get_rect()
                        quit_text_surface.center = (320, 300)

                        start_select = False

                    if event.key == pygame.K_z and start_select is True:
                        running = False

                    if event.key == pygame.K_z and start_select is False:
                        pygame.quit()

                pygame.display.update()

        self.start()

    def start(self):
        self.game_loop()

    def game_loop(self):
        running = True
        while running:

            self.SCREEN.blit(self.bg, (self.x, self.y))

            for event in pygame.event.get():  # When input is...

                # Hitting X button in game window
                if event.type == pygame.QUIT:  # Exit
                    running = False

                # Player movement
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

                # Presses x (BAG MENU)
                if event.key == pygame.K_x:
                    self.bag_menu()

            self.player()

            pygame.display.update()

    def bag_menu(self):
        items_text = self.BAG_MENU_FONT.render('items', True, 'red')
        items_text_surface = items_text.get_rect()
        items_text_surface.center = (320, 140)

        settings_text = self.BAG_MENU_FONT.render('settings', True, 'white')
        settings_text_surface = settings_text.get_rect()
        settings_text_surface.center = (320, 200)

        quit_text = self.BAG_MENU_FONT.render('quit game', True, 'white')
        quit_text_surface = quit_text.get_rect()
        quit_text_surface.center = (320, 260)

        items_select = True
        settings_select = False
        quit_select = False
        running = True
        while running:
            self.SCREEN.fill((0, 0, 0))
            self.SCREEN.blit(items_text, items_text_surface)
            self.SCREEN.blit(settings_text, settings_text_surface)
            self.SCREEN.blit(quit_text, quit_text_surface)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:  # Exit
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and quit_select is True:
                        settings_text = self.BAG_MENU_FONT.render('settings', True, 'red')
                        settings_text_surface = settings_text.get_rect()
                        settings_text_surface.center = (320, 200)

                        quit_text = self.BAG_MENU_FONT.render('quit game', True, 'white')
                        quit_text_surface = quit_text.get_rect()
                        quit_text_surface.center = (320, 260)

                        settings_select = True
                        quit_select = False

                        break

                    if event.key == pygame.K_UP and settings_select is True:
                        items_text = self.BAG_MENU_FONT.render('items', True, 'red')
                        items_text_surface = items_text.get_rect()
                        items_text_surface.center = (320, 140)

                        settings_text = self.BAG_MENU_FONT.render('settings', True, 'white')
                        settings_text_surface = settings_text.get_rect()
                        settings_text_surface.center = (320, 200)

                        items_select = True
                        settings_select = False

                        break

                    if event.key == pygame.K_DOWN and items_select is True:
                        items_text = self.BAG_MENU_FONT.render('items', True, 'white')
                        items_text_surface = items_text.get_rect()
                        items_text_surface.center = (320, 140)

                        settings_text = self.BAG_MENU_FONT.render('settings', True, 'red')
                        settings_text_surface = settings_text.get_rect()
                        settings_text_surface.center = (320, 200)

                        settings_select = True
                        items_select = False

                        break

                    if event.key == pygame.K_DOWN and settings_select is True:
                        settings_text = self.BAG_MENU_FONT.render('settings', True, 'white')
                        settings_text_surface = settings_text.get_rect()
                        settings_text_surface.center = (320, 200)

                        quit_text = self.BAG_MENU_FONT.render('quit game', True, 'red')
                        quit_text_surface = quit_text.get_rect()
                        quit_text_surface.center = (320, 260)

                        quit_select = True
                        settings_select = False

                        break

                    if event.key == pygame.K_z and items_select is True:
                        print('ITEMS')

                    if event.key == pygame.K_z and settings_select is True:
                        print('SETTINGS')

                    if event.key == pygame.K_z and quit_select is True:
                        pygame.quit()

                    if event.key == pygame.K_ESCAPE:
                        running = False

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

    def round_multiple_32(self, n):
        if n % 32 != 0:
            return n - (n % 32)
        return n

    def get_map_size(self):
        return self.bg.get_size()

    def get_new_bg(self):
        filepath = self.request_image()
        return self.formatted_bg(filepath)

    def request_image(self):
        # MICROSERVICE
        filepath = 'img/jungle.jpg'
        return filepath

    def formatted_bg(self, filepath):
        bg = Image.open(filepath)                   # Open image
        width, height = bg.size                     # Get dimensions
        width = self.round_multiple_32(width)
        height = self.round_multiple_32(height)     # Adjust dimensions to fit 32x32 grid
        bg.crop((width, height, width, height))
        cropped_size = (width, height)              # Crop image
        bg.resize(cropped_size)

        new_size = (width + 640, height + 640)      # Adjust dimensions again for black border
        bg_border = Image.new("RGB", new_size)
        bg_border.paste(bg, ((new_size[0] - width) // 2, (new_size[1] - height) // 2))

        bg_border.save('img/bg_jungle.jpg')         # Save as new image (temporary)
        return pygame.image.load('img/bg_jungle.jpg')


if __name__ == '__main__':
    Game()
