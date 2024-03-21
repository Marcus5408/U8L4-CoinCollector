from random import randint
import pygame


class Bomb:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(
            f"{__file__.replace('bomb.py', '')}bomb-sprite.png"
        )
        self.image_size = self.image.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])

    def set_location(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])

    def new_location(self, window_width):
        self.x = randint(0, window_width - self.image_size[0])
        self.y = 0 - self.image_size[1]
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])
