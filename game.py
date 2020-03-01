import pygame


class Game:
    def __init__(self, fps, width, height, cell_size, back_ground):
        self.FPS = fps
        self.width = width
        self.height = height
        self.cell = cell_size
        self.bg = back_ground
        self.all_sprites = pygame.sprite.Group()
        self.players = []
