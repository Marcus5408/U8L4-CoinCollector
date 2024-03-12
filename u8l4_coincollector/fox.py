import pygame


class Fox:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("orange-fox-sprite.png")
        self.image_size = self.image.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])
        self.delta = 0.1

    def move_direction(self, direction):
        if direction == "right":
            self.x = self.x + self.delta
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])
