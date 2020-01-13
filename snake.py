import random
import pygame


pygame.init()
pygame.display.set_caption("SNAKE")
clock = pygame.time.Clock()


class Cube(object):
    def __init__(self, position):
        self.position = position

        
class Snake(object):
    body = []
    stomach = []
    UP = "UP"
    DOWN = "DOWN"
    RIGHT = "RIGHT"
    LEFT = "LEFT"

    def __init__(self, head_r, head_c, head_direction=RIGHT):
        self.body.append(Cube([head_r, head_c]))

        self.head_direction = head_direction

    def snake_position(self):
        all_snake_pos = []
        for el in self.body:
            all_snake_pos.append(el.position)
        return all_snake_pos