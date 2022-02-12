# Author: Colin Joss
# Last date updated: 2/2/2022

import pygame
from PIL import Image


pygame.init()


class Game:

    pygame.display.set_caption('Dungeon Explorer')      # Title
    SCREEN = pygame.display.set_mode((640, 480))        # The game window
    INSTRUCTIONS = pygame.image.load('img/instructions.png')
    TITLE_FONT = pygame.font.Font('freesansbold.ttf', 32)
    TITLE_MENU_FONT = pygame.font.Font('freesansbold.ttf', 28)
    BAG_MENU_FONT = pygame.font.Font('freesansbold.ttf', 24)
    CENTER = (320, 240)

    def __init__(self):
        self.map = Map()
        self.player = Player(self.map.get_center()[0][0], self.map.get_center()[1])

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

        self.instructions()

    def instructions(self):
        running = True
        while running:
            self.SCREEN.blit(self.INSTRUCTIONS, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Exit
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        running = False

            pygame.display.update()

        self.start()

    def start(self):
        self.game_loop()

    def game_loop(self):
        running = True
        while running:

            self.SCREEN.blit(self.map.get_bg_image(), (self.player.get_x(), self.player.get_y()))

            for event in pygame.event.get():  # When input is...

                # Hitting X button in game window
                if event.type == pygame.QUIT:  # Exit
                    running = False

                if event.type == pygame.KEYDOWN:

                    # Player movement
                    if event.key == pygame.K_LEFT:
                        if not self.map.player_at_x_boundary(self.player.get_x() + 32):
                            self.player.move_left()
                    if event.key == pygame.K_RIGHT:
                        if not self.map.player_at_x_boundary(self.player.get_x() + -32):
                            self.player.move_right()
                    if event.key == pygame.K_UP:
                        if not self.map.player_at_y_boundary(self.player.get_y() + 32):
                            self.player.move_up()
                    if event.key == pygame.K_DOWN:
                        if not self.map.player_at_y_boundary(self.player.get_y() + -32):
                            self.player.move_down()

                    print(self.player.get_x(), self.player.get_y())

                    # Presses x (BAG MENU)
                    if event.key == pygame.K_x:
                        self.bag_menu()

            self.SCREEN.blit(self.player.get_sprite(), (self.CENTER[0], self.CENTER[1]))

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
                        self.quit_dialogue()

                    if event.key == pygame.K_ESCAPE:
                        running = False

                pygame.display.update()

    def quit_dialogue(self):
        quit_title = self.TITLE_MENU_FONT.render('ALL PROGRESS WILL BE LOST. QUIT?', True, 'white')
        quit_title_surface = quit_title.get_rect()
        quit_title_surface.center = (320, 140)

        yes_text = self.BAG_MENU_FONT.render('Yes', True, 'white')
        yes_text_surface = yes_text.get_rect()
        yes_text_surface.center = (320, 200)

        no_text = self.BAG_MENU_FONT.render('No', True, 'Red')
        no_text_surface = no_text.get_rect()
        no_text_surface.center = (320, 260)

        quit_select = False
        running = True
        while running:
            self.SCREEN.fill((0, 0, 0))
            self.SCREEN.blit(quit_title, quit_title_surface)
            self.SCREEN.blit(yes_text, yes_text_surface)
            self.SCREEN.blit(no_text, no_text_surface)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:  # Exit
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        yes_text = self.BAG_MENU_FONT.render('Yes', True, 'Red')
                        yes_text_surface = yes_text.get_rect()
                        yes_text_surface.center = (320, 200)

                        no_text = self.BAG_MENU_FONT.render('No', True, 'White')
                        no_text_surface = no_text.get_rect()
                        no_text_surface.center = (320, 260)

                        quit_select = True
                        break

                    if event.key == pygame.K_DOWN:
                        yes_text = self.BAG_MENU_FONT.render('Yes', True, 'white')
                        yes_text_surface = yes_text.get_rect()
                        yes_text_surface.center = (320, 200)

                        no_text = self.BAG_MENU_FONT.render('No', True, 'Red')
                        no_text_surface = no_text.get_rect()
                        no_text_surface.center = (320, 260)

                        quit_select = False
                        break

                    if event.key == pygame.K_z:
                        running = False

                pygame.display.update()

        if quit_select:
            pass
        else:
            pass


class Map:

    def __init__(self):
        self.bg = self.get_new_bg()
        self.size = self.bg.get_size()
        self.width = self.size[0] - 640
        self.height = self.size[1] - 640
        self.n_bound = -80
        self.w_bound = 0
        self.s_bound = self.n_bound - self.height + 32
        self.e_bound = self.w_bound - self.width + 32

    def get_bg_image(self):
        return self.bg

    def get_size(self):
        return self.size

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_center(self):
        x = 320 - self.round_multiple_32(self.get_width() // 2),
        y = 240 - self.round_multiple_32(self.get_height() // 2)
        return x, y

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

    def round_multiple_32(self, n):
        if n % 32 != 0:
            return n - (n % 32)
        return n

    def player_at_x_boundary(self, x_coord):
        if x_coord < self.e_bound or x_coord > self.w_bound:
            return True
        return False

    def player_at_y_boundary(self, y_coord):
        if y_coord > self.n_bound or y_coord < self.s_bound:
            return True
        return False


class Player:

    def __init__(self, x, y):
        self.sprite = pygame.image.load('img/player1.png')
        self.x = x
        self.y = y
        self.health_cap = 1
        self.health_current = 1
        self.items = {
            'gold': 0,
            'jewel': 0,
            'potion': 1
        }

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_sprite(self):
        return self.sprite

    def get_current_health(self):
        return self.health_current

    def get_health_cap(self):
        return self.health_cap

    def get_items(self):
        return self.items

    def use_item(self, item):
        if self.items[item] != 0:
            self.items[item] -= 1

        # Item effect

    def increase_health(self, n):
        self.health_current += n

        if self.health_current > self.health_cap:
            self.health_current = self.health_cap

    def decrease_health(self, n):
        self.health_current -= n

        if self.health_current < 0:
            self.health_current = 0

    def increase_health_cap(self, n):
        self.health_cap += n

    def move_right(self):
        self.x += -32

    def move_left(self):
        self.x += 32

    def move_up(self):
        self.y += 32

    def move_down(self):
        self.y += -32


if __name__ == '__main__':
    Game()
