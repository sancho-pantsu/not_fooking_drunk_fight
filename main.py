import player
import pygame
import os
import game


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


main_data = {}
f = open('data\\main_data.txt')
for i in f.readlines():
    var, val = i.split()
    if '.' not in i:
        main_data[var] = int(val)
    else:
        main_data[var] = float(val)
f.close()

HEIGHT = main_data['HEIGHT']
WIDTH = main_data['WIDTH']
CELL_SIZE = main_data['CELL_SIZE']
FPS = main_data['FPS']
ATTRACTION = main_data['ATTRACTION']


pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
sounds = {}
for i in os.listdir(os.getcwd() + '\\data\\sound\\effects\\'):
    sounds[i.split('.')[0]] = pygame.mixer.Sound('data\\sound\\effects\\' + i)
sounds['drunk_fight'].play()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.display.update()

#  making this shit beautiful

pygame.display.set_caption('drunk fight')
icon = load_image('data\\icon.png')
pygame.display.set_icon(icon)

#  that's all

g = game.Game(FPS, WIDTH, HEIGHT, CELL_SIZE, 'data\\bg.png')
PATH = os.getcwd() + '\\data\\'
g.player1 = player.Player(PATH + 'plr1', ['default'], {97: 'left', 100: 'right', 115: 'down', 119: 'up', 118: 'attack'})
g.player2 = player.Player(PATH + 'plr2', ['default'], {276: 'left', 275: 'right', 274: 'down', 273: 'up', 110: 'attack'})
g.player2.cords[0] = g.width - g.player2.size
g.players += [g.player1, g.player2]


def calc_jump_move(jump_v, start_cord, last_cord, t, p):
    cord = start_cord + jump_v * t - ATTRACTION * t ** 2 // 2
    p.conditions['in_jump'][0] += 2
    p.conditions['in_jump'][1] = cord
    return cord - last_cord


def check_movement(m, p):
    if p.cords[0] + m[0] > g.width - p.size:
        m[0] = g.width - p.size - p.cords[0]
    elif p.cords[0] + m[0] < 0:
        m[0] = p.cords[0] * (-1)
    if p.cords[1] + m[1] <= 0:
        m[1] = 0
        p.cords[1] = 0
        #nice
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
        if p.pressed_buttons['left']:
            if p.conditions['in_attack']:
                movement[0] -= p.speed // 3
            else:
                movement[0] -= p.speed
        if p.pressed_buttons['right']:
            if p.conditions['in_attack']:
                movement[0] += p.speed // 3
            else:
                movement[0] += p.speed
    if p.pressed_buttons['down'] and not p.conditions['in_attack']:
        p.conditions['crouch'] = True
    elif not p.pressed_buttons['down'] and not p.conditions['in_attack']:
        p.conditions['crouch'] = False
    check_movement(movement, p)
    p.move(movement)


def check_all_shit():
    for p in g.players:
        if p.cords[0] < 0:
            p.cords[0] = 0
        elif p.cords[0] > g.width:
            p.cords[0] = g.width
        if p.conditions['in_attack'] and not p.model.counter:
            p.model.reboot()
            p.conditions['in_attack'] = False


def check_all_shit1():
    for p in g.players:
        if p.conditions['in_attack']:
            for i in g.players:
                if id(p) != id(i) and pygame.sprite.collide_mask(p.model.attack_hitbox, i.model):
                    i.damaged(p.model.cur_damage)
                    if p.model.cur_damage:
                        i.sound('damaged')
                    p.model.cur_damage = 0


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
        im, rct = p.get_image(m, CELL_SIZE, WIDTH, HEIGHT, direction, crouch=p.conditions['crouch'], upd=upd)
        screen.blit(im, rct)
        direction = (direction + 1) % 2
    draw_hp_bars()
    pygame.display.update()


def draw_hitboxes():
    for p in g.players:
        if p.conditions['in_attack']:
            screen.blit(p.model.attack_hitbox.image, p.model.attack_hitbox.rect)


def draw_hp_bars():
    width = WIDTH // 2 - 50
    pygame.draw.rect(screen, (0, 0, 0), (20, 20, width, 50))
    bar1_width = int(g.players[0].HP / 100 * (width - 4))
    bar2_width = int(g.players[1].HP / 100 * (width - 4))
    if bar1_width < 0:
        bar1_width = 0
    if bar2_width < 0:
        bar2_width = 0
    pygame.draw.rect(screen, (255, 0, 0), (22 + width - 4 - bar1_width, 22, bar1_width, 46))
    pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 2 + 30, 20, WIDTH // 2 - 50, 50))
    pygame.draw.rect(screen, (255, 0, 0), (WIDTH // 2 + 32, 22, bar2_width, 46))


def timer(time, reverse=True, drawing=False):
    counter = 0
    if time > 15:
        time = 15
    frames = [load_image('data\\timer\\' + str(i) + '.png', -1) for i in range(time + 1)]
    table = int(reverse) * time
    while counter <= time:
        if drawing:
            draw()
            screen.blit(frames[table], drawing)
            pygame.display.update()
        if reverse:
            table -= 1
        else:
            table += 1
        counter += 1
        clock.tick(1)


d = {}
bg = load_image(g.bg)

timer(3, True, ((g.width - 200) // 2, (g.height - 200) // 2, 200, 200))

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
                        p.conditions['in_attack'] = True
                        p.sound('attack')
                        p.model = p.models['in_attack']
                    if p.buttons[key] == 'down' and not p.conditions['in_attack']:
                        p.conditions['crouch'] = True
                    elif p.buttons[key] == 'up' and not p.conditions['in_jump'] and not p.conditions['in_jump']:
                        p.conditions['in_jump'] = [1, p.cords[1], p.cords[1]]
                        p.sound('jump')
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
                    if p.buttons[key] == 'down' and not p.conditions['in_attack']:
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
    check_all_shit1()
    #for p in g.players:
    #    print(p.HP, end=' ')
    #print()
    clock.tick(g.FPS)
