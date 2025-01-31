import sys

import pygame
import random
from sys import exit

class Fruit:
    def __init__(self):
        self.x = random.randint(0, 19) * 40 # go forward by steps size = 40
        self.y = random.randint(0, 14) * 40
        self.pos = pygame.math.Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit = pygame.image.load('2.png').convert_alpha()
        fruit = pygame.transform.scale(fruit, (40, 40))
        fruit_rect = fruit.get_rect(topleft = self.pos)
        screen.blit(fruit, fruit_rect)
class Snake:
    def __init__(self):
        self.body = [pygame.math.Vector2(5, 10) * 40, pygame.math.Vector2(6, 10) * 40, pygame.math.Vector2(7, 10) * 40]
        self.direction = pygame.math.Vector2(-40, 0)
        self.color = (185, 197, 80)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            snake_block = pygame.Surface((40,40))
            snake_block.fill(self.color)
            snake_block = pygame.transform.scale(snake_block, (40, 40))
            snake_block_rect = snake_block.get_rect(topleft = block)
            screen.blit(snake_block, snake_block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1] # we dont need the last block of snake
            body_copy.insert(0, body_copy[0] + self.direction) # moving head
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True
class MAIN:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.collision_head()
        self.check_game_over()

    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def collision_head(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.pos = (random.randint(0, 19) * 40, random.randint(0, 14) * 40)
            self.snake.add_block()

    def check_game_over(self):
        if self.snake.body[0].x < 0 or self.snake.body[0].x > 800 or self.snake.body[0].y <0 or self.snake.body[0].y > 600:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()


main_game = MAIN()
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('EX 01')
clock = pygame.time.Clock()
screen_input = pygame.USEREVENT
pygame.time.set_timer(screen_input, 500)

while True:
    # exit code
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # moving snake by taking the user input
        if event.type == screen_input:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction != (0, 40):
                main_game.snake.direction = (0, -40)
            if event.key == pygame.K_DOWN and main_game.snake.direction != (0, -40):
                main_game.snake.direction = (0, 40)
            if event.key == pygame.K_RIGHT and main_game.snake.direction != (-40, 0):
                main_game.snake.direction = (40, 0)
            if event.key == pygame.K_LEFT and main_game.snake.direction != (40, 0):
                main_game.snake.direction = (-40, 0)
    screen.fill((196, 62, 210))
    main_game.draw_elements()
    clock.tick(60)
    pygame.display.update()
