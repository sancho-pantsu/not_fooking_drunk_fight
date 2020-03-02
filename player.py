import random

import model
import attack
import os
import pygame

DEFAULT_CONDITIONS = {'in_jump': [], 'dead': False, 'staying': True, 'crouch': False, 'in_attack': False}
DEFAULT_EFFECTS = {}
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)


class Player:
    def __init__(self, data, attacks, buttons, cord=0, hp=100, damage=5, speed=10, jump_v=17, effects=DEFAULT_EFFECTS,
                 conditions=DEFAULT_CONDITIONS):
        self.cords = [cord, 0]
        self.HP = hp
        self.damage = damage
        self.attacks = attacks
        self.effects = effects.copy()
        self.sounds = {'death': [], 'damaged': [], 'attack': [], 'jump': [], 'win': [], 'win_phrase': []}
        for i in os.listdir(data + '\\sound'):
            s = pygame.mixer.Sound(data + '\\sound\\' + i)
            s.set_volume(1.5)
            self.sounds[''.join(filter(lambda x: not x.isdecimal(), i.split('.')[0]))] += [s]
        f = open(data + '\\size.txt')
        self.size = tuple(map(int, f.read().split()))
        f.close()
        self.size = 500
        self.conditions = conditions.copy()
        self.load_models(data + '\\sprites')
        self.rect = self.models['default'].rect
        self.model = self.models['default']
        self.jump_v = jump_v
        self.speed = speed
        self.buttons = buttons
        self.pressed_buttons = {}
        for i in self.buttons:
            self.pressed_buttons[self.buttons[i]] = False

    def damaged(self, damage):
        self.HP -= damage
        if self.HP <= 0:
            self.conditions['dead'] = True

    def sound(self, name):
        return random.choice(self.sounds[name]).play()

    def move(self, movement):
        self.cords[0] += movement[0]
        self.cords[1] += movement[1]

    def load_models(self, d):
        models = {}
        for i in os.listdir(d):
            if '.' not in i:
                if 'attack' in i:
                    f = open(d + '\\' + i + '\\' + 'info.txt')
                    text = f.read()
                    f.close()
                    dmg, effects = int(text.split(';')[0]), text.split(';')[1].split(',')
                    models[i] = attack.Attack(dmg,
                                              effects, [[d + '\\' + i + '\\default\\' + x for x in os.listdir(d + '\\' + i +
                                              '\\default')], [d + '\\' + i + '\\crouch\\' + x for x in os.listdir(d + '\\' + i +
                                              '\\crouch')]], self.size)
                else:
                    models[i] = model.Model([[d + '\\' + i + '\\default\\' + x for x in os.listdir(d + '\\' + i +
                                              '\\default')], [d + '\\' + i + '\\crouch\\' + x for x in os.listdir(d + '\\' + i +
                                              '\\crouch')]], self.size)
        self.models = models

    def get_image(self, m, cell, width, height, direction, crouch=False, upd=True):
        model = self.models[m]
        self.models[m].update(*self.cords, cell, width, height, direction, crouch=crouch, upd=upd)
        self.rect = model.rect
        self.model = model
        return [model.image, model.rect]
