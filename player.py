import model
import attack
import os

DEFAULT_CONDITIONS = {'in_jump': [], 'dead': False, 'staying': True, 'crouch': False, 'in_attack': False}
DEFAULT_EFFECTS = {}


class Player:
    def __init__(self, models, attacks, buttons, cord=0, hp=100, damage=5, speed=7, jump_v=17, effects=DEFAULT_EFFECTS,
                 conditions=DEFAULT_CONDITIONS):
        self.cords = [cord, 0]
        self.HP = hp
        self.damage = damage
        self.attacks = attacks
        self.effects = effects.copy()
        f = open(models + '\\size.txt')
        self.size = tuple(map(int, f.read().split()))
        f.close()
        self.size = 500
        self.conditions = conditions.copy()
        self.load_models(models)
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

    def move(self, movement):
        self.cords[0] += movement[0]
        self.cords[1] += movement[1]

    def load_models(self, m):
        models = {}
        for i in os.listdir(m):
            if '.' not in i:
                if 'attack' in i:
                    f = open(m + '\\' + i + '\\' + 'info.txt')
                    text = f.read()
                    f.close()
                    dmg, effects = int(text.split(';')[0]), text.split(';')[1].split(',')
                    models[i] = attack.Attack(dmg,
                                              effects, [[m + '\\' + i + '\\default\\' + x for x in os.listdir(m + '\\' + i +
                                              '\\default')], [m + '\\' + i + '\\crouch\\' + x for x in os.listdir(m + '\\' + i +
                                              '\\crouch')]], self.size)
                else:
                    models[i] = model.Model([[m + '\\' + i + '\\default\\' + x for x in os.listdir(m + '\\' + i +
                                              '\\default')], [m + '\\' + i + '\\crouch\\' + x for x in os.listdir(m + '\\' + i +
                                              '\\crouch')]], self.size)
        self.models = models

    def get_image(self, m, cell, width, height, direction, crouch=False, upd=True):
        model = self.models[m]
        self.models[m].update(*self.cords, cell, width, height, direction, crouch=crouch, upd=upd)
        self.rect = model.rect
        self.model = model
        return [model.image, model.rect]
