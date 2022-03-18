# Author: Colin Joss
# Last date updated: 3/8/2022

import pygame
from config import *
from sprites import *
import level_generation as level
import rpyc


def sequence():
    n = 0
    while True:
        yield n
        n += 1


class Game:
    def __init__(self):

        # Fundamentals
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.player = None
        self.bg = None
        self.loc = None
        self.friend_eater = None
        self.shop = None

        self.door_count = sequence()
        self.room_count = sequence()

        # Sprite sheets
        self.character_sheet = SpriteSheet('img/player_sheet.png')
        self.enemy_sheet = SpriteSheet('img/enemy_sheet.png')
        self.npc_sheet = SpriteSheet('img/npc_sheet.png')
        self.terrain_sheet = SpriteSheet('img/terrain_sheet.png')
        self.door_sheet = SpriteSheet('img/door_sheet.png')
        self.items_sheet = SpriteSheet('img/items_sheet.png')
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.all_doors = pygame.sprite.LayeredUpdates()
        self.all_enemies = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.ground = pygame.sprite.LayeredUpdates()

        # Counts and tallies
        self.lives = 1
        self.fruit_count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.visited = [0]
        self.unvisited = 0
        self.depth = 0
        self.level = 0
        self.paths = 0
        self.unopened_doors = []
        self.locked_doors = []
        self.current_room = None
        self.invulnerable = False
        self.invulnerability_timer = 0

        # Special switches
        self.home = False
        self.challenge = False

        self.sprite_key = {'B': Block,
                           'S': ShopKeep,
                           'Ewb': WaddleBug,
                           'Egl': GrimLeaper,
                           'Eww': WaitWatch,
                           'Egf': None,
                           'Ezm': ZipperMouth,
                           'Ch': Cherry,
                           'Ba': Banana,
                           'Me': Melon,
                           'Gr': Grape,
                           'Or': Orange,
                           'Ap': Apple
                           }

    # Getters and setters

    def set_bg(self, new_bg):
        self.bg = pygame.image.load(new_bg)

    def set_current_location(self, new_loc):
        self.loc = new_loc

    # Incrementers and decrementers

    def increment_level(self):
        self.level += 1

    def decrement_level(self):
        self.level -= 1

    def increment_depth(self):
        self.depth += 1

    def increment_paths(self):
        self.paths += 1

    def decrement_paths(self):
        self.paths -= 1

    def increment_fruit_count(self, key):
        self.fruit_count[key] += 1

    def increment_lives(self):
        self.lives += 1

    def decrement_lives(self):
        self.lives -= 1

    # Adders and removers

    def add_to_visited(self, door):
        pass

    def add_to_unvisited(self, door):
        pass

    def remove_from_unvisited(self, door):
        pass

    # All the other junk

    def reset(self):
        """
        Resets key variables for a new game.
        """
        self.player = None
        self.lives = 1
        self.visited = [0]
        self.unvisited = 0
        self.depth = 0
        self.level = 0
        self.paths = 0
        self.unopened_doors = []
        self.locked_doors = []
        self.home = True
        self.door_count = sequence()
        self.room_count = sequence()
        self.friend_eater = None

    def start(self):
        """
        Starts new game by creating new map tree and initial maps.
        """
        tree = level.start_tree()
        tree.head, player = level.generate_starting_maps(self)
        self.load_room(tree.head, player)

    def load_room(self, room, player):
        """
        Loads the current dungeon room.
        """
        self.friend_eater = None
        self.invulnerable = True
        self.invulnerability_timer = pygame.time.get_ticks() + 1000
        self.set_current_location(room)  # Set incoming as current location
        room.data[player[0] + 1][player[1]] = 'P'  # Place player spawn in room data
        self.build_map(room)  # Translate map data to sprites
        room.data[player[0] + 1][player[1]] = '.'  # Remove player spawn
        self.center_camera(player)  # Center camera on player

    def build_map(self, room):
        """
        Loop through map data and create corresponding sprites.
        """
        for y, row in enumerate(room.data):
            for x, col in enumerate(row):
                Ground(self, x, y)
                if isinstance(col, int):  # If number, create door
                    self.place_door(col, x, y)
                elif col == '.':
                    continue
                elif col == 'P':  # If P, create player
                    self.player = Player(self, x, y)
                elif col == 'Efe':
                    self.friend_eater = FriendEater(self, x, y)
                else:  # Otherwise create sprite via sprite key
                    self.sprite_key[col](self, x, y)

    def place_door(self, col, x, y):
        """
        Create door sprite.
        """
        if col in self.locked_doors:  # Locked door
            Door(self, x, y, col, True, True)
        elif col in self.unopened_doors:  # Unlocked unopened door
            Door(self, x, y, col, False, True)
        else:  # Unlocked opened door
            Door(self, x, y, col, False, False)

    def center_camera(self, player):
        """
        Centers game camera on player spawn point.
        """
        for sprite in self.all_sprites:
            sprite.rect.x -= player[1] * TILE_SIZE
            sprite.rect.x += 10 * TILE_SIZE
            sprite.rect.y -= player[0] * TILE_SIZE
            sprite.rect.y += 6 * TILE_SIZE

    def keyboard_events(self):
        """
        Handles non-movement keyboard events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:
                self.player.check_facing_tile()

    def kill_map(self):
        """
        Kills all currently existing sprites.
        """
        for sprite in self.all_sprites:
            sprite.kill()

    def update(self):
        """
        Update sprites on the map.
        """
        self.check_invulnerability()
        self.check_victory()
        self.update_level()
        if self.loc.fruit == 0 and self.loc.cleared is False:
            self.unlock_all_doors()
            self.kill_all_enemies()
        self.all_sprites.update()

    def check_invulnerability(self):
        if self.invulnerability_timer < pygame.time.get_ticks():
            self.invulnerable = False

    def check_victory(self):
        if self.depth == 99:
            self.victory()

    def unlock_all_doors(self):
        """
        Loops through all door sprites and makes them unlocked.
        """
        for door in self.all_doors:
            door.unlock()

    def kill_all_enemies(self):
        """
        Loops through all enemy sprites and removes them.
        """
        for enemy in self.all_enemies:
            enemy.defeat()

    def draw(self):
        """
        Draws sprites to the screen.
        """
        self.screen.blit(self.bg, (0, 0))
        self.all_sprites.draw(self.screen)
        self.blit_lives()
        self.blit_fruit_count()
        self.clock.tick(FPS)
        pygame.display.update()

    def update_level(self):
        """
        Changes level background and music by player depth.
        """
        if self.home:  # Home room
            self.set_bg(HOME)
            self.play_song(OCEAN)
            self.home = False
            pygame.time.wait(500)
            self.play_sound(TRY_AGAIN)

        elif self.depth == 1 and self.level == 0:  # First room
            self.request_bg(BACKGROUND[self.level])
            self.play_song(MUSIC[self.level])
            self.increment_level()

        elif self.depth == PROG[self.level]:  # New level
            self.request_bg(BACKGROUND[self.level])
            self.play_song(MUSIC[self.level])
            self.increment_level()

        elif self.depth == REG[self.level]:  # Old level
            self.request_bg(BACKGROUND[self.level - 2])
            self.play_song(MUSIC[self.level - 2])
            self.decrement_level()

    def blit_lives(self):
        """
        Displays player lives in top left corner.
        """
        x = 0
        for life in range(0, self.lives):
            self.screen.blit(LIFE, (x, 0))
            x += TILE_SIZE

    def blit_fruit_count(self):
        """
        Displays player fruit count in top of screen.
        """
        # Blit fruit sprites to top left
        sprite_x, screen_x = 0, 182
        for fruit in range(0, 6):
            self.screen.blit(self.items_sheet.get_sprite(sprite_x, 0, 32, 32), (screen_x, 0))
            sprite_x += TILE_SIZE
            screen_x += 80

        # Blit fruit counts to top left
        screen_x = 214
        for i in range(0, 6):
            count = self.fruit_count[i]
            ones, tens, hunds = count % 10, count // 10, count // 100
            t = SMALL_FONT.render(str(hunds) + str(tens) + str(ones), True, 'white')
            t_rect = t.get_rect()
            t_rect.center = (screen_x, 0)
            self.screen.blit(t, (screen_x, 9))
            screen_x += 80

    def main(self):
        """
        Main game loop.
        """
        while self.playing:
            self.keyboard_events()
            self.update()
            self.draw()

    def game_over(self):
        """
        Displays game over screen and ends main game loop.
        """
        title = TITLE_FONT.render('GAME OVER', True, 'RED')
        title_rect = title.get_rect()
        title_rect.center = (336, 150)
        self.screen.fill((0, 0, 0))
        self.screen.blit(title, title_rect)
        pygame.display.update()
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(GAME_OVER)
        pygame.time.delay(3000)
        self.playing = False

    def victory(self):
        title = TITLE_FONT.render('CONGRATULATIONS!', True, 'BLUE')
        title_rect = title.get_rect()
        title_rect.center = (336, 150)
        self.screen.fill((0, 0, 0))
        self.screen.blit(title, title_rect)
        pygame.display.update()
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(VICTORY)
        pygame.time.delay(3000)
        self.playing = False

    def title_screen(self):
        """
        Displays interactive title screen.
        """
        self.running = True
        self.play_song(MENU_MUSIC)
        start_color, instruct_color, quit_color = 'red', 'white', 'white'
        while self.running:
            self.screen.fill((0, 0, 0))
            self.blit_big_text('D U N G E O N', 'blue', (336, 150))
            self.blit_small_text('START', start_color, (336, 260))
            self.blit_small_text('RULES', instruct_color, (336, 300))
            self.blit_small_text('QUIT', quit_color, (336, 340))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Exit
                    pygame.quit()
                start_color, instruct_color, quit_color = self.update_title_screen(
                    event, start_color, instruct_color, quit_color)
                if self.playing:
                    return
            pygame.display.update()

    def update_title_screen(self, event, start_color, instruct_color, quit_color):
        """
        Updates title screen based on keyboard input
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and instruct_color == 'red':    # Up arrow
                self.play_sound(CHANGE_OPTION)
                return 'red', 'white', 'white'
            if event.key == pygame.K_UP and quit_color == 'red':    # Up arrow
                self.play_sound(CHANGE_OPTION)
                return 'white', 'red', 'white'
            if event.key == pygame.K_DOWN and start_color == 'red':  # Up arrow
                self.play_sound(CHANGE_OPTION)
                return 'white', 'red', 'white'
            if event.key == pygame.K_DOWN and instruct_color == 'red':  # Down arrow
                self.play_sound(CHANGE_OPTION)
                return 'white', 'white', 'red'
            if event.key == pygame.K_z and quit_color == 'red':
                self.play_sound(SELECT)
                self.running = False
            if event.key == pygame.K_z and instruct_color == 'red':
                self.play_sound(SELECT)
                self.instructions_screen()
            if event.key == pygame.K_z and start_color == 'red':
                self.play_sound(SELECT)
                self.playing = True
        return start_color, instruct_color, quit_color

    def blit_big_text(self, text, color, pos):
        """
        Displays title text to the screen.
        """
        big_text = TITLE_FONT.render(text, True, color)
        big_text_rect = big_text.get_rect()
        big_text_rect.center = pos
        self.screen.blit(big_text, big_text_rect)

    def blit_small_text(self, text, color, pos):
        """
        Displays start option text to the screen.
        """
        small_text = TITLE_MENU_FONT.render(text, True, color)
        small_text_rect = small_text.get_rect()
        small_text_rect.center = pos
        self.screen.blit(small_text, small_text_rect)

    def play_song(self, song):
        """
        Plays given song indefinitely.
        """
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(-1)

    def play_sound(self, effect):
        """
        Plays given sound effect once.
        """
        pygame.mixer.Sound.play(effect)

    def request_bg(self, keyword):
        """
        Opens a connection with image microserviceand retrieves image matching given keyword.
        """
        conn = rpyc.connect("localhost", 18861)
        image = conn.root.exposed_get_image(keyword, IMAGE_PATH)
        self.set_bg(image)
        conn.close()

    def instructions_screen(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.blit_big_text('R U L E S', 'white', (336, 80))
            self.blit_small_text('EXPLORE A SPRAWLING DUNGEON', 'white', (336, 200))
            self.blit_small_text('FIND ALL THE FRUIT', 'white', (336, 240))
            self.blit_small_text('AVOID 5 UNIQUE ENEMIES', 'white', (336, 280))
            self.blit_small_text('BUY UPGRADES', 'white', (336, 320))
            self.blit_small_text('TRY AGAIN!', 'white', (336, 360))
            self.blit_small_text('PRESS Z TO RETURN TO MENU', 'red', (336, 400))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.play_sound(SELECT)
                        return
            pygame.display.update()

    def player_death(self):
        """
        Subtract life and respawn player, else end game.
        """
        self.decrement_lives()
        self.kill_map()
        self.screen.fill(BLACK)
        if self.lives == 0:
            self.game_over()
        else:
            self.invulnerable = True
            self.invulnerability_timer = pygame.time.get_ticks() + 1000
            self.load_room(self.loc, (len(self.loc.data) // 2, len(self.loc.data[0]) // 2))

    def traverse(self, door):
        """
        Travel into a new dungeon room.
        """
        self.player.rel_x, self.player.rel_y = 0, 0
        self.kill_map()
        self.screen.fill(BLACK)
        node = self.loc.bridges[door].room  # Get target room
        self.update_depth(node)
        self.play_sound(DOOR)
        player = self.loc.bridges[door].spawn  # Get player spawn coordinate
        self.player.movement_delay = pygame.time.get_ticks() + 2000
        self.shop = None
        self.load_room(node, player)

    def update_depth(self, node):
        """
        Update player depth
        """
        if node.num not in self.visited:  # New depth
            self.depth += 1
            node = level.generate_next_maps(self, node)
            self.visited.append(node.num)
        elif node.num in self.visited and self.loc.num < node.num:  # Depth reachieved
            self.depth += 1
        else:  # Backtracking
            self.depth -= 1

    def open_shop(self):
        return Shop(self)

    def trade(self):
        self.shop.open = True
        self.shop.menu()


class Shop:
    def __init__(self, game):
        self.game = game

        self.menu_1 = pygame.image.load('img/shop_menu_1.png')
        self.menu_1.set_colorkey(NASTY_GREEN)
        self.menu_2 = pygame.image.load('img/shop_menu_2.png')
        self.menu_2.set_colorkey(NASTY_GREEN)
        self.menu_3 = pygame.image.load('img/shop_menu_3.png')
        self.menu_3.set_colorkey(NASTY_GREEN)

        self.ware_count = 0
        self.trade_1 = self.restock()
        self.trade_2 = self.restock()
        self.trade_3 = self.restock()

        self.open = False

    def menu(self):
        active_menu = self.menu_1
        while self.open:
            self.game.screen.blit(active_menu, (192, 112))
            self.blit_trades()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:  # Exit
                    active_menu = self.scroll_shop_menu(event, active_menu)
                    if event.key == pygame.K_x:
                       self.open = False
                    if event.key == pygame.K_z:
                        self.purchase(active_menu)
            pygame.display.update()

    def blit_trades(self):
        y = 158
        for trade in [self.trade_1, self.trade_2, self.trade_3]:
            self.game.screen.blit(trade.cost_image, (218, y))          # Fruit cost !
            self.game.screen.blit(trade.ret_image, (354, y))          # Ware !
            self.blit_ware_price(trade.cost_count, (262, y+10))   # Price !
            self.blit_ware_price(trade.ret_count, (400, y+10))   # How many wares
            y += 64

    def blit_ware_price(self, price, pos):
        ones, tens, hunds = price % 10, (price // 10) % 10, price // 100
        t = SMALL_FONT.render(str(hunds) + str(tens) + str(ones), True, 'white')
        t_rect = t.get_rect()
        t_rect.center = pos
        self.game.screen.blit(t, pos)

    def scroll_shop_menu(self, event, active_menu):
        if event.key == pygame.K_UP:
            self.game.play_sound(CHANGE_OPTION)
            if active_menu == self.menu_2:
                active_menu = self.menu_1
            elif active_menu == self.menu_3:
                active_menu = self.menu_2
        elif event.key == pygame.K_DOWN:
            self.game.play_sound(CHANGE_OPTION)
            if active_menu == self.menu_1:
                active_menu = self.menu_2
            elif active_menu == self.menu_2:
                active_menu = self.menu_3
        return active_menu

    def purchase(self, selected):
        trade = None
        if selected == self.menu_1:
            trade = self.trade_1
        elif selected == self.menu_2:
            trade = self.trade_2
        elif selected == self.menu_3:
            trade = self.trade_3

        if self.game.fruit_count[trade.cost_code] >= trade.cost_count:
            self.game.fruit_count[trade.cost_code] -= trade.cost_count
            self.game.fruit_count[trade.ret_code] += trade.ret_count
            self.game.blit_fruit_count()
            self.game.play_sound(PURCHASE)
        else:
            self.game.play_sound(ERROR)

        if self.game.fruit_count[6] == 4:
            self.game.fruit_count[6] = 0
            self.game.increment_lives()

    def restock(self):
        if self.game.depth == 0 and not self.is_lives_full() and self.ware_count == 0:
            self.ware_count += 1
            return self.stock_life_shard()
        elif self.ware_count != 3:
            self.ware_count += 1
            return self.stock_random_fruit()

    def stock_life_shard(self):
        return Trade(self.game, int(rd.random() * 6), 6)

    def stock_random_fruit(self):
        return Trade(self.game, int(rd.random() * 6), int(rd.random() * 6))

    def is_shop_full(self):
        return self.ware_count == 3

    def is_lives_full(self):
        return self.game.lives == 5


class Trade:
    def __init__(self, game, cost_code, ret_code):
        self.game = game
        self.cost_code = cost_code
        self.ret_code = ret_code
        self.cost_image = None
        self.ret_image = None
        self.cost_count = None
        self.ret_count = None
        self.set_images()
        self.set_counts()
        self.active = True

    def set_images(self):
        self.cost_image = self.game.items_sheet.get_sprite(self.cost_code * 32, 0, 32, 32)
        self.cost_image.set_colorkey(NASTY_GREEN)
        self.ret_image = self.game.items_sheet.get_sprite(self.ret_code * 32, 0, 32, 32)
        self.ret_image.set_colorkey(NASTY_GREEN)

    def set_counts(self):
        if self.ret_code == 6:
            self.cost_count = self.game.lives * 20 + self.game.fruit_count[6] * 4
        else:
            self.cost_count = 2 + int(rd.random() * 3)
        self.ret_count = 1


if __name__ == '__main__':
    game = Game()
    while game.running:
        game.title_screen()
        if game.playing is True:
            game.reset()
            game.start()
        while game.playing:
            game.main()
