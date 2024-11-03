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
        self.color = (0, 153, 255)
        self.new_block = False

    def draw_snake(self):
        for i,block in enumerate(self.body):
            if i==0:
                head=pygame.image.load("open_mouth.png")
                head=pygame.transform.scale(head, (40, 40))
                directions={(-40, 0):(0,0),(40, 0):(1,0),(0,-40):(0,0),(0, 40):(0,0)}
                head = pygame.transform.flip(head, directions[tuple(self.direction)][0], directions[tuple(self.direction)][1])
                if tuple(self.direction)==(0, 40):
                    head=pygame.transform.rotate(head,90)
                if tuple(self.direction)==(0, -40):
                    head=pygame.transform.rotate(head,-90)
                head_rect = head.get_rect(topleft = block)
                screen.blit(head, head_rect)
            elif i==len(self.body)-1:
                tail=pygame.image.load("tail1.png")
                tail=pygame.transform.scale(tail, (40, 40))
                tail_rect=tail.get_rect(topleft = block)
                last_block=tuple(self.body[i-1])
                dx=last_block[0]-block[0]
                dy=last_block[1]-block[1]
                if dx:
                    if dx>0:
                       tail = pygame.transform.flip(tail,1,0)
                else:
                    if dy>0:
                        tail=pygame.transform.rotate(tail,90) 
                    else:
                        tail=pygame.transform.rotate(tail,-90)
                screen.blit(tail, tail_rect)
            else:    
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
            while True:
                possible_pose = (random.randint(0, 19) * 40, random.randint(0, 14) * 40)
                if possible_pose not in self.snake.body:
                    break
            self.fruit.pos=possible_pose   
            self.snake.add_block()

    def check_game_over(self):
        if self.snake.body[0].x <= 0 or self.snake.body[0].x >= 800 or self.snake.body[0].y <=0 or self.snake.body[0].y >= 600:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        #screen = pygame.display.set_mode((800, 600))
        screen.blit(MAIN.backg_surface,(0,0))
        screen.blit(MAIN.starting_surf,MAIN.starting_rect)
        pygame.quit()
        sys.exit()


main_game = MAIN()
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('EX 01')
clock = pygame.time.Clock()
screen_input = pygame.USEREVENT
pygame.time.set_timer(screen_input, 200)

starting_surf=pygame.image.load("D:\دروس دانشگاه\ترم ۱  ۱۴۰۳\AP\snake_images\cute_snake.jpg")
starting_rect=starting_surf.get_rect(topleft=(70,20))
backg_surface=pygame.Surface((700,600))
backg_surface.fill("antiquewhite")

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
    screen.fill("antiquewhite")
    main_game.draw_elements()
    clock.tick(60)
    pygame.display.update()
