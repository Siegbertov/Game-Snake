import random
import pygame


pygame.init()
pygame.display.set_caption("SNAKE")
clock = pygame.time.Clock()


class Cube(object):
    def __init__(self, position):
        self.position = position