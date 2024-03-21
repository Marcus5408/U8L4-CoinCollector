import pygame


class Fox:

    def __init__(self, x: int, y: int, bounds: tuple, sprite:str) -> None:
        self.x = x
        self.y = y
        self.bounds = bounds
        self.image = pygame.image.load(
            f"{__file__.replace('fox.py', '')}{sprite}"
        )
        self.image_size = self.image.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])
        self.delta = 4

    def move_direction(self, direction: str) -> None:
        if direction == "right" and self.x < self.bounds[0]:
            self.x = self.x + self.delta
        elif direction == "left" and self.x > 0:
            self.x = self.x - self.delta
        elif direction == "up" and self.y > 0:
            self.y = self.y - self.delta
        elif direction == "down" and self.y < self.bounds[1]:
            self.y = self.y + self.delta
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])
