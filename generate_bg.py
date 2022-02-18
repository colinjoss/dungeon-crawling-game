from PIL import Image
from func_timer import func_timer


@func_timer
def work():
    f1 = 'img/ocean600.png'
    bg = Image.open(f1, 'r')
    bg.save("img/ocean600-1.png", format='png')
    bg.close()

# if self.x_change > 0:
#     for sprite in self.game.all_sprites:
#         sprite.rect.x += PLAYER_SPEED
#     self.rect.x = hits[0].rect.left - self.rect.width
# if self.x_change < 0:
#     for sprite in self.game.all_sprites:
#         sprite.rect.x -= PLAYER_SPEED
#     self.rect.x = hits[0].rect.right

# if self.y_change > 0:
#     for sprite in self.game.all_sprites:
#         sprite.rect.y += PLAYER_SPEED
#     self.rect.y = hits[0].rect.top - self.rect.height
# if self.y_change < 0:
#     for sprite in self.game.all_sprites:
#         sprite.rect.y -= PLAYER_SPEED
#     self.rect.y = hits[0].rect.bottom
