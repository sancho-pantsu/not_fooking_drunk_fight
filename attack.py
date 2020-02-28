import pygame
import hitbox
import model


class Attack(model.Model):
    def __init__(self, damage, effects, paths, height):
        super().__init__(paths, height)
        self.damage = damage
        self.cur_damage = damage
        self.effects = effects
        self.counter = len(self.frames['default'])

    def update(self, x, y, cell, width, height, *another_shit):
        super().update(x, y, cell, width, height, True)
        self.counter -= 1
        print(self.counter)

    def reboot(self):
        super().reboot()
        self.counter = len(self.frames['default'])
        self.cur_damage = self.damage
