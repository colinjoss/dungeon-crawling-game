from config import *
import random as rd


class SpriteSheet:
    def __init__(self, sheet):
        self.sheet = pygame.image.load(sheet).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(NASTY_GREEN)
        return sprite


class Player(pygame.sprite.Sprite):
    """
    Class representing the player character.
    """
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
        self.speed = 4
        self.invulnerable = False
        self.invulnerability_timer = 0

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
        self.check_invulnerability()
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

    def check_invulnerability(self):
        """
        Monitors the players invulnerability status.
        """
        if self.invulnerability_timer < pygame.time.get_ticks():
            self.invulnerable = False

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
        self.movement_end += PLAYER_SPEED
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = LEFT
        elif keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = RIGHT
        elif keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = DOWN
        elif keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = UP
        else:
            self.movement_end -= PLAYER_SPEED
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
        self.rect.y += self.speed
        self.center_camera('y', -1 * self.speed)
        if self.movement_start == 16:
            self.animation_loop += 1
            self.image = self.down_animations[self.animation_loop]

    def move_up(self):
        """
        Animates player up movement.
        """
        self.rect.y -= self.speed
        self.center_camera('y', self.speed)
        if self.movement_start == 16:
            self.animation_loop += 1
            self.image = self.up_animations[self.animation_loop]

    def move_left(self):
        """
        Animates player left movement.
        """
        self.rect.x -= self.speed
        self.center_camera('x', self.speed)
        if self.movement_start == 16:
            self.animation_loop += 1
            self.image = self.left_animations[self.animation_loop]

    def move_right(self):
        """
        Animates player right movement.
        """
        self.rect.x += self.speed
        self.center_camera('x', -1 * self.speed)
        if self.movement_start == 16:
            self.animation_loop += 1
            self.image = self.right_animations[self.animation_loop]

    def check_feet(self):
        """
        Looks for items at player coordinate.
        """
        if self.game.loc.data[self.rel_y//32][self.rel_x//32] in ITEM_CODES:
            self.game.loc.data[self.rel_y//32][self.rel_x//32] = '.'
            self.game.loc.fruit -= 1

    def check_facing_tile(self):
        """
        Attempts to interact with the tile the player is facing.
        """
        tile = self.get_facing_tile()
        if self.game.loc.data[tile[0]//32][tile[1]//32] == 'S':
            if self.game.shop is None:
                self.game.shop = self.game.open_shop()
            self.game.trade()

    def get_facing_tile(self):
        """
        Returns the coordinates of the tile the player is facing.
        """
        if self.facing == UP:
            return self.rel_y - 32, self.rel_x
        elif self.facing == DOWN:
            return self.rel_y + 32, self.rel_x
        elif self.facing == RIGHT:
            return self.rel_y, self.rel_x + 32
        elif self.facing == LEFT:
            return self.rel_y, self.rel_x - 32

    def use_power(self):
        """
        The player uses their current power up.
        """
        if self.game.power_up == 7:     # Ice cream - fruit multiplier
            for key in self.game.fruit_count:
                self.game.fruit_count[key] = self.game.fruit_count[key] * 2
        elif self.game.power_up == 8:   # Drink - eats all the fruit
            for fruit in self.game.all_items:
                fruit.eat_without_touch()
        elif self.game.power_up == 9 and self.game.lives != 5:   # Candy - add a life
            self.game.lives += 1
        else:
            self.game.play_sound(ERROR)
        self.game.power_up = 0

    def kill_player(self):
        """
        Animate player death.
        """
        self.image = self.game.character_sheet.get_sprite(128, 0, self.width, self.height)
        self.game.draw()
        pygame.time.delay(2000)
        self.game.player_death()

    def use_door(self, door):
        """
        The player uses a door to enter a new dungeon room.
        """
        if door in self.game.locked_doors:  # Locked door; cannot use
            return
        elif door in self.game.unopened_doors:  # Unopened door; remove from unopened_doors
            self.game.unopened_doors.remove(door)
        self.game.traverse(door)


class NPC(pygame.sprite.Sprite):
    """
    Represents a non-player character.
    """
    def __init__(self, game):
        self.game = game
        self.groups = self.game.all_sprites, self.game.blocks
        self.animation_loop = 0
        pygame.sprite.Sprite.__init__(self, self.groups)


class ShopKeep(NPC):
    """
    Represents NPC who sells the player upgrades and powers.
    """
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
    """
    Represents an enemy.
    """
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
        if self.is_hitting_player() and self.game.player.invulnerable:
            self.game.play_sound(SAFE)

        if self.is_hitting_player() and not self.game.player.invulnerable:
            self.game.play_sound(DAMAGE)
            self.game.player.kill_player()

    def is_hitting_player(self):
        """
        Returns true if hit player, false otherwise.
        """
        return pygame.sprite.collide_rect(self.game.player, self)


class WaddleBug(Enemy):
    """
    Represents WaddleBug, a simple enemy who marches back and forth.
    """
    def __init__(self, game, x, y):
        super().__init__(game)
        self._layer = PLAYER_LAYER

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

    def defeat(self):
        """
        Remove WaddleBug from screen.
        """
        self.image = self.game.enemy_sheet.get_sprite(128, 0, 32, 32)
        self.game.draw()
        self.kill()
        self.game.friend_eater = None


class GrimLeaper(Enemy):
    """
    Represents GrimLeaper, an enemy that jumps around in random directions.
    """
    def __init__(self, game, x, y):
        super().__init__(game)
        self._layer = PLAYER_LAYER

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

    def defeat(self):
        """
        Remove GrimLeaper from screen.
        """
        self.image = self.game.enemy_sheet.get_sprite(128, 96, 32, 32)
        self.game.draw()
        self.kill()
        self.game.friend_eater = None


class WaitWatch(Enemy):
    """
    Represents WaitWatch, an enemy who will kill the player if the player enters
    its line of sight.
    """
    def __init__(self, game, x, y):
        super().__init__(game)
        self._layer = PLAYER_LAYER

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
        Randomly select a new direction for WaitWatch
        """
        i = int(rd.random() * len(self.directions))
        self.facing = self.directions[i]

    def stationary(self):
        """
        Resets WaitWatch's sprite to stationary
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
        """
        Returns true if WaitWatch's eyes is open, false otherwise.
        """
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
        """
        Returns true if collision, false otherwise.
        """
        return pygame.sprite.spritecollide(self, object, False)

    def animate_movement(self):
        """
        Animate WaitWatch's movement.
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
        Move WaitWatch down
        """
        if self.movement_start < self.animation_frame:
            self.image = self.game.enemy_sheet.get_sprite(0, 192, self.width, self.height)
        else:
            self.image = self.game.enemy_sheet.get_sprite(0, 224, self.width, self.height)
        self.rect.y += self.speed

    def move_up(self):
        """
        Move WaitWatch up
        """
        if self.movement_start < self.animation_frame:
            self.image = self.game.enemy_sheet.get_sprite(32, 192, self.width, self.height)
        else:
            self.image = self.game.enemy_sheet.get_sprite(32, 224, self.width, self.height)
        self.rect.y -= self.speed

    def move_left(self):
        """
        Move WaitWatch left
        """
        if self.movement_start < self.animation_frame:
            self.image = self.game.enemy_sheet.get_sprite(64, 192, self.width, self.height)
        else:
            self.image = self.game.enemy_sheet.get_sprite(64, 224, self.width, self.height)
        self.rect.x -= self.speed

    def move_right(self):
        """
        Move WaitWatch right
        """
        if self.movement_start < self.animation_frame:
            self.image = self.game.enemy_sheet.get_sprite(96, 192, self.width, self.height)
        else:
            self.image = self.game.enemy_sheet.get_sprite(96, 224, self.width, self.height)
        self.rect.x += self.speed

    def in_eyeshot(self):
        """
        Returns true if the player is in WaitWatch's eyeshot, false otherwise.
        """
        if self.watching:
            if self.facing == DOWN:
                return self.see_player('y', 32)
            elif self.facing == UP:
                return self.see_player('y', -32)
            elif self.facing == LEFT:
                return self.see_player('x', -32)
            elif self.facing == RIGHT:
                return self.see_player('x', 32)
        return False

    def see_player(self, direction, amount):
        """
        Returns true if WaitWatch can see the player, false otherwise.
        """
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

    def defeat(self):
        """
        Remove WaitWatch from screen.
        """
        self.image = self.game.enemy_sheet.get_sprite(128, 160, 32, 32)
        self.game.draw()
        self.kill()
        self.game.friend_eater = None


class FriendEater(Enemy):
    """
    Represents FriendEater, an enemy that spreads poison as it wanders the dungeon.
    """
    def __init__(self, game, x, y):
        super().__init__(game)
        self._layer = PLAYER_LAYER

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.rel_x = self.x
        self.rel_y = self.y

        self.image = self.game.enemy_sheet.get_sprite(0, 288, self.width, self.height)
        self.image.set_colorkey(NASTY_GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.movement_start = 0
        self.movement_end = 0
        self.speed = 2
        self.facing = DOWN

        self.down_animations = [
            self.game.enemy_sheet.get_sprite(0, 288, self.width, self.height),
            self.game.enemy_sheet.get_sprite(0, 320, self.width, self.height),
            self.game.enemy_sheet.get_sprite(0, 352, self.width, self.height),
        ]
        self.up_animations = [
            self.game.enemy_sheet.get_sprite(32, 288, self.width, self.height),
            self.game.enemy_sheet.get_sprite(32, 320, self.width, self.height),
            self.game.enemy_sheet.get_sprite(32, 352, self.width, self.height),
        ]
        self.left_animations = [
            self.game.enemy_sheet.get_sprite(64, 288, self.width, self.height),
            self.game.enemy_sheet.get_sprite(64, 320, self.width, self.height),
            self.game.enemy_sheet.get_sprite(64, 352, self.width, self.height),
        ]
        self.right_animations = [
            self.game.enemy_sheet.get_sprite(96, 288, self.width, self.height),
            self.game.enemy_sheet.get_sprite(96, 320, self.width, self.height),
            self.game.enemy_sheet.get_sprite(96, 352, self.width, self.height),
        ]

        self.animation_frame_1 = 8
        self.animation_frame_2 = 16
        self.animation_frame_3 = 24
        self.directions = [DOWN, UP, LEFT, RIGHT]

    def update(self):
        """
        Update FriendEater
        """
        self.collide_player()
        if self.movement_start == self.movement_end and self.movement_delay < pygame.time.get_ticks():
            self.movement_start, self.movement_end, self.movement_delay = 0, 32 * int(rd.random() * 5), 0
            if self.collide_block():  # If no collision, animate movement
                self.movement_start, self.movement_end, self.movement_delay = 0, 0, 0
                self.change_direction()
        elif self.movement_start != self.movement_end:
            self.animate_movement()
            if self.movement_start == self.movement_end:
                self.update_relative_pos()
                self.movement_delay = pygame.time.get_ticks() + 1000
                self.stationary()
                self.change_direction()

    def change_direction(self):
        """
        Randomly select a new direction for FriendEater
        """
        i = int(rd.random() * len(self.directions))
        self.facing = self.directions[i]

    def collide_block(self):
        """
        Detects if FriendEater has collided with block.
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
        """
        Return true if collsion, false otherwise.
        """
        return pygame.sprite.spritecollide(self, object, False)

    def animate_movement(self):
        """
        Animate FriendEater movement.
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

    def stationary(self):
        """
        Resets FriendEater's sprite to stationary
        """
        if self.facing == DOWN:
            self.image = self.down_animations[0]
        elif self.facing == UP:
            self.image = self.up_animations[0]
        elif self.facing == LEFT:
            self.image = self.left_animations[0]
        elif self.facing == RIGHT:
            self.image = self.right_animations[0]

    def move_down(self):
        """
        Move FriendEater down
        """
        if self.movement_start < self.animation_frame_1:
            self.image = self.down_animations[1]
        elif self.movement_start < self.animation_frame_2:
            self.image = self.down_animations[0]
        elif self.movement_start < self.animation_frame_3:
            self.image = self.down_animations[2]
        else:
            self.image = self.down_animations[0]
        self.rect.y += self.speed

    def move_up(self):
        """
        Move FriendEater up
        """
        if self.movement_start < self.animation_frame_1:
            self.image = self.up_animations[1]
        elif self.movement_start < self.animation_frame_2:
            self.image = self.up_animations[0]
        elif self.movement_start < self.animation_frame_3:
            self.image = self.up_animations[2]
        else:
            self.image = self.up_animations[0]
        self.rect.y -= self.speed

    def move_left(self):
        """
        Move FriendEater left
        """
        if self.movement_start < self.animation_frame_1:
            self.image = self.left_animations[1]
        elif self.movement_start < self.animation_frame_2:
            self.image = self.left_animations[0]
        elif self.movement_start < self.animation_frame_3:
            self.image = self.left_animations[2]
        else:
            self.image = self.left_animations[0]
        self.rect.x -= self.speed

    def move_right(self):
        """
        Move FriendEater right
        """
        if self.movement_start < self.animation_frame_1:
            self.image = self.right_animations[1]
        elif self.movement_start < self.animation_frame_2:
            self.image = self.right_animations[0]
        elif self.movement_start < self.animation_frame_3:
            self.image = self.right_animations[2]
        else:
            self.image = self.right_animations[0]
        self.rect.x += self.speed

    def update_relative_pos(self):
        """
        Updates FriendEater's relative position.
        """
        if self.facing == UP:
            self.rel_y -= 32
        elif self.facing == DOWN:
            self.rel_y += 32
        elif self.facing == RIGHT:
            self.rel_x += 32
        elif self.facing == LEFT:
            self.rel_x -= 32

    def defeat(self):
        """
        Remove FriendEater from screen.
        """
        self.image = self.game.enemy_sheet.get_sprite(128, 288, 32, 32)
        self.game.draw()
        self.kill()
        self.game.friend_eater = None


class ZipperMouth(Enemy):
    """
    Represents ZipperMouth, an enemy who relentlessly pursues the player.
    """
    def __init__(self, game, x, y):
        super().__init__(game)
        self._layer = PLAYER_LAYER

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.rel_x = self.x
        self.rel_y = self.y

        self.image = self.game.enemy_sheet.get_sprite(0, 384, self.width, self.height)
        self.image.set_colorkey(NASTY_GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.movement_start = 0
        self.movement_end = 0
        self.speed = 2
        self.facing = DOWN

        self.down_animations = [
            self.game.enemy_sheet.get_sprite(0, 384, self.width, self.height),
            self.game.enemy_sheet.get_sprite(0, 416, self.width, self.height),
            self.game.enemy_sheet.get_sprite(0, 448, self.width, self.height),
        ]
        self.up_animations = [
            self.game.enemy_sheet.get_sprite(32, 384, self.width, self.height),
            self.game.enemy_sheet.get_sprite(32, 416, self.width, self.height),
            self.game.enemy_sheet.get_sprite(32, 448, self.width, self.height),
        ]
        self.left_animations = [
            self.game.enemy_sheet.get_sprite(64, 384, self.width, self.height),
            self.game.enemy_sheet.get_sprite(64, 416, self.width, self.height),
            self.game.enemy_sheet.get_sprite(64, 448, self.width, self.height),
        ]
        self.right_animations = [
            self.game.enemy_sheet.get_sprite(96, 384, self.width, self.height),
            self.game.enemy_sheet.get_sprite(96, 416, self.width, self.height),
            self.game.enemy_sheet.get_sprite(96, 448, self.width, self.height),
        ]

        self.animation_frame_1 = 8
        self.animation_frame_2 = 16
        self.animation_frame_3 = 24
        self.directions = [DOWN, UP, LEFT, RIGHT]

        self.target = self.get_player_location()
        self.game.play_sound(ZIPPERMOUTH)

    def update(self):
        """
        Update ZipperMouth
        """
        self.collide_player()
        if self.movement_start == self.movement_end and self.movement_delay < pygame.time.get_ticks():
            self.movement_start, self.movement_end, self.movement_delay = 0, 32, 0
            if self.collide_block():  # If no collision, animate movement
                self.movement_start, self.movement_end, self.movement_delay = 0, 0, 0
        elif self.movement_start != self.movement_end:
            self.animate_movement()
            if self.movement_start == self.movement_end:
                self.update_relative_pos()
                self.stationary()
                self.target = self.get_player_location()
                self.facing = self.get_next_direction()

    def collide_block(self):
        """
        Detects if ZipperMouth has collided with block.
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
        """
        Return true if collision, false otherwise
        """
        return pygame.sprite.spritecollide(self, object, False)

    def animate_movement(self):
        """
        Animate ZipperMouth movement.
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

    def stationary(self):
        """
        Resets ZipperMouth's sprite to stationary
        """
        if self.facing == DOWN:
            self.image = self.down_animations[0]
        elif self.facing == UP:
            self.image = self.up_animations[0]
        elif self.facing == LEFT:
            self.image = self.left_animations[0]
        elif self.facing == RIGHT:
            self.image = self.right_animations[0]

    def move_down(self):
        """
        Move ZipperMouth down
        """
        if self.movement_start < self.animation_frame_1:
            self.image = self.down_animations[1]
        elif self.movement_start < self.animation_frame_2:
            self.image = self.down_animations[0]
        elif self.movement_start < self.animation_frame_3:
            self.image = self.down_animations[2]
        else:
            self.image = self.down_animations[0]
        self.rect.y += self.speed

    def move_up(self):
        """
        Move ZipperMouth up
        """
        if self.movement_start < self.animation_frame_1:
            self.image = self.up_animations[1]
        elif self.movement_start < self.animation_frame_2:
            self.image = self.up_animations[0]
        elif self.movement_start < self.animation_frame_3:
            self.image = self.up_animations[2]
        else:
            self.image = self.up_animations[0]
        self.rect.y -= self.speed

    def move_left(self):
        """
        Move ZipperMouth left
        """
        if self.movement_start < self.animation_frame_1:
            self.image = self.left_animations[1]
        elif self.movement_start < self.animation_frame_2:
            self.image = self.left_animations[0]
        elif self.movement_start < self.animation_frame_3:
            self.image = self.left_animations[2]
        else:
            self.image = self.left_animations[0]
        self.rect.x -= self.speed

    def move_right(self):
        """
        Move ZipperMouth right
        """
        if self.movement_start < self.animation_frame_1:
            self.image = self.right_animations[1]
        elif self.movement_start < self.animation_frame_2:
            self.image = self.right_animations[0]
        elif self.movement_start < self.animation_frame_3:
            self.image = self.right_animations[2]
        else:
            self.image = self.right_animations[0]
        self.rect.x += self.speed

    def update_relative_pos(self):
        """
        Updates ZipperMouth's relative position.
        """
        if self.facing == UP:
            self.rel_y -= 32
        elif self.facing == DOWN:
            self.rel_y += 32
        elif self.facing == RIGHT:
            self.rel_x += 32
        elif self.facing == LEFT:
            self.rel_x -= 32

    def get_player_location(self):
        """
        Returns the player's current location.
        """
        return self.game.player.rel_y // 32, self.game.player.rel_x // 32

    def get_next_direction(self):
        """
        Returns ZipperMouth's next direction based on where the player is currently.
        """
        curr = self.rel_y // 32, self.rel_x // 32
        possible = []
        if self.target[0] > curr[0]:
            possible.append(DOWN)
        elif self.target[0] < curr[0]:
            possible.append(UP)
        if self.target[1] > curr[1]:
            possible.append(RIGHT)
        elif self.target[1] < curr[1]:
            possible.append(LEFT)

        if len(possible) > 0:
            return rd.choice(possible)
        return DOWN

    def defeat(self):
        """
        Remove ZipperMouth from screen.
        """
        self.image = self.game.enemy_sheet.get_sprite(128, 384, 32, 32)
        self.game.draw()
        self.kill()
        self.game.friend_eater = None


class Block(pygame.sprite.Sprite):
    """
    Represents a non-player area.
    """
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
    """
    Represents a tile the player can walk.
    """
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.ground
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
        self.poisoned = False
        self.poisoned_timer = 0

    def update(self):
        """
        Update the ground sprite.
        """
        if self.is_hitting_friendeater() and self.poisoned is False:
            self.image = self.game.terrain_sheet.get_sprite(32, 0, self.width, self.height)
            self.poisoned = True
            self.poisoned_timer = pygame.time.get_ticks() + 5000
        elif self.poisoned_timer < pygame.time.get_ticks() and self.poisoned is True:
            self.image = self.game.terrain_sheet.get_sprite(0, 0, self.width, self.height)
            self.poisoned = False
        if self.is_hitting_player() and self.is_poisoned() and self.game.player.invulnerable is False:
            self.game.play_sound(DAMAGE)
            self.game.player.kill_player()

    def is_hitting_friendeater(self):
        """
        Returns true if collision with friendeater, false otherwise
        """
        if isinstance(self.game.friend_eater, pygame.sprite.Sprite):
            return pygame.sprite.collide_rect(self.game.friend_eater, self)

    def is_hitting_player(self):
        """
        Returns true if collision with player, false otherwise
        """
        return pygame.sprite.collide_rect(self.game.player, self)

    def is_poisoned(self):
        """
        Returns true if ground is poisoned.
        """
        return self.poisoned


class Door(pygame.sprite.Sprite):
    """
    Represents a dungeon door.
    """
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
    """
    Represents a item.
    """
    def __init__(self, game):
        self.game = game
        self.groups = self.game.all_sprites, self.game.all_items
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        self.eat()

    def eat(self):
        hits = pygame.sprite.collide_rect(self.game.player, self)
        if hits:
            pygame.mixer.Sound.play(EAT)
            self.kill()
            self.game.fruit_count[self.code] += 1

    def eat_without_touch(self):
        pygame.mixer.Sound.play(EAT)
        self.kill()
        self.game.fruit_count[self.code] += 1
        self.game.loc.fruit -= 1


class Cherry(Item):
    """
    Represents a cherry
    """
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
    """
    Represents a banana
    """
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
    """
    Represents a melon
    """
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
    """
    Represents a grape
    """
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
    """
    Represents an orange
    """
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
    """
    Represents an apple.
    """
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
