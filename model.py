import pygame
import os
from PIL import Image


def load_image(name, colorkey=-1):
    image = pygame.image.load(name).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    im = Image.open(os.path.join('data', name))
    width, height = im.size
    return pygame.transform.scale(image, (250, 250)), pygame.Rect(0, 0, 250, 250)


class Model(pygame.sprite.Sprite):
    def __init__(self, paths):
        super().__init__()
        self.paths = paths
        self.frames = []
        for p in self.paths:
            sprite = pygame.sprite.Sprite()
            sprite.image, sprite.rect = load_image(p)
            self.frames += [sprite]
        self.cur_frame = 0
        self.sprite = self.frames[self.cur_frame]

    def update(self, x, y, cell, width, height):
        self.cur_frame = (self.cur_frame + 1) % (len(self.frames))
        self.sprite = self.frames[self.cur_frame]
        self.sprite.rect.x = x * cell + 1
        self.sprite.rect.y = height - self.sprite.rect.height - y * cell
        print(self.cur_frame)

    def reboot(self):
        self.cur_frame = 0
