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

        self.start = 0
        self.end = 0

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
        self.check_feet()
        if self.start == self.end:
            self.rel_x += self.x_change
            self.rel_y += self.y_change
            self.start, self.end = 0, 0
            self.x_change, self.y_change = 0, 0
            self.move_direction()

            if self.facing == DOWN and self.y_change == 0:
                self.image = self.game.character_sheet.get_sprite(0, 0, self.width, self.height)
                self.animation_loop = 0
            if self.facing == UP and self.y_change == 0:
                self.image = self.game.character_sheet.get_sprite(32, 0, self.width, self.height)
                self.animation_loop = 0
            if self.facing == LEFT and self.x_change == 0:
                self.image = self.game.character_sheet.get_sprite(64, 0, self.width, self.height)
                self.animation_loop = 0
            if self.facing == RIGHT and self.x_change == 0:
                self.image = self.game.character_sheet.get_sprite(96, 0, self.width, self.height)
                self.animation_loop = 0

            if self.collide_block('x') or self.collide_block('y'):
                if self.sound_delay < pygame.time.get_ticks():
                    self.sound_delay = pygame.time.get_ticks() + 320
                    pygame.mixer.Sound.play(WALL)
                self.x_change = 0
                self.y_change = 0
                self.end -= PLAYER_SPEED
                return

        elif self.start != self.end:
            self.animate_movement()

    def move_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.end += PLAYER_SPEED
            self.facing = LEFT
        elif keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.end += PLAYER_SPEED
            self.facing = RIGHT
        elif keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.end += PLAYER_SPEED
            self.facing = DOWN
        elif keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.end += PLAYER_SPEED
            self.facing = UP
        return False

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
        if self.animation_loop == 2:
            self.animation_loop = 0

        if self.facing == DOWN:
            self.rect.y += 4
            for sprite in self.game.all_sprites:
                sprite.rect.y -= 4
            self.start += 4
            if self.start == 16:
                self.animation_loop += 1
                self.image = self.down_animations[self.animation_loop]

        elif self.facing == UP:
            self.rect.y -= 4
            for sprite in self.game.all_sprites:
                sprite.rect.y += 4
            self.start += 4
            if self.start == 16:
                self.animation_loop += 1
                self.image = self.up_animations[self.animation_loop]

        elif self.facing == LEFT:
            self.rect.x -= 4
            for sprite in self.game.all_sprites:
                sprite.rect.x += 4
            self.start += 4
            if self.start == 16:
                self.animation_loop += 1
                self.image = self.left_animations[self.animation_loop]

        elif self.facing == RIGHT:
            self.rect.x += 4
            for sprite in self.game.all_sprites:
                sprite.rect.x -= 4
            self.start += 4
            if self.start == 16:
                self.animation_loop += 1
                self.image = self.right_animations[self.animation_loop]

    def check_feet(self):
        items = ['Ch', 'Ba', 'Me', 'Gr', 'Or', 'Ap']
        if self.game.loc.data[self.rel_y//32][self.rel_x//32] in items:
            self.game.loc.data[self.rel_y//32][self.rel_x//32] = '.'

    def death(self):
        self.image = self.game.character_sheet.get_sprite(128, 0, self.width, self.height)
        self.game.draw()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = self.game.all_sprites
        self.x_change = 0
        self.y_change = 0
        self.animation_loop = 0
        self.movement_delay = 0
        pygame.sprite.Sprite.__init__(self, self.groups)

    def collide_player(self):
        hits = pygame.sprite.collide_rect(self.game.player, self)
        if hits:
            pygame.mixer.Sound.play(DAMAGE)
            self.game.player.death()


class Balloon(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game)
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.enemy_sheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(NASTY_GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.start = 0
        self.end = 0
        self.speed = 1
        self.type = rd.choice(['HORIZONTAL', 'VERTICAL'])
        if self.type == 'HORIZONTAL':
            self.facing = DOWN
        elif self.type == 'VERTICAL':
            self.facing = RIGHT

        self.down_animations = [
            self.game.enemy_sheet.get_sprite(0, 0, self.width, self.height),
            self.game.enemy_sheet.get_sprite(0, 32, self.width, self.height)
        ]
        self.up_animations = [
            self.game.enemy_sheet.get_sprite(32, 0, self.width, self.height),
            self.game.enemy_sheet.get_sprite(32, 32, self.width, self.height)
        ]
        self.left_animations = [
            self.game.enemy_sheet.get_sprite(64, 0, self.width, self.height),
            self.game.enemy_sheet.get_sprite(64, 32, self.width, self.height)
        ]
        self.right_animations = [
            self.game.enemy_sheet.get_sprite(96, 0, self.width, self.height),
            self.game.enemy_sheet.get_sprite(96, 32, self.width, self.height)
        ]

    def update(self):
        self.collide_player()
        if self.start == self.end:
            self.start, self.end = 0, 0
            self.end = 32
            if self.collide_block():  # If no collision, animate movement
                self.change_direction()
        elif self.start != self.end:
            self.animate_movement()

    def change_direction(self):
        if self.facing == RIGHT:
            self.facing = LEFT
        elif self.facing == LEFT:
            self.facing = RIGHT

        if self.facing == DOWN:
            self.facing = UP
        elif self.facing == UP:
            self.facing = DOWN

    def collide_block(self):
        hits = None
        if self.facing == UP:
            self.rect.y -= self.end
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            self.rect.y += self.end
        elif self.facing == DOWN:
            self.rect.y += self.end
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            self.rect.y -= self.end
        elif self.facing == RIGHT:
            self.rect.x += self.end
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            self.rect.x -= self.end
        elif self.facing == LEFT:
            self.rect.x -= self.end
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            self.rect.x += self.end
        return True if hits else False

    def animate_movement(self):

        if self.facing == DOWN:
            self.image = self.game.enemy_sheet.get_sprite(0, 0, self.width, self.height)
            self.rect.y += self.speed

        if self.facing == UP:
            self.image = self.game.enemy_sheet.get_sprite(0, 0, self.width, self.height)
            self.rect.y -= self.speed

        if self.facing == LEFT:
            self.image = self.game.enemy_sheet.get_sprite(0, 0, self.width, self.height)
            self.rect.x -= self.speed

        if self.facing == RIGHT:
            self.image = self.game.enemy_sheet.get_sprite(0, 0, self.width, self.height)
            self.rect.x += self.speed

        self.start += self.speed


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
    def __init__(self, game, x, y, n, used):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.number = n

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        if not used:
            self.image = self.game.door_sheet.get_sprite(0, 0, self.width, self.height)
        else:
            self.image = self.game.door_sheet.get_sprite(32, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.use_door()

    def use_door(self):
        hits = pygame.sprite.collide_rect(self.game.player, self)
        if hits:
            if self.number not in self.game.used_doors:
                self.game.used_doors.append(self.number)

            self.game.kill_map()
            self.game.screen.fill(BLACK)

            node = self.game.loc.bridges[self.number].room

            if node.num not in self.game.visited:   # New depth
                self.game.depth += 1
                node = level.generate_next_maps(self.game, node)
                self.game.visited.append(node.num)
            elif node.num in self.game.visited and self.game.loc.num < node.num:    # Depth reachieved
                self.game.depth += 1
            else:   # Backtracking
                self.game.depth -= 1

            pygame.mixer.Sound.play(DOOR)
            player = self.game.loc.bridges[self.number].spawn
            self.game.player.movement_delay = pygame.time.get_ticks() + 2000
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
