import player
import pygame
import os

pygame.init()


class Game:
    def __init__(self, fps, width, cell_size, back_ground, player1, player2):
        self.FPS = fps
        self.width = width
        self.cell = cell_size
        self.player1 = player1
        self.player2 = player2
        self.bg = back_ground


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


g = Game(30, 1000, 1, 'ext_beach_sunset.jpg', player.Player([], ['default']),
         player.Player([], ['default']))

scale = 1
height = 500

ATTRACTION = 1
screen = pygame.display.set_mode((g.width * g.cell, height))
clock = pygame.time.Clock()
pygame.display.update()


def check_movement(m, p):
    if p.cords[0] + m[0] > g.width - p.width:
        m[0] = g.width - p.width - p.cords[0]
    elif p.cords[0] + m[0] < 0:
        m[0] = p.cords[0] * (-1)
    if p.cords[1] + m[1] <= 0:
        m[1] = 0
        p.cords[1] = 0
        g.player1.conditions['in_jump'] = False
    else:
        return True


def calc_jump_move(jump_v, start_cord, last_cord, t):
    cord = start_cord + jump_v * t - ATTRACTION * t ** 2 // 2
    g.player1.conditions['in_jump'][0] += 1
    g.player1.conditions['in_jump'][1] = cord
    return cord - last_cord


def move_player1():
    movement1 = [0, 0]
    if g.player1.conditions['in_jump']:
        v, strt_cord, last_cord, t = g.player1.jump_v, g.player1.conditions['in_jump'][2], \
                               g.player1.conditions['in_jump'][1], g.player1.conditions['in_jump'][0]
        movement1[1] += calc_jump_move(v, strt_cord, last_cord, t)
        movement1[0] += g.player1.conditions['in_jump'][3]
        if d['a']:
            movement1[0] -= 2
        if d['d']:
            movement1[0] += 2
    else:
        if d['a']:
            movement1[0] -= g.player1.speed
        if d['d']:
            movement1[0] += g.player1.speed

    check_movement(movement1, g.player1)
    g.player1.move(movement1)


d = {'a': False, 'd': False, 'w': False}

bg = load_image(g.bg)
bg = pygame.transform.scale(bg, (g.width * g.cell, height))

while True:

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:
            if i.unicode == 'a':
                d['a'] = True
            elif i.unicode == 'd':
                d['d'] = True
            elif i.unicode == 'w':
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
            if i.key == 97:
                d['a'] = False
            elif i.key == 100:
                d['d'] = False
            elif i.key == 119:
                d['w'] = False
    move_player1()
    g.player2.move([0, 0])

    screen.blit(bg, (0, 0))

    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(g.player1.cords[0] * g.cell, height - 100 - g.player1.cords[1],
                                                      50, 100))

    pygame.display.update()

    clock.tick(g.FPS)
