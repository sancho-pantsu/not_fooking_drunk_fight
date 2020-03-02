import pygame


class Menu:
    def __init__(self, screen_size, color, button_size=(640, 180)):
        self.b_size = button_size
        self.buttons = []
        self.font = pygame.font.Font('data\\fonts\\Helicopta-YwXj.ttf', 150)
        self.bg = pygame.Surface(screen_size, 32)
        self.bg.set_alpha(150)
        self.screen_size = screen_size
        pygame.draw.rect(self.bg, (*color, 150), self.bg.get_rect())
        self.interval = 10

    def add_button(self, text, func=None, args=None, size=None, font_size=50, switch=False):
        if not size:
            size = self.b_size
        if len(self.buttons):
            b = self.buttons[-1]
            cords = b.cords
            cords = (cords[0], cords[1] + self.interval + size[1])
        else:
            cords = ((self.screen_size[0] - size[0]) // 2, (self.screen_size[1] - size[1]) // 2)

        self.buttons += [Button(text, size, func, args, cords, font_size, switch)]

        common_height = (len(self.buttons) - 1) * self.interval + sum(map(lambda x: x.size[1], self.buttons))
        delta = self.buttons[0].cords[1] - (self.screen_size[1] - common_height) // 2
        for i in self.buttons:
            i.cords = (i.cords[0], i.cords[1] - delta)

    def render(self, screen):
        screen.blit(self.bg, self.bg.get_rect())
        for i in self.buttons:
            screen.blit(i.image, i.cords)

    def clicked(self, pos, type=None, button=None):
        for i in self.buttons:
            i.update(pos, type, button)


class Button(pygame.sprite.Sprite):
    def __init__(self, text, size, func, args, cords=(0, 0), font_size=50, switch=False, text_color=(255, 0, 0)):
        super().__init__()
        self.func, self.args = func, args
        self.image = pygame.Surface(size)
        self.image.set_alpha(50)
        self.rect = pygame.rect.Rect([*cords, *size])
        self.text = text
        self.size = size
        self.color = (255, 255, 255)
        self.cords = cords
        self.text_color = text_color
        self.font = pygame.font.Font('data\\fonts\\Helicopta-YwXj.ttf', font_size)
        self.switch = switch
        self.crossed = False
        self.pressed = False
        self.mouse_in = False
        self.reload_image()

    def reload_image(self, alpha=50):
        self.image.set_alpha(alpha)
        pygame.draw.rect(self.image, self.color, self.rect, 5)
        line = self.font.render(self.text, True, (255, 255, 255))
        line_rect = line.get_rect()
        x = (self.rect.w - line_rect.w) // 2
        y = (self.rect.h - line_rect.h) // 2
        self.image.blit(line, (x, y))
        if self.crossed:
            pygame.draw.line(self.image, pygame.Color('red'), (0, 0), (self.rect.w - 1, self.rect.h - 1), 5)
            pygame.draw.line(self.image, pygame.Color('red'), (self.rect.w - 1, 0), (0, self.rect.h - 1), 5)

    def update(self, pos, event_type=None, event_button=None):
        self.rect = pygame.rect.Rect([*self.cords, *self.size])
        if event_type == pygame.MOUSEBUTTONDOWN and event_button == pygame.BUTTON_LEFT:
            if self.rect.collidepoint(*pos):
                if not self.pressed:
                    self.pressed = True
                    self.reload_image(200)
            else:
                self.reload_image()
                self.mouse_in = False
                self.pressed = False

        if event_type == pygame.MOUSEBUTTONUP and event_button == pygame.BUTTON_LEFT:
            if self.rect.collidepoint(*pos) and self.pressed:
                self.pressed = False
                if self.switch:
                    self.crossed = not self.crossed
                self.reload_image()
                if self.func is not None:
                    if self.args is not None:
                        self.func(self.args)
                    else:
                        self.func()
            else:
                self.reload_image()
                self.mouse_in = False
                self.pressed = False
        if event_type is None:
            if self.rect.collidepoint(*pos):
                if not self.mouse_in:
                    self.mouse_in = True
                    if not self.pressed:
                        self.reload_image(130)
            else:
                if not self.pressed:
                    self.reload_image()
                self.mouse_in = False
