import pygame


pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((672, 480))
        self.player = pygame.image.load('img/player1.png')
        self.bg = pygame.image.load('img/ocean600.png')
        self.rect = self.bg.get_rect()
        self.game_loop()

    def game_loop(self):
        x, y = 0, 0
        running = True
        while running:

            self.screen.fill('black')
            self.screen.blit(self.bg, self.rect)
            self.screen.blit(self.player, (x, y))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:

                    # Player movement
                    if event.key == pygame.K_LEFT:
                        x -= 32
                    if event.key == pygame.K_RIGHT:
                        x += 32
                    if event.key == pygame.K_UP:
                        y -= 32
                    if event.key == pygame.K_DOWN:
                        y += 32

            pygame.display.update()


class Map:
    def __init__(self):
        pass


class Player:
    def __init__(self):
        pass


if __name__ == '__main__':
    Game()
