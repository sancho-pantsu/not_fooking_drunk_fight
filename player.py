import os
import model

DEFAULT_CONDITIONS = {'in_jump': [], 'dead': False, 'staying': True, 'crouch': False}
DEFAULT_EFFECTS = {}


class Player:
    def __init__(self, models, attacks, buttons, cord=0, hp=100, damage=5, speed=7, jump_v=15, effects=DEFAULT_EFFECTS,
                 conditions=DEFAULT_CONDITIONS):
        self.cords = [cord, 0]
        self.HP = hp
        self.damage = damage
        self.attacks = attacks
        self.effects = effects.copy()
        self.conditions = conditions.copy()
        self.load_models(models)
        self.jump_v = jump_v
        self.speed = speed
        self.buttons = buttons
        self.rect = self.models['default'].sprite.rect
        self.pressed_buttons = {}
        for i in self.buttons:
            self.pressed_buttons[self.buttons[i]] = False

    def damaged(self, damage):
        self.HP -= damage
        if self.HP <= 0:
            self.conditions['dead'] = True

    def move(self, movement):
        self.cords[0] += movement[0]
        self.cords[1] += movement[1]

    def jump_clicked(self, v=5):
        self.jump_v = v

    def update_data(self):
        if self.cords[1] == 0:
            self.conditions['in_jump'] = []
        self.rect = model.sprite.rect

    def load_models(self, m):
        models = {}
        for i in os.listdir(m):
            if '.' not in i:
                models[i] = model.Model([m + '\\' + i + '\\' + x for x in os.listdir(m + '\\' + i)])
        self.models = models

    def get_image(self, m, cell, width, height, upd=True):
        model = self.models[m]
        self.models[m].update(*self.cords, cell, width, height, upd)
        self.rect = model.sprite.rect
        return [model.sprite.image, model.sprite.rect]
