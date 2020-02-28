import player
import pygame
import os
import model
import attack

pygame.init()


class Game:
    def __init__(self, fps, width, height, cell_size, back_ground):
        self.FPS = fps
        self.width = width
        self.height = height
        self.cell = cell_size
        self.bg = back_ground
        self.all_sprites = pygame.sprite.Group()
        self.players = []


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


HEIGHT = 900
WIDTH = 1600
CELL_SIZE = 1
FPS = 32
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

g = Game(FPS, WIDTH, HEIGHT, CELL_SIZE, 'bg.png')
PATH = os.getcwd() + '\\sprites\\'
g.player1 = player.Player(PATH + 'plr1', ['default'], {97: 'left', 100: 'right', 115: 'down', 119: 'up', 118: 'attack'})
g.player2 = player.Player(PATH + 'plr2', ['default'], {276: 'left', 275: 'right', 274: 'down', 273: 'up', 110: 'attack'}, g.width - 400)

g.players += [g.player1, g.player2]

scale = 1

ATTRACTION = 0.5

clock = pygame.time.Clock()
pygame.display.update()


def calc_jump_move(jump_v, start_cord, last_cord, t, p):
    cord = start_cord + jump_v * t - ATTRACTION * t ** 2 // 2
    p.conditions['in_jump'][0] += 2
    p.conditions['in_jump'][1] = cord
    return cord - last_cord


def check_movement(m, p):
    if p.cords[0] + m[0] > g.width - p.model.sprite.rect.width:
        m[0] = g.width - p.rect.width - p.cords[0]
    elif p.cords[0] + m[0] < 0:
        m[0] = p.cords[0] * (-1)
    if p.cords[1] + m[1] <= 0:
        m[1] = 0
        p.cords[1] = 0
        p.conditions['in_jump'] = False
    else:
        return True


def move_player(p):
    movement = [0, 0]
    if p.conditions['in_jump']:
        v, strt_cord, last_cord, t = p.jump_v, p.conditions['in_jump'][2], \
                               p.conditions['in_jump'][1], p.conditions['in_jump'][0]
        movement[1] += calc_jump_move(v, strt_cord, last_cord, t, p)
        movement[0] += p.conditions['in_jump'][3]
        if p.pressed_buttons['left']:
            movement[0] -= 2
        if p.pressed_buttons['right']:
            movement[0] += 2
    else:
        if p.pressed_buttons['left'] and not p.conditions['in_attack']:
            movement[0] -= p.speed
        if p.pressed_buttons['right'] and not p.conditions['in_attack']:
            movement[0] += p.speed
    check_movement(movement, p)
    p.move(movement)


def check_all_shit():
    for p in g.players:
        if p.cords[0] < 0:
            p.cords[0] = 0
        elif p.cords[0] > g.width:
            p.cords[0] = g.width
        if p.conditions['in_attack'] and not p.conditions['in_attack'].counter:
            p.conditions['in_attack'].reboot()
            print(p.conditions['in_attack'].cur_frame)
            p.conditions['in_attack'] = False
        if p.conditions['in_attack']:
            for i in g.players:
                if id(p) != id(i) and p.conditions['in_attack'].hitbox.collision(i.hitbox):
                    i.damaged(p.conditions['in_attack'].cur_damage)
                    p.conditions['in_attack'].cur_damage = 0


def draw():
    global bg
    b = pygame.transform.scale(bg, (int(g.width * g.cell), int(g.height * g.cell)))
    screen.fill((0, 0, 0))
    screen.blit(b, (0, 0))
    direction = int(g.player1.cords[0] - g.player2.cords[0] < 0)
    for p in g.players:
        m = 'default'
        for i in ['in_jump', 'in_attack']:
            if p.conditions[i]:
                m = i
                break
        upd = True
        if p.conditions['staying']:
            upd = False
        im, rct = p.get_image(m, CELL_SIZE, WIDTH, HEIGHT, crouch=p.conditions['crouch'], upd=upd)
        im = pygame.transform.flip(im, direction, 0)
        screen.blit(im, rct)
    draw_hitboxes()
    pygame.display.update()


def draw_hitboxes():
    for p in g.players:
        pygame.draw.rect(screen, (255, 0, 0), tuple(map(lambda x: int(x * g.cell), p.hitbox.get_rect())))
        if p.conditions['in_attack']:
            pygame.draw.rect(screen, (255, 0, 0), tuple(map(lambda x: int(x * g.cell), p.conditions['in_attack'].hitbox.get_rect())))


d = {}

bg = load_image(g.bg)

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:
            d[i.key] = True
            key = i.key
            for p in g.players:
                if key in p.buttons:
                    p.pressed_buttons[p.buttons[key]] = True
                    if p.buttons[key] == 'attack' and not p.conditions['in_attack'] and not p.conditions['in_jump']:
                        p.conditions['in_attack'] = p.models['in_attack']
                    if p.buttons[key] == 'down':
                        p.conditions['crouch'] = True
                    elif p.buttons[key] == 'up' and not p.conditions['in_jump'] and not p.conditions['in_jump']:
                        p.conditions['in_jump'] = [1, p.cords[1], p.cords[1]]
                        if p.pressed_buttons['right'] and not p.pressed_buttons['left']:
                            p.conditions['in_jump'] += [p.speed]
                        elif p.pressed_buttons['left'] and not p.pressed_buttons['right']:
                            p.conditions['in_jump'] += [p.speed * -1]
                        else:
                            p.conditions['in_jump'] += [0]
        elif i.type == pygame.KEYUP:
            key = i.key
            for p in g.players:
                if key in p.buttons:
                    p.pressed_buttons[p.buttons[key]] = False
                    if p.buttons[key] == 'down':
                        p.conditions['crouch'] = False
    for p in g.players:
        if not (p.pressed_buttons['left'] and p.pressed_buttons['right']) and \
                (p.pressed_buttons['left'] or p.pressed_buttons['right']):
            p.conditions['staying'] = False
        else:
            p.conditions['staying'] = True
    for p in g.players:
        move_player(p)
    check_all_shit()
    draw()
    #for p in g.players:
    #    print(p.HP, end=' ')
    #print()
    clock.tick(g.FPS)
