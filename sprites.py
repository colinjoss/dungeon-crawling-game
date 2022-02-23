import pygame
from config import *
import level_generation as level
import math
import random
import time


class SpriteSheet:
    def __init__(self, sheet):
        self.sheet = pygame.image.load(sheet).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(NASTY_GREEN)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.movement_delay = 0
        self.sound_delay = 0

        self.facing = 'down'
        self.animation_loop = 0

        self.image = self.game.character_sheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.rel_x = self.x
        self.rel_y = self.y

        self.down_animations = [
            self.game.character_sheet.get_sprite(0, 0, self.width, self.height),
            self.game.character_sheet.get_sprite(0, 32, self.width, self.height),
            self.game.character_sheet.get_sprite(0, 64, self.width, self.height),
            self.game.character_sheet.get_sprite(0, 96, self.width, self.height)
        ]
        self.up_animations = [
            self.game.character_sheet.get_sprite(32, 0, self.width, self.height),
            self.game.character_sheet.get_sprite(32, 32, self.width, self.height),
            self.game.character_sheet.get_sprite(32, 64, self.width, self.height),
            self.game.character_sheet.get_sprite(32, 96, self.width, self.height)
        ]
        self.left_animations = [
            self.game.character_sheet.get_sprite(64, 0, self.width, self.height),
            self.game.character_sheet.get_sprite(64, 32, self.width, self.height),
            self.game.character_sheet.get_sprite(64, 64, self.width, self.height),
            self.game.character_sheet.get_sprite(64, 96, self.width, self.height)
        ]
        self.right_animations = [
            self.game.character_sheet.get_sprite(96, 0, self.width, self.height),
            self.game.character_sheet.get_sprite(96, 32, self.width, self.height),
            self.game.character_sheet.get_sprite(96, 64, self.width, self.height),
            self.game.character_sheet.get_sprite(96, 96, self.width, self.height)
        ]

    def update(self):
        if self.movement_delay < pygame.time.get_ticks():

            self.movement_delay = pygame.time.get_ticks() + 80

            self.move_direction()       # Gets keyboard input; sets x/y change  and facing direction

            if self.collide_block('x') or self.collide_block('y'):    # Tests move - if collides, do not update

                if self.sound_delay < pygame.time.get_ticks():
                    self.sound_delay = pygame.time.get_ticks() + 320
                    pygame.mixer.Sound.play(WALL)

                self.x_change = 0
                self.y_change = 0
                return

            self.rel_x += self.x_change
            self.rel_y += self.y_change

            self.animate_movement()
            self.check_ground()

        self.x_change = 0
        self.y_change = 0

    def move_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = LEFT
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = RIGHT
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = DOWN
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = UP

    def collide_block(self, direction):
        if direction == 'x':
            self.rect.x += self.x_change
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            self.rect.x -= self.x_change
            return True if hits else False

        if direction == 'y':
            self.rect.y += self.y_change
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            self.rect.y -= self.y_change
            return True if hits else False

    def animate_movement(self):
        start = 0
        animation_frame = 16
        end = 32

        if self.animation_loop == 2:
            self.animation_loop = 0

        if self.facing == DOWN:
            if self.y_change == 0:
                self.image = self.game.character_sheet.get_sprite(0, 0, self.width, self.height)
                self.animation_loop = 0
            else:
                while start != end:
                    self.rect.y += 4

                    if start == animation_frame:
                        self.animation_loop += 1
                        self.image = self.down_animations[self.animation_loop]

                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= 4

                    self.game.draw()

                    start += 4

                self.y_change = 0

        if self.facing == UP:
            if self.y_change == 0:
                self.image = self.game.character_sheet.get_sprite(32, 0, self.width, self.height)
                self.animation_loop = 0
            else:
                while start != end:
                    self.rect.y -= 4

                    if start == animation_frame:
                        self.animation_loop += 1
                        self.image = self.up_animations[self.animation_loop]

                    for sprite in self.game.all_sprites:
                        sprite.rect.y += 4

                    self.game.draw()

                    start += 4

                self.y_change = 0

        if self.facing == LEFT:
            if self.x_change == 0:
                self.image = self.game.character_sheet.get_sprite(64, 0, self.width, self.height)
                self.animation_loop = 0
            else:
                while start != end:
                    self.rect.x -= 4

                    for sprite in self.game.all_sprites:
                        sprite.rect.x += 4

                    if start == animation_frame:
                        self.animation_loop += 1
                        self.image = self.left_animations[self.animation_loop]

                    self.game.draw()

                    start += 4

                self.y_change = 0

        if self.facing == RIGHT:
            if self.x_change == 0:
                self.image = self.game.character_sheet.get_sprite(96, 0, self.width, self.height)
                self.animation_loop = 0
            else:
                while start != end:
                    self.rect.x += 4

                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= 4

                    if start == animation_frame:
                        self.animation_loop += 1
                        self.image = self.right_animations[self.animation_loop]

                    self.game.draw()

                    start += 4

                self.y_change = 0

    def check_ground(self):
        items = ['Ch', 'Ba', 'Me', 'Gr', 'Or', 'Ap']
        if self.game.loc.data[self.rel_y//32][self.rel_x//32] in items:
            self.game.loc.data[self.rel_y//32][self.rel_x//32] = '.'


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_sheet.get_sprite(type * TILE_SIZE, 0, self.width, self.height)
        self.image.set_colorkey(NASTY_GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y, n):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.number = n

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.door_sheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(NASTY_GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.use_door()

    def use_door(self):
        hits = pygame.sprite.collide_rect(self.game.player, self)
        if hits:
            self.game.kill_map()
            self.game.screen.fill(BLACK)
            node = self.game.loc.bridges[self.number].room

            if node.num not in self.game.visited:
                self.game.depth += 1
                node = level.generate_next_maps(node)
                self.game.visited.append(node.num)
            elif node.num in self.game.visited and self.game.loc.num < node.num:
                self.game.depth += 1
            else:
                self.game.depth -= 1

            pygame.mixer.Sound.play(DOOR)
            player = self.game.loc.bridges[self.number].spawn
            self.game.load_room(node, player)


class Item(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        self.use_item()

    def use_item(self):
        hits = pygame.sprite.collide_rect(self.game.player, self)
        if hits:
            pygame.mixer.Sound.play(EAT)
            self.kill()


class Cherry(Item):
    def __init__(self, game, x, y):
        super().__init__(game)
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.items_sheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(NASTY_GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Banana(Item):
    def __init__(self, game, x, y):
        super().__init__(game)
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.items_sheet.get_sprite(32, 0, self.width, self.height)
        self.image.set_colorkey(NASTY_GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Melon(Item):
    def __init__(self, game, x, y):
        super().__init__(game)
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.items_sheet.get_sprite(64, 0, self.width, self.height)
        self.image.set_colorkey(NASTY_GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Grape(Item):
    def __init__(self, game, x, y):
        super().__init__(game)
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.items_sheet.get_sprite(96, 0, self.width, self.height)
        self.image.set_colorkey(NASTY_GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Orange(Item):
    def __init__(self, game, x, y):
        super().__init__(game)
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.items_sheet.get_sprite(128, 0, self.width, self.height)
        self.image.set_colorkey(NASTY_GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Apple(Item):
    def __init__(self, game, x, y):
        super().__init__(game)
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.items_sheet.get_sprite(160, 0, self.width, self.height)
        self.image.set_colorkey(NASTY_GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
