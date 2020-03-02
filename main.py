import menu
import player
import pygame
import os
import game


DEFAULT_CONDITIONS = {'in_jump': [], 'dead': False, 'staying': True, 'crouch': False, 'in_attack': False}
DEFAULT_EFFECTS = {}


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
music_box = pygame.mixer.music
music_box.set_volume(0.2)
sounds = {}
for i in os.listdir(os.getcwd() + '\\data\\sound\\effects\\'):
    s = pygame.mixer.Sound('data\\sound\\effects\\' + i)
    s.set_volume(1.5)
    sounds[i.split('.')[0]] = s
sounds['drunk_fight'].play()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.display.update()
main_font = pygame.font.Font('data\\fonts\\Helicopta-YwXj.ttf', 200)
timer_font = pygame.font.Font('data\\fonts\\Youmurdererbb-pwoK.otf', 200)

#  making this shit beautiful

pygame.display.set_caption('drunk fight')
icon = load_image('data\\icon.png')
pygame.display.set_icon(icon)
pygame.mouse.set_visible(False)

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
                movement[0] -= p.speed // 2
            else:
                movement[0] -= p.speed
        if p.pressed_buttons['right']:
            if p.conditions['in_attack']:
                movement[0] += p.speed // 2
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
    i = 0
    for p in g.players:
        if p.conditions['dead']:
            music_box.set_volume(0.05)
            snds = [p.sound('death', True)]
            for pp in g.players:
                if id(pp) != id(p):
                    snds += [pp.sound('win_phrase', True)]
                    snds += [pp.sound('win', True)]
            for snd in snds:
                snd.play()
                pygame.time.delay(int(snd.get_length() * 1000 + 1000))
            call_menu(finish_menu, False)
            music_box.set_volume(0.2)
            break


def draw():
    global bg, last_draw
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
    last_draw = screen.copy()
    pygame.display.update()


def draw_minimal():
    screen.blit(last_draw, (0, 0))


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


def timer(time, fnt, final='0', color=(0, 0, 0), tick=sounds['tick'], final_sound=sounds['fight'],
          reverse=True, drawing=[]):
    counter = 0
    if reverse:
        table = time
    else:
        table = 0
    while counter <= time:
        if table == final:
            final_sound.play()
        else:
            tick.play()
        if drawing:
            draw_minimal()
            text = fnt.render(str(table), 0, color)
            rct = text.get_rect()
            if drawing[0]:
                screen.blit(text, (drawing[1] - rct[2] // 2, drawing[2] - rct[3] // 2))
            else:
                screen.blit(text, (drawing[1], drawing[2]))
            pygame.display.update()
        counter += 1
        if reverse:
            table = time - counter
        else:
            table = counter
        if not table:
            table = final
        clock.tick(1)


d = {}
bg = load_image(g.bg)
last_draw = pygame.Surface((100, 100))


draw()
timer(4, timer_font, 'Fight!', (255, 0, 0), reverse=True, final_sound=sounds['fight'],
      drawing=(True, g.width//2, g.height//2))

music_box.load('data\\sound\\music\\main_theme.wav')
music_box.play(loops=100)


def call_menu(m, esc):
    draw()
    music_box.set_volume(0.05)
    sos = False
    while True:
        pygame.mouse.set_visible(True)
        draw_minimal()
        m.render(screen)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == 27:
                    sos = esc
                    break
            elif e.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                if m.clicked(e.pos, e.type, e.button):
                    sos = True
                    break
            elif e.type == pygame.MOUSEMOTION:
                m.clicked(e.pos)
        if sos:
            music_box.set_volume(0.2)
            pygame.mouse.set_visible(False)
            break


def restart():
    global g, d
    i = 0
    music_box.stop()
    draw()
    d = {}
    for p in g.players:
        p.HP = 100
        p.cords = [(g.width - p.size) * i, 0]
        p.pressed_buttons = {}
        for b in p.buttons:
            p.pressed_buttons[p.buttons[b]] = False
        p.conditions = DEFAULT_CONDITIONS.copy()
        p.effects = DEFAULT_EFFECTS.copy()
        for m in p.models:
            p.models[m].reboot()
        i += 1
    timer(4, timer_font, 'Fight!', (255, 0, 0), reverse=True, final_sound=sounds['fight'],
          drawing=(True, g.width//2, g.height//2))
    music_box.load('data\\sound\\music\\main_theme.wav')
    music_box.play(loops=100)


def nothing():
    pass


def_menu = menu.Menu((g.width, g.height), (0, 0, 0), (640, 180))

def_menu.add_button('continue', nothing)
def_menu.add_button('restart', restart)
def_menu.add_button('exit', exit)
def_menu.render(screen)

finish_menu = menu.Menu((g.width, g.height), (0, 0, 0), (640, 180))

finish_menu.add_button('restart', restart)
finish_menu.add_button('exit', exit)

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:
            d[i.key] = True
            key = i.key
            if key == 27:
                call_menu(def_menu, True)
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
    clock.tick(g.FPS)

