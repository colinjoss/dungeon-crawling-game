import pygame
from config import *
import level_generation as level
import math
import random as rd
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
        
        # Fundamental variables
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = self.game.character_sheet.get_sprite(0, 0, self.width, self.height)
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Movement and size variables
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.rel_x = self.x
        self.rel_y = self.y
        self.x_change = 0
        self.y_change = 0
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Animation variables
        self.movement_start = 0
        self.movement_end = 0
        self.movement_delay = 0
        self.sound_delay = 0
        self.facing = DOWN
        self.animation_loop = 0

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
        """
        Updates player character.
        """
        self.check_feet()   # Player checks the ground at their current coordinate

        if self.movement_start == self.movement_end:    # No current movement

            # Reset variables from previous movement; update player relative coordinate
            self.rel_x += self.x_change
            self.rel_y += self.y_change
            self.movement_start, self.movement_end = 0, 0
            self.x_change, self.y_change = 0, 0

            # Get keyboard input from user
            self.move_direction()

            # Cancel movement if blocked
            if self.is_collision('x') or self.is_collision('y'):
                self.cancel_movement()
                return

        elif self.movement_start != self.movement_end:      # Movement currently in motion
            self.animate_movement()

    def cancel_movement(self):
        """
        Cancel attempted player move.
        """
        if self.sound_delay < pygame.time.get_ticks():
            self.sound_delay = pygame.time.get_ticks() + 320
            pygame.mixer.Sound.play(WALL)
        self.x_change, self.y_change = 0, 0
        self.movement_end -= PLAYER_SPEED

    def stationary(self):
        """
        If no movement, resets player image to stationary.
        """
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

    def move_direction(self):
        """
        Detects arrow input and adjusts x/y change variables.
        If no input, resets player animation to stationary.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.movement_end += PLAYER_SPEED
            self.facing = LEFT
        elif keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.movement_end += PLAYER_SPEED
            self.facing = RIGHT
        elif keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.movement_end += PLAYER_SPEED
            self.facing = DOWN
        elif keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.movement_end += PLAYER_SPEED
            self.facing = UP
        else:
            self.stationary()

    def is_collision(self, direction):
        """
        Returns true if collision detected, false otherwise.
        """
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
        """
        Animates player movement.
        """
        if self.animation_loop == 2:
            self.animation_loop = 0

        self.movement_start += 4
        if self.facing == DOWN:
            self.move_down()
        elif self.facing == UP:
            self.move_up()
        elif self.facing == LEFT:
            self.move_left()
        elif self.facing == RIGHT:
            self.move_right()

    def center_camera(self, dir, amount):
        """
        Adjusts camera to stay centered on player.
        """
        if dir == 'x':
            for sprite in self.game.all_sprites:
                sprite.rect.x += amount
        elif dir == 'y':
            for sprite in self.game.all_sprites:
                sprite.rect.y += amount

    def move_down(self):
        """
        Animates player down movement.
        """
        self.rect.y += 4
        self.center_camera('y', -4)
        if self.movement_start == 16:
            self.animation_loop += 1
            self.image = self.down_animations[self.animation_loop]

    def move_up(self):
        """
        Animates player up movement.
        """
        self.rect.y -= 4
        self.center_camera('y', 4)
        if self.movement_start == 16:
            self.animation_loop += 1
            self.image = self.up_animations[self.animation_loop]

    def move_left(self):
        """
        Animates player left movement.
        """
        self.rect.x -= 4
        self.center_camera('x', 4)
        if self.movement_start == 16:
            self.animation_loop += 1
            self.image = self.left_animations[self.animation_loop]

    def move_right(self):
        """
        Animates player right movement.
        """
        self.rect.x += 4
        self.center_camera('x', -4)
        if self.movement_start == 16:
            self.animation_loop += 1
            self.image = self.right_animations[self.animation_loop]

    def check_feet(self):
        """
        Looks for items at player coordinate.
        """
        items = ['Ch', 'Ba', 'Me', 'Gr', 'Or', 'Ap']

        if self.game.loc.data[self.rel_y//32][self.rel_x//32] in items:
            self.game.loc.data[self.rel_y//32][self.rel_x//32] = '.'
            self.game.loc.fruit -= 1

    def kill_player(self):
        """
        Animate player death.
        """
        self.image = self.game.character_sheet.get_sprite(128, 0, self.width, self.height)
        self.game.draw()
        pygame.time.delay(2000)
        self.game.player_death()

    def use_door(self, door):
        if door in self.game.locked_doors:  # Locked door; cannot use
            return
        elif door in self.game.unopened_doors:  # Unopened door; remove from unopened_doors
            self.game.unopened_doors.remove(door)
        self.game.traverse(door)


class NPC(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = self.game.all_sprites, self.game.blocks
        self.animation_loop = 0
        pygame.sprite.Sprite.__init__(self, self.groups)


class ShopKeep(NPC):
    def __init__(self, game, x, y):
        super().__init__(game)
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.npc_sheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(NASTY_GREEN)
        self.animation_loop = 0

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        """
        Update shopkeeper sprite.
        """
        self.animate()

    def animate(self):
        """
        Stationary animation for shopkeeper.
        """
        self.animation_loop += 1
        if self.animation_loop < 40:
            self.image = self.game.npc_sheet.get_sprite(0, 32, self.width, self.height)
        elif self.animation_loop < 80:
            self.image = self.game.npc_sheet.get_sprite(0, 0, self.width, self.height)
        else:
            self.animation_loop = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = self.game.all_sprites, self.game.all_enemies
        self.x_change = 0
        self.y_change = 0
        self.animation_loop = 0
        self.movement_delay = 0
        pygame.sprite.Sprite.__init__(self, self.groups)

    def collide_player(self):
        """
        If enemy hits player, kill player.
        """
        if self.is_hitting_player():
            self.game.play_sound(DAMAGE)
            self.game.player.kill_player()

    def is_hitting_player(self):
        """
        Returns true if hit player, false otherwise.
        """
        return pygame.sprite.collide_rect(self.game.player, self)

    def defeat(self):
        """
        Remove enemy from screen.
        """
        self.kill()


class WaddleBug(Enemy):
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

        self.movement_start = 0
        self.movement_end = 0
        self.speed = 1
        self.type = rd.choice(['HORIZONTAL', 'VERTICAL'])
        if self.type == 'HORIZONTAL':
            self.facing = DOWN
        elif self.type == 'VERTICAL':
            self.facing = RIGHT

        self.down_animations = [
            self.game.enemy_sheet.get_sprite(0, 0, self.width, self.height),
            self.game.enemy_sheet.get_sprite(0, 32, self.width, self.height),
            self.game.enemy_sheet.get_sprite(0, 64, self.width, self.height),
            self.game.enemy_sheet.get_sprite(0, 96, self.width, self.height)
        ]
        self.up_animations = [
            self.game.enemy_sheet.get_sprite(32, 0, self.width, self.height),
            self.game.enemy_sheet.get_sprite(32, 32, self.width, self.height),
            self.game.enemy_sheet.get_sprite(32, 64, self.width, self.height),
            self.game.enemy_sheet.get_sprite(32, 96, self.width, self.height)
        ]
        self.left_animations = [
            self.game.enemy_sheet.get_sprite(64, 0, self.width, self.height),
            self.game.enemy_sheet.get_sprite(64, 32, self.width, self.height),
            self.game.enemy_sheet.get_sprite(64, 64, self.width, self.height),
            self.game.enemy_sheet.get_sprite(64, 96, self.width, self.height)
        ]
        self.right_animations = [
            self.game.enemy_sheet.get_sprite(96, 0, self.width, self.height),
            self.game.enemy_sheet.get_sprite(96, 32, self.width, self.height),
            self.game.enemy_sheet.get_sprite(96, 64, self.width, self.height),
            self.game.enemy_sheet.get_sprite(96, 96, self.width, self.height)
        ]

        self.animation_frame_1 = 8
        self.animation_frame_2 = 16
        self.animation_frame_3 = 24

    def update(self):
        """
        Update WaddleBug.
        """
        self.collide_player()
        if self.movement_start == self.movement_end:
            self.movement_start, self.movement_end = 0, 0
            self.movement_end = TILE_SIZE
            if self.collide_block():  # If no collision, animate movement
                self.change_direction()
        elif self.movement_start != self.movement_end:
            self.animate_movement()

    def change_direction(self):
        """
        Change WaddleBug walking direction.
        """
        if self.facing == RIGHT:
            self.facing = LEFT
        elif self.facing == LEFT:
            self.facing = RIGHT

        if self.facing == DOWN:
            self.facing = UP
        elif self.facing == UP:
            self.facing = DOWN

    def collide_block(self):
        """
        Detects if WaddleBug has collided with block.
        """
        hits = None
        if self.facing == UP:
            self.rect.y -= self.movement_end
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            self.rect.y += self.movement_end
        elif self.facing == DOWN:
            self.rect.y += self.movement_end
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            self.rect.y -= self.movement_end
        elif self.facing == RIGHT:
            self.rect.x += self.movement_end
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            self.rect.x -= self.movement_end
        elif self.facing == LEFT:
            self.rect.x -= self.movement_end
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            self.rect.x += self.movement_end
        return True if hits else False

    def animate_movement(self):
        """
        Animate WaddleBug movement.
        """
        if self.facing == DOWN:
            self.move_down()
        if self.facing == UP:
            self.move_up()
        if self.facing == LEFT:
            self.move_left()
        if self.facing == RIGHT:
            self.move_right()
        self.movement_start += self.speed

    def move_down(self):
        """
        Move WaddleBug down
        """
        if self.movement_start < self.animation_frame_1:
            self.image = self.game.enemy_sheet.get_sprite(0, 0, self.width, self.height)
        elif self.movement_start < self.animation_frame_2:
            self.image = self.game.enemy_sheet.get_sprite(0, 32, self.width, self.height)
        elif self.movement_start < self.animation_frame_3:
            self.image = self.game.enemy_sheet.get_sprite(0, 0, self.width, self.height)
        else:
            self.image = self.game.enemy_sheet.get_sprite(0, 64, self.width, self.height)
        self.rect.y += self.speed

    def move_up(self):
        """
        Move WaddleBug up
        """
        if self.movement_start < self.animation_frame_1:
            self.image = self.game.enemy_sheet.get_sprite(32, 0, self.width, self.height)
        elif self.movement_start < self.animation_frame_2:
            self.image = self.game.enemy_sheet.get_sprite(32, 32, self.width, self.height)
        elif self.movement_start < self.animation_frame_3:
            self.image = self.game.enemy_sheet.get_sprite(32, 0, self.width, self.height)
        else:
            self.image = self.game.enemy_sheet.get_sprite(32, 64, self.width, self.height)
        self.rect.y -= self.speed

    def move_left(self):
        """
        Move WaddleBug left
        """
        if self.movement_start < self.animation_frame_1:
            self.image = self.game.enemy_sheet.get_sprite(64, 0, self.width, self.height)
        elif self.movement_start < self.animation_frame_2:
            self.image = self.game.enemy_sheet.get_sprite(64, 32, self.width, self.height)
        elif self.movement_start < self.animation_frame_3:
            self.image = self.game.enemy_sheet.get_sprite(64, 0, self.width, self.height)
        else:
            self.image = self.game.enemy_sheet.get_sprite(64, 64, self.width, self.height)
        self.rect.x -= self.speed

    def move_right(self):
        """
        Move WaddleBug right
        """
        if self.movement_start < self.animation_frame_1:
            self.image = self.game.enemy_sheet.get_sprite(96, 0, self.width, self.height)
        elif self.movement_start < self.animation_frame_2:
            self.image = self.game.enemy_sheet.get_sprite(96, 32, self.width, self.height)
        elif self.movement_start < self.animation_frame_3:
            self.image = self.game.enemy_sheet.get_sprite(96, 0, self.width, self.height)
        else:
            self.image = self.game.enemy_sheet.get_sprite(96, 64, self.width, self.height)
        self.rect.x += self.speed


class GrimLeaper(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game)
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.enemy_sheet.get_sprite(0, 96, self.width, self.height)
        self.image.set_colorkey(NASTY_GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.movement_start = 0
        self.movement_end = 0
        self.speed = 2
        self.facing = DOWN
        self.jump_cycle = 32

        self.down_animations = [
            self.game.enemy_sheet.get_sprite(0, 96, self.width, self.height),
            self.game.enemy_sheet.get_sprite(0, 128, self.width, self.height),
        ]
        self.up_animations = [
            self.game.enemy_sheet.get_sprite(32, 96, self.width, self.height),
            self.game.enemy_sheet.get_sprite(32, 128, self.width, self.height),
        ]
        self.left_animations = [
            self.game.enemy_sheet.get_sprite(64, 96, self.width, self.height),
            self.game.enemy_sheet.get_sprite(64, 128, self.width, self.height),
        ]
        self.right_animations = [
            self.game.enemy_sheet.get_sprite(96, 96, self.width, self.height),
            self.game.enemy_sheet.get_sprite(96, 128, self.width, self.height),
        ]

        self.directions = [DOWN, UP, LEFT, RIGHT]

    def update(self):
        """
        Update GrimLeaper.
        """
        self.collide_player()
        if int(self.movement_start) == self.movement_end and self.movement_delay < pygame.time.get_ticks():
            self.movement_start, self.movement_end, self.movement_delay = 0, 64, 0
            self.change_direction()
            if self.collide_block():  # If no collision, animate movement
                self.movement_start, self.movement_end, self.movement_delay = 0, 0, 0
        elif self.movement_start != self.movement_end:
            self.animate_movement()
            if self.movement_start == self.movement_end:
                self.movement_delay = pygame.time.get_ticks() + 1000
                self.stationary()

    def change_direction(self):
        """
        Randomly select a new direction for GrimLeaper
        """
        i = int(rd.random() * len(self.directions))
        self.facing = self.directions[i]

    def stationary(self):
        """
        Resets GrimLeaper's sprite to stationary
        """
        if self.facing == DOWN:
            self.image = self.game.enemy_sheet.get_sprite(0, 96, self.width, self.height)
        elif self.facing == UP:
            self.image = self.game.enemy_sheet.get_sprite(32, 96, self.width, self.height)
        elif self.facing == LEFT:
            self.image = self.game.enemy_sheet.get_sprite(64, 96, self.width, self.height)
        elif self.facing == RIGHT:
            self.image = self.game.enemy_sheet.get_sprite(96, 96, self.width, self.height)

    def collide_block(self):
        """
        Detects if GrimLeaper has collided with block.
        """
        hits = None
        if self.facing == UP:
            self.rect.y -= self.movement_end
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            self.rect.y += self.movement_end
        elif self.facing == DOWN:
            self.rect.y += self.movement_end
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            self.rect.y -= self.movement_end
        elif self.facing == RIGHT:
            self.rect.x += self.movement_end
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            self.rect.x -= self.movement_end
        elif self.facing == LEFT:
            self.rect.x -= self.movement_end
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            self.rect.x += self.movement_end
        return True if hits else False

    def animate_movement(self):
        """
        Animate GrimLeaper movement.
        """
        if self.facing == DOWN:
            self.move_down()
        if self.facing == UP:
            self.move_up()
        if self.facing == LEFT:
            self.move_left()
        if self.facing == RIGHT:
            self.move_right()
        self.movement_start += self.speed

    def move_down(self):
        """
        Move GrimLeaper down
        """
        if self.movement_start == 0:
            self.image = self.game.enemy_sheet.get_sprite(0, 128, self.width, self.height)

        self.rect.y += self.speed

    def move_up(self):
        """
        Move GrimLeaper up
        """
        if self.movement_start == 0:
            self.image = self.game.enemy_sheet.get_sprite(32, 128, self.width, self.height)
        self.rect.y -= self.speed

    def move_left(self):
        """
        Move GrimLeaper left
        """
        if self.movement_start == 0:
            self.image = self.game.enemy_sheet.get_sprite(64, 128, self.width, self.height)

        if self.movement_start < self.jump_cycle:  # 32
            self.rect.y -= 1
        else:  # 64
            self.rect.y += 1
        self.rect.x -= self.speed

    def move_right(self):
        """
        Move GrimLeaper right
        """
        if self.movement_start == 0:
            self.image = self.game.enemy_sheet.get_sprite(96, 128, self.width, self.height)

        if self.movement_start < self.jump_cycle:  # 32
            self.rect.y -= 1
        else:  # 64
            self.rect.y += 1
        self.rect.x += self.speed


class WaitWatch(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game)
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.enemy_sheet.get_sprite(0, 160, self.width, self.height)
        self.image.set_colorkey(NASTY_GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.movement_start = 0
        self.movement_end = 0
        self.speed = 1
        self.facing = DOWN
        self.watching = False

        self.down_animations = [
            self.game.enemy_sheet.get_sprite(0, 160, self.width, self.height),
            self.game.enemy_sheet.get_sprite(0, 192, self.width, self.height),
            self.game.enemy_sheet.get_sprite(0, 224, self.width, self.height),
        ]
        self.up_animations = [
            self.game.enemy_sheet.get_sprite(32, 160, self.width, self.height),
            self.game.enemy_sheet.get_sprite(32, 192, self.width, self.height),
            self.game.enemy_sheet.get_sprite(32, 224, self.width, self.height),
        ]
        self.left_animations = [
            self.game.enemy_sheet.get_sprite(64, 160, self.width, self.height),
            self.game.enemy_sheet.get_sprite(64, 192, self.width, self.height),
            self.game.enemy_sheet.get_sprite(64, 224, self.width, self.height),
        ]
        self.right_animations = [
            self.game.enemy_sheet.get_sprite(96, 160, self.width, self.height),
            self.game.enemy_sheet.get_sprite(96, 192, self.width, self.height),
            self.game.enemy_sheet.get_sprite(96, 224, self.width, self.height),
        ]
        self.evil_face = self.game.enemy_sheet.get_sprite(32, 256, self.width, self.height)

        self.animation_frame = 16
        self.directions = [DOWN, UP, LEFT, RIGHT]

    def update(self):
        """
        Update WaitWatch
        """
        self.collide_player()
        if self.in_eyeshot():
            self.image = self.evil_face
            return

        if int(self.movement_start) == self.movement_end and self.movement_delay < pygame.time.get_ticks():
            self.movement_start, self.movement_end, self.movement_delay = 0, 32, 0
            self.change_direction()

            if self.collide_block():  # If no collision, animate movement
                self.movement_start, self.movement_end, self.movement_delay = 0, 0, 0

            seed = int(rd.random() * 100)
            if seed > 50:
                self.movement_start, self.movement_end = 0, 0
                self.movement_delay = pygame.time.get_ticks() + 3000
                self.stationary()

        elif self.movement_start != self.movement_end:
            self.watching = False
            self.animate_movement()
            if self.movement_start == self.movement_end:
                self.movement_delay = pygame.time.get_ticks() + 3000
                self.stationary()

    def change_direction(self):
        """
        Randomly select a new direction for GrimLeaper
        """
        i = int(rd.random() * len(self.directions))
        self.facing = self.directions[i]

    def stationary(self):
        """
        Resets GrimLeaper's sprite to stationary
        """
        if self.facing == DOWN:
            self.image = self.game.enemy_sheet.get_sprite(0, 160, self.width, self.height)
        elif self.facing == UP:
            self.image = self.game.enemy_sheet.get_sprite(32, 160, self.width, self.height)
        elif self.facing == LEFT:
            self.image = self.game.enemy_sheet.get_sprite(64, 160, self.width, self.height)
        elif self.facing == RIGHT:
            self.image = self.game.enemy_sheet.get_sprite(96, 160, self.width, self.height)
        self.watching = True

    def is_watching(self):
        return self.watching

    def collide_block(self):
        """
        Detects if GrimLeaper has collided with block.
        """
        hits = None
        if self.facing == UP:
            self.rect.y -= self.movement_end
            hits = self.collision(self.game.blocks)
            self.rect.y += self.movement_end
        elif self.facing == DOWN:
            self.rect.y += self.movement_end
            hits = self.collision(self.game.blocks)
            self.rect.y -= self.movement_end
        elif self.facing == RIGHT:
            self.rect.x += self.movement_end
            hits = self.collision(self.game.blocks)
            self.rect.x -= self.movement_end
        elif self.facing == LEFT:
            self.rect.x -= self.movement_end
            hits = self.collision(self.game.blocks)
            self.rect.x += self.movement_end
        return True if hits else False

    def collision(self, object):
        return pygame.sprite.spritecollide(self, object, False)

    def animate_movement(self):
        """
        Animate GrimLeaper movement.
        """
        if self.facing == DOWN:
            self.move_down()
        if self.facing == UP:
            self.move_up()
        if self.facing == LEFT:
            self.move_left()
        if self.facing == RIGHT:
            self.move_right()
        self.movement_start += self.speed

    def move_down(self):
        """
        Move WaddleBug down
        """
        if self.movement_start < self.animation_frame:
            self.image = self.game.enemy_sheet.get_sprite(0, 192, self.width, self.height)
        else:
            self.image = self.game.enemy_sheet.get_sprite(0, 224, self.width, self.height)
        self.rect.y += self.speed

    def move_up(self):
        """
        Move WaddleBug up
        """
        if self.movement_start < self.animation_frame:
            self.image = self.game.enemy_sheet.get_sprite(32, 192, self.width, self.height)
        else:
            self.image = self.game.enemy_sheet.get_sprite(32, 224, self.width, self.height)
        self.rect.y -= self.speed

    def move_left(self):
        """
        Move WaddleBug left
        """
        if self.movement_start < self.animation_frame:
            self.image = self.game.enemy_sheet.get_sprite(64, 192, self.width, self.height)
        else:
            self.image = self.game.enemy_sheet.get_sprite(64, 224, self.width, self.height)
        self.rect.x -= self.speed

    def move_right(self):
        """
        Move WaddleBug right
        """
        if self.movement_start < self.animation_frame:
            self.image = self.game.enemy_sheet.get_sprite(96, 192, self.width, self.height)
        else:
            self.image = self.game.enemy_sheet.get_sprite(96, 224, self.width, self.height)
        self.rect.x += self.speed

    def in_eyeshot(self):
        if self.watching:
            if self.facing == DOWN:
                return self.look_for_player('y', 32)
            elif self.facing == UP:
                return self.look_for_player('y', -32)
            elif self.facing == LEFT:
                return self.look_for_player('x', -32)
            elif self.facing == RIGHT:
                return self.look_for_player('x', 32)
        return False

    def look_for_player(self, direction, amount):
        if direction == 'x':
            for tile in range(1, 6):
                self.rect.x += tile * amount
                if self.is_hitting_player():
                    return True
                self.rect.x -= tile * amount
        if direction == 'y':
            for tile in range(1, 6):
                self.rect.y += tile * amount
                if self.is_hitting_player():
                    return True
                self.rect.y -= tile * amount
        return False


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
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_sheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(NASTY_GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y, n, locked, unopened):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.all_doors
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.number = n

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        if locked:
            self.image = self.game.door_sheet.get_sprite(64, 0, self.width, self.height)
        elif unopened:
            self.image = self.game.door_sheet.get_sprite(0, 0, self.width, self.height)
        else:   # used doors
            self.image = self.game.door_sheet.get_sprite(32, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        """
        Update door
        """
        if self.is_hitting_player():
            self.game.player.use_door(self.number)

    def is_hitting_player(self):
        """
        Returns true if hitting player, else false.
        """
        return pygame.sprite.collide_rect(self.game.player, self)

    def unlock(self):
        """
        Unlock door
        """
        self.game.loc.cleared = True
        if self.game.loc.num != 0:
            self.game.locked_doors.remove(self.number)

        if self.number in self.game.unopened_doors:
            self.image = self.game.door_sheet.get_sprite(0, 0, self.width, self.height)
        else:
            self.image = self.game.door_sheet.get_sprite(32, 0, self.width, self.height)

        self.game.play_sound(CLEAR)


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
            self.game.fruit_count[self.code] += 1


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

        self.code = 0


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

        self.code = 1


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

        self.code = 2


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

        self.code = 3


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

        self.code = 4


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

        self.code = 5
