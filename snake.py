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


class Game:
    WIDTH = 600
    HEIGHT = WIDTH

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 200, 0)
    text_font = pygame.font.Font("freesansbold.ttf", 20)

    ROW_NUM = 20

    def __init__(self):
        self.lose_flag = False
        self.run = True
        self.ceil_size = self.WIDTH // self.ROW_NUM
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.newSnake = Snake(self.ROW_NUM-2, 1)
        self.newFood = self.create_new_food()

    # TODO                                                                                            CREATING NEW FOOD
    def all_possible_positions(self):
        all_poss_pos = []
        for r in range(self.ROW_NUM):
            for c in range(self.ROW_NUM):
                poss = [r, c]
                if poss not in self.newSnake.snake_position():
                    all_poss_pos.append(poss)
        return all_poss_pos

    def create_new_food(self):
        return Cube(random.choice(self.all_possible_positions()))

    # TODO                                                                                                 CHECKING LOSE
    def snake_bites_itself(self):
        if len(self.newSnake.body) >= 2:
            for i in range(1, len(self.newSnake.body)):
                if self.newSnake.body[0].position == self.newSnake.body[i].position:
                    return True
        return False

    # YOU CAN YOU THIS IF YOU WANT PLAY WITH BORDERS
    def snake_hits_border(self):
        r, c = self.newSnake.body[0].position[0], self.newSnake.body[0].position[1]
        if r<0 or r>self.ROW_NUM-1 or c<0 or c>self.ROW_NUM-1:
            return True
        return False

    def check_lose(self):
        if self.snake_bites_itself() or self.snake_hits_border():
            self.lose_flag = True

    # TODO                                                                                                 SNAKE MOVING
    def snake_bites_food(self):
        if self.newSnake.body[0].position == self.newFood.position:
            self.newSnake.stomach.append(self.newFood.position)
            self.newFood = self.create_new_food()

    def snake_should_expand(self):
        if self.newSnake.stomach and self.newSnake.body[-1].position == self.newSnake.stomach[0]:
            self.newSnake.stomach.pop(0)
            return True
        return False

    def next_position_of_head(self):
        r, c = self.newSnake.body[0].position[0], self.newSnake.body[0].position[1]

        # YOU CAN DELETE checker for r and c IF YOU WANT PLAY WITH BORDERS

        if self.newSnake.head_direction == self.newSnake.UP:
            if r == 0:
                r = 20
            return [r-1, c]
        if self.newSnake.head_direction == self.newSnake.DOWN:
            if r == 19:
                r = -1
            return [r+1, c]
        if self.newSnake.head_direction == self.newSnake.RIGHT:
            if c == 19:
                c = -1
            return [r, c+1]
        if self.newSnake.head_direction == self.newSnake.LEFT:
            if c == 0:
                c = 20
            return [r, c-1]

    def move_snake(self):
        if not self.lose_flag:
            self.snake_bites_food()
            self.newSnake.body.insert(0, Cube(self.next_position_of_head()))
            if not self.snake_should_expand():
                self.newSnake.body.pop()

    # TODO                                                                                                      DRAWING
    def draw_score(self):
        score_text = "Score: " + str(len(self.newSnake.body))
        text_surf = self.text_font.render(score_text, True, self.BLACK)
        text_rect = text_surf.get_rect()
        self.screen.blit(text_surf, text_rect)

    def draw_food(self):
        r, c = self.newFood.position[0], self.newFood.position[1]
        w = self.ceil_size//2
        pygame.draw.rect(self.screen, self.RED,
                         (c*self.ceil_size+w//2+1, r*self.ceil_size+w//2+1, w, w))

    def draw_snake(self):
        for part_of_snake_body in self.newSnake.body:
            r, c = part_of_snake_body.position[0], part_of_snake_body.position[1]
            if self.newSnake.body.index(part_of_snake_body) == 0:
                pygame.draw.rect(self.screen, self.DARK_GREEN,
                                 (c*self.ceil_size, r*self.ceil_size, self.ceil_size, self.ceil_size))
            else:
                pygame.draw.rect(self.screen, self.GREEN,
                                 (c * self.ceil_size, r * self.ceil_size, self.ceil_size, self.ceil_size))

    def draw_grid(self):
        for i in range(self.ROW_NUM):
            pygame.draw.line(self.screen, self.BLACK, (0, i*self.ceil_size), (self.WIDTH, i*self.ceil_size))
            pygame.draw.line(self.screen, self.BLACK, (i*self.ceil_size, 0), (i*self.ceil_size, self.HEIGHT))

    def redraw_screen(self):
        self.screen.fill(self.WHITE)
        self.draw_food()
        self.draw_snake()
        self.draw_grid()
        self.draw_score()
        pygame.display.update()


def main_loop():
    newGame = Game()
    while newGame.run:
        pygame.time.delay(80)
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not newGame.newSnake.head_direction == newGame.newSnake.DOWN:
                    newGame.newSnake.head_direction = newGame.newSnake.UP
                elif event.key == pygame.K_DOWN and not newGame.newSnake.head_direction == newGame.newSnake.UP:
                    newGame.newSnake.head_direction = newGame.newSnake.DOWN
                elif event.key == pygame.K_RIGHT and not newGame.newSnake.head_direction == newGame.newSnake.LEFT:
                    newGame.newSnake.head_direction = newGame.newSnake.RIGHT
                elif event.key == pygame.K_LEFT and not newGame.newSnake.head_direction == newGame.newSnake.RIGHT:
                    newGame.newSnake.head_direction = newGame.newSnake.LEFT

        newGame.check_lose()
        newGame.move_snake()
        newGame.redraw_screen()


if __name__ == '__main__':
    main_loop()