import player
import pygame
import os

pygame.init()


class Game:
    def __init__(self, fps, width, height, cell_size, back_ground):
        self.FPS = fps
        self.width = width
        self.height = height
        self.cell = cell_size
        self.bg = back_ground
        self.all_sprites = pygame.sprite.Group()


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
screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))

g = Game(32, WIDTH, HEIGHT, CELL_SIZE, 'bg.png')
g.player1 = player.Player('D:\\!programming\\Projects\\not_fookin_drunk_fight\\not_fooking_drunk_fight\\sprites\\plr1',
                          ['default'])
g.player2 = player.Player('D:\\!programming\\Projects\\not_fookin_drunk_fight\\not_fooking_drunk_fight\\sprites\\plr2',
                          ['default'], cord=2000)

scale = 1

ATTRACTION = 1

clock = pygame.time.Clock()
pygame.display.update()


def calc_jump_move(jump_v, start_cord, last_cord, t, p):
    cord = start_cord + jump_v * t - ATTRACTION * t ** 2 // 2
    p.conditions['in_jump'][0] += 1
    p.conditions['in_jump'][1] = cord
    return cord - last_cord


def check_movement(m, p):
    if p.cords[0] + m[0] > g.width - p.models['default'].sprite.rect.width:
        m[0] = g.width - p.width - p.cords[0]
    elif p.cords[0] + m[0] < 0:
        m[0] = p.cords[0] * (-1)
    if p.cords[1] + m[1] <= 0:
        m[1] = 0
        p.cords[1] = 0
        p.conditions['in_jump'] = False
    else:
        return True


def move_player(p):
    movement1 = [0, 0]
    if p.conditions['in_jump']:
        v, strt_cord, last_cord, t = p.jump_v, p.conditions['in_jump'][2], \
                               p.conditions['in_jump'][1], p.conditions['in_jump'][0]
        movement1[1] += calc_jump_move(v, strt_cord, last_cord, t, g.player1)
        movement1[0] += p.conditions['in_jump'][3]
        if d['a']:
            movement1[0] -= 2
        if d['d']:
            movement1[0] += 2
    else:
        if d['a']:
            movement1[0] -= p.speed
        if d['d']:
            movement1[0] += p.speed
    check_movement(movement1, p)
    p.move(movement1)


def draw():
    screen.blit(bg, (0, 0))
    #  print((g.player1.cords[0] * g.cell, HEIGHT - 500 - g.player1.cords[1]))
    direction = int(g.player1.cords[0] - g.player2.cords[0] < 0)
    for p in [g.player1, g.player2]:
        m = 'default'
        print(p.conditions)
        for i in ['in_jump', 'crouch']:
            if p.conditions[i]:
                m = i
                break
        print(m)
        upd = True
        if p.conditions['staying']:
            upd = False
        im, rct = p.get_image(m, CELL_SIZE, WIDTH, HEIGHT, upd=upd)
        im = pygame.transform.flip(im, direction, 0)
        screen.blit(im, rct)
    pygame.display.update()


d = {'a': False, 'd': False, 'w': False}

bg = load_image(g.bg)
bg = pygame.transform.scale(bg, (g.width * g.cell, g.height * g.cell))

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:
            d[i.key] = True
            if i.key == 97:
                d['a'] = True
            elif i.key == 100:
                d['d'] = True
            elif i.key == 115:
                d['s'] = False
                g.player1.conditions['crouch'] = True
            elif i.key == 119:
                if not g.player1.conditions['in_jump']:
                    g.player1.conditions['in_jump'] = [1, g.player1.cords[1], g.player1.cords[1]]
                    if d['d'] and not d['a']:
                        g.player1.conditions['in_jump'] += [g.player1.speed]
                    elif d['a'] and not d['d']:
                        g.player1.conditions['in_jump'] += [g.player1.speed * -1]
                    else:
                        g.player1.conditions['in_jump'] += [0]
                d['w'] = True
        elif i.type == pygame.KEYUP:
            print(i.key)
            if i.key == 97:
                d['a'] = False
            elif i.key == 100:
                d['d'] = False
            elif i.key == 119:
                d['w'] = False
            elif i.key == 115:
                d['s'] = False
                g.player1.conditions['crouch'] = False
    if not (d['a'] and d['d']) and (d['a'] or d['d']):
        g.player1.conditions['staying'] = False
    else:
        g.player1.conditions['staying'] = True
    move_player(g.player1)
    #  g.player2.move([0, 0])
    draw()
    clock.tick(g.FPS)
