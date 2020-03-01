import hitbox
import pygame
from PIL import Image


class Model(pygame.sprite.Sprite):
    def load_image(self, name, size, colorkey=-1):
        image = pygame.image.load(name)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
            image = image.convert()
        else:
            image = image.convert_alpha()
        m = Image.open(name)
        if type(size) != tuple:
            width, height = m.size
            self.size = (int(size / height * width), size)
        return pygame.transform.scale(image, self.size), pygame.Rect(0, 0, *self.size)

    def __init__(self, paths, size, attack=False):
        super().__init__()
        self.attack = attack
        self.paths = paths
        self.size = size
        self.default_common_hitboxes = []
        self.crouch_common_hitboxes = []
        common_hitboxes = [self.default_common_hitboxes, self.crouch_common_hitboxes]
        i = 0
        if attack:
            self.default_hitboxes = []
            self.crouch_hitboxes = []
            hitboxes = [self.default_hitboxes, self.crouch_hitboxes]
        for folder in self.paths:
            for p in folder:
                if attack and 'hitbox' in p:
                    sprite = pygame.sprite.Sprite()
                    sprite.image, sprite.rect = self.load_image(p, size)
                    hitboxes[i] += [(sprite, int(p.split('.')[0].split('\\')[-1].replace('hitbox', '')))]
                    continue
                im, rect = self.load_image(p, size)
                common_hitboxes[i] += [(im, int(p.split('.')[0].split('\\')[-1]))]
            common_hitboxes[i].sort(key=lambda x: x[-1])
            if attack:
                hitboxes[i].sort(key=lambda x: x[-1])
            i += 1
        self.common_hitboxes = {'default': self.default_common_hitboxes, 'crouch': self.crouch_common_hitboxes}
        if attack:
            self.attack_hitboxes = {'default': self.default_hitboxes, 'crouch': self.crouch_hitboxes}
        self.cur_frame = 0
        self.rect = self.default_common_hitboxes[self.cur_frame][0].get_rect()

    def update(self, x, y, cell, width, height, direction, crouch=False, upd=True):
        condition = int(crouch) * 'crouch' + int((crouch + 1) % 2) * 'default'
        if upd:
            self.cur_frame = (self.cur_frame + 1) % (len(self.common_hitboxes[condition]))
        if self.attack:
            self.attack_hitbox = pygame.sprite.Sprite()
            self.attack_hitbox.image = self.attack_hitboxes[condition][self.cur_frame][0].image.copy()
            self.attack_hitbox.rect = self.attack_hitboxes[condition][self.cur_frame][0].rect.copy()
        self.image = self.common_hitboxes[condition][self.cur_frame][0].copy()
        if direction:
            self.image = pygame.transform.flip(self.image, 1, 0)
            if self.attack:
                self.attack_hitbox.image = pygame.transform.flip(self.attack_hitbox.image, 1, 0)
        st = [self]
        if self.attack:
            st += [self.attack_hitbox]
        for i in st:
            i.rect = pygame.Rect(0, 0, self.size[0], self.size[1])
            i.rect.x = x + 1
            i.rect.y = height - i.rect.height - y
            if not direction == 'sos' and self.size[0] != self.size[1]:
                i.rect.x -= (self.size[0] - self.size[1])

    def reboot(self):
        self.cur_frame = 0
