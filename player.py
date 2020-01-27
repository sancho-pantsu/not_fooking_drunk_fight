DEFAULT_CONDITIONS = {'in_jump': [], 'dead': False}
DEFAULT_EFFECTS = {}


class Player:
    def __init__(self, models, attacks, cord=0, hp=100, damage=5, speed=15, jump_v=15, effects=DEFAULT_EFFECTS,
                 conditions=DEFAULT_CONDITIONS):
        self.cords = [cord, 0]
        self.HP = hp
        self.damage = damage
        self.attacks = attacks
        self.effects = effects
        self.conditions = conditions
        self.models = models
        self.jump_v = jump_v
        self.speed = speed
        self.width = 50

    def damaged(self, damage):
        self.HP -= damage
        if self.HP <= 0:
            self.conditions['dead'] = True

    def move(self, movement):
        self.cords[0] += movement[0]
        self.cords[1] += movement[1]

    def jump_clicked(self, v=5):
        self.conditions['in_jump'] = True
        self.jump_v = v

    def update_data(self):
        if self.cords[1] == 0:
            self.conditions['in_jump'] = False
