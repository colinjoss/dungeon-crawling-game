from PIL import Image
from func_timer import func_timer


@func_timer
def work():
    f1 = 'img/ocean600.png'
    bg = Image.open(f1, 'r')
    bg.save("img/ocean600-1.png", format='png')
    bg.close()
