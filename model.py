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
            sze = self.size
        return pygame.transform.scale(image, sze), pygame.Rect(0, 0, *sze)

    def __init__(self, paths, size):
        super().__init__()
        self.paths = paths
        self.size = size
        self.default_frames = []
        self.crouch_frames = []
        self.last_cell = 0
        self.hitbox = False
        self.crouch_hitboxes = {}
        self.default_hitboxes = {}
        frames = [self.default_frames, self.crouch_frames]
        hitboxes = [self.default_hitboxes, self.crouch_hitboxes]
        i = 0
        for folder in self.paths:
            for p in folder:
                if '.png' not in p and '.PNG' not in p:
                    if 'hitbox.txt' in p:
                        f = open(p)
                        self.hitbox = hitbox.HitBox(*map(int, f.read().split()))
                        f.close()
                    elif '.txt' in p and 'info' not in p:
                        f = open(p)
                        hitboxes[i][int(p.split('\\')[-1].split('.')[0])] = hitbox.HitBox(*map(int, f.read().split()))
                        f.close()
                    continue
                sprite = pygame.sprite.Sprite()
                sprite.image, sprite.rect = self.load_image(p, size)
                im = sprite.image
                frames[i] += [(sprite, im, int(p.split('.')[0].split('\\')[-1]))]
            if self.hitbox:
                for j in range(len(frames[i])):
                    hitboxes[i][j] = self.hitbox
            frames[i].sort(key=lambda x: x[-1])
            i += 1
            self.hitbox = False

        self.frames = {'default': self.default_frames, 'crouch': self.crouch_frames}
        self.hitboxes = {'default': self.default_hitboxes, 'crouch': self.crouch_hitboxes}
        self.cur_frame = 0
        self.sprite = self.default_frames[self.cur_frame][0]
        self.hitbox = self.default_hitboxes[self.cur_frame]

    def update(self, x, y, cell, width, height, direction, crouch=False, upd=True):
        condition = int(crouch) * 'crouch' + int((crouch + 1) % 2) * 'default'
        if upd:
            self.cur_frame = (self.cur_frame + 1) % (len(self.frames[condition]))
        self.sprite = self.frames[condition][self.cur_frame][0]
        self.hitbox = self.hitboxes[condition][self.cur_frame]
        if cell != self.last_cell:
            self.last_cell = cell
            self.sprite.image = pygame.transform.scale(self.frames[condition][self.cur_frame][1],
                                                       (int(self.size[0] * cell), int(self.size[1] * cell)))
        else:
            self.sprite.image = self.frames[condition][self.cur_frame][1]
        self.sprite.rect = pygame.Rect(0, 0, int(self.size[0] * cell), int(self.size[1] * cell))
        self.sprite.rect.x = int(x * cell) + 1
        self.sprite.rect.y = int((height - self.sprite.rect.height / cell - y) * cell)
        if direction == 'sos':
            print(direction)
        if direction == 'sos' and self.size[0] != self.size[1]:
            self.sprite.rect.x -= (self.size[0] - self.size[1])
        if direction == 'sos' or direction == 1:
            self.hitbox.left = self.sprite.rect.x + self.sprite.rect.width - self.hitbox.margin_left - self.hitbox.width
            self.hitbox.top = self.sprite.rect.y + self.hitbox.margin_top
        else:
            self.hitbox.move(self.sprite.rect.x, self.sprite.rect.y)

    def reboot(self):
        self.cur_frame = 0
