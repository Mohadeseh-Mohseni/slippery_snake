import sys
import math
import pygame
import random
import numpy as np
import heapq as hq
from itertools import combinations
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('AI powered Snake Game')

# A* section
class Block:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.parent_i = -1
        self.parent_j = -1
        self.g = 0
        self.h = math.inf
        self.f = math.inf

    def calculate_h(self, fruit_pos):
        return abs(self.i- fruit_pos[0]) + abs(self.j-fruit_pos[1])
    
    def __lt__(self, next):
        if self.f == next.f:
            return self.g > next.g
        return self.f < next.f


def grid_def(body):
    board = np.zeros((15, 20))
    for block in body[1:]:
        i= int(block[1]/40)
        j= int(block[0]/40)
        board[i, j] = 1
    return board
    

def A_alg(body, fruit_pos, board):
    head= Block(int(body[0][1]/40) , int(body[0][0]/40))
    head.f= 0
    fruit_pos= (int(fruit_pos[1]/40), int(fruit_pos[0]/40))

    open_list=[]
    hq.heappush(open_list, (head.f, head))
    closed_list=[[False for i in range (20)] for j in range(15)]
    grid = [[ None for i in range (20)] for j in range(15)]
    grid[head.i][head.j]= head 

    while open_list:
        q= hq.heappop(open_list)[1]
        i, j= q.i, q.j
        closed_list[i][j] = True

        directions= [(1,0), (-1,0), (0,1), (0,-1)]
        for dir in directions:
            succ_i, succ_j = i + dir[0] , j + dir[1]

            if 0<= succ_i < 15 and 0<= succ_j <20 and not closed_list[succ_i][succ_j] and board[succ_i, succ_j] == 0:
                succ= Block(succ_i, succ_j)
                succ.parent_i, succ.parent_j = i, j
                succ.g = q.g + 1
                succ.h = succ.calculate_h(fruit_pos)
                succ.f = succ.g + succ.h

                if (succ_i, succ_j) == fruit_pos:
                    grid[succ_i][succ_j] = succ
                    return grid
                
                else:
                    if grid[succ_i][succ_j] == None or grid[succ_i][succ_j].f > succ.f:
                        hq.heappush(open_list, (succ.f, succ))
                        grid[succ_i][succ_j] = succ

    return None


class Wall():
    def __init__(self, position):
        self.pos = position
        self.image = pygame.image.load("tree.png")
        self.image = pygame.transform.scale(self.image, (40, 40))


def path(grid,fruit_pos):
    fruit_pos_x, fruit_pos_y = int(fruit_pos[1]/40), int(fruit_pos[0]/40)
    path= []
    if grid is None:
        print('no path')
        return []
    else:
        current = grid[fruit_pos_x][fruit_pos_y]
        while current.g != 0:
            new_i= current.parent_i
            new_j= current.parent_j
            path.append((new_j, new_i))
            current=grid[new_i][new_j]
        path.reverse()
        path.append((fruit_pos_y, fruit_pos_x))
        return path

def show_path(path):
    for i,sq in enumerate(path):
        color=(150,10,150)
        tile= pygame.Surface((40,40))
        tile.fill(color)
        tile.set_alpha(65)
        screen.blit(tile, (sq[0]*40,sq[1]*40))


class Fruit:
    def __init__(self, chosen_fruit, score, position):
        self.chosen = chosen_fruit
        self.score = score
        self.pos = pygame.math.Vector2(position[0], position[1])
        self.image = pygame.image.load(f'{self.chosen}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40,40))

    def draw_fruit(self):
        fruit_rect = self.image.get_rect(topleft=self.pos)
        screen.blit(self.image, fruit_rect)

class Snake:
    def __init__(self):
        self.body = [pygame.math.Vector2(5, 13) * 40, pygame.math.Vector2(6, 13) * 40, pygame.math.Vector2(7, 13) * 40]
        self.direction = pygame.math.Vector2(-40, 0)
        self.color = (0, 153, 255)
        self.new_block = False

    def draw_snake(self):
        for i,block in enumerate(self.body):
            if i==0:
                head=pygame.image.load("open_mouth.png")
                head = pygame.transform.flip(head, True, False)
                head=pygame.transform.scale(head, (38, 38))										
                directions={(-40, 0):(0,0),(40, 0):(1,0),(0,-40):(0,0),(0, 40):(0,0)}
                head = pygame.transform.flip(head, directions[tuple(self.direction)][0], directions[tuple(self.direction)][1])
                if tuple(self.direction)==(0, 40):
                    head=pygame.transform.rotate(head,90)
                if tuple(self.direction)==(0, -40):
                    head=pygame.transform.rotate(head,-90)
                head_rect = head.get_rect(topleft = block + (1,1))
                screen.blit(head, head_rect)
            elif i==len(self.body)-1:
                tail=pygame.image.load("tail1.png")
                tail = pygame.transform.flip(tail, True, False)
                tail=pygame.transform.scale(tail, (38, 38))
                tail_rect=tail.get_rect(topleft = block + (1,1))
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
                snake_block.fill("antiquewhite")
                snake_block = pygame.transform.scale(snake_block, (40, 40))
                snake_block_rect = snake_block.get_rect(topleft = block)
                screen.blit(snake_block, snake_block_rect)
                border_rect = snake_block_rect.inflate(-2, -2)  # Inflate to make the border smaller
                pygame.draw.rect(screen, self.color, border_rect)

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

    def __init__(self, fruit_scores, wall_pos):
        self.snake = Snake()
        self.fruit_scores = fruit_scores
        # self.fruit_images = {"banana": "a_banana.png", "cucumber": "cucumber.png", "apple": "2.png", "grapes": "grapes.png", "mango": "mango.png", "3banana": "3banana.png", "blueberry": "blue.png", "strawberry": "strawberry.webp"}
        self.fruits = []
        for i in range(3):
            chosen_fruit = random.choice(list(fruit_scores.keys()))
            score = fruit_scores[chosen_fruit]
            while True:
                fruit_possible_pos = (random.randint(0, 19) * 40, random.randint(0, 14) * 40)
                if fruit_possible_pos not in [tuple(block) for block in self.snake.body] and fruit_possible_pos not in wall_pos:
                    break
            self.fruits.append(Fruit(chosen_fruit, score, fruit_possible_pos))

    def update(self):
        self.snake.move_snake()
        self.collision_head()
        self.check_game_over()

    def draw_elements(self):
        self.snake.draw_snake()
        for fruit in self.fruits:
            fruit.draw_fruit()
        draw_wall()

    def collision_head(self):
        global score
        for fruit in self.fruits[:]:
            if fruit.pos == self.snake.body[0]:
                score += fruit.score
                self.fruits.remove(fruit)
                while True:
                    fruits_pos = [self.fruits[self.fruits.index(fruit)].pos for fruit in self.fruits]
                    possible_pose = (random.randint(0, 19) * 40, random.randint(0, 14) * 40)
                    if possible_pose not in self.snake.body and possible_pose not in fruits_pos:
                        break
                new_chosen_fruit = random.choice(list(self.fruit_scores.keys()))
                new_fruit = Fruit(new_chosen_fruit, self.fruit_scores[new_chosen_fruit], possible_pose)
                self.fruits.append(new_fruit)
                self.snake.add_block()
                break

    def random_fruits(self):
        chosen_fruit = random.choice(list(self.fruit_scores.keys()))
        return Fruit(chosen_fruit=random.choice(list(self.fruit_scores.keys())),
                score=self.fruit_scores[chosen_fruit],
                fruit_image=self.fruit_images[chosen_fruit])

    def check_game_over(self):
        if self.snake.body[0].x <= -40 or self.snake.body[0].x >= 800 or self.snake.body[0].y <= -40 or self.snake.body[0].y >= 600:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
                
    def game_over(self):
        global game_state
        game_state= 'game over'
        

def draw_wall():
    h_or_v = [random.randint(0, 2) for k in range(2)]
    wall_pos = []
    walls = []
    for j in range(2):
        while True:
            if h_or_v[j] == 0:
                wall_possible_pos = (random.randint(0, 17) * 40, random.randint(0, 14) * 40)
                if wall_possible_pos not in [pygame.math.Vector2(5, 13) * 40, pygame.math.Vector2(6, 13) * 40, pygame.math.Vector2(7, 13) * 40]:
                    break
                wall_pos.append(wall_possible_pos, wall_possible_pos + (1, 0), wall_possible_pos + (2, 0))
            if h_or_v[j] == 1:
                wall_possible_pos = (random.randint(0, 19) * 40, random.randint(0, 12) * 40)
                if wall_possible_pos not in [pygame.math.Vector2(5, 13) * 40, pygame.math.Vector2(6, 13) * 40, pygame.math.Vector2(7, 13) * 40]:
                    break
                wall_pos.append(wall_possible_pos, wall_possible_pos + (0, 1), wall_possible_pos + (0, 2))
    for wall in wall_pos:
        walls.append(Wall(wall))
    for wall in walls:
        wall_rect = wall.image.get_rect(topleft=wall.pos[wall_pos.index(wall)])
        screen.blit(wall.image, wall_rect)
    return wall_pos


fruit_scores = {"a_banana": 2, "cucumber": 1, "apple": 3, "grapes": 5, "mango": 7, "3 bananas": 6, "blueberry": 8,
                "strawberry": 9, "pamigrant": 10, 'watermelon': 12, 'pineapple': 15, 'fig': 4}

main_game = MAIN(fruit_scores, draw_wall())
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('AI powered Snake Game')


def game_grid():
    for i in range(40,800,40):
        pygame.draw.aaline(screen,'bisque3',(i,0),(i,600))
    for j in range(40,600,40):
        pygame.draw.aaline(screen,'bisque3',(0,j),(800,j))


pygame.display.set_caption('EX 01')
clock = pygame.time.Clock()
screen_input = pygame.USEREVENT
pygame.time.set_timer(screen_input, 200)
game_state= 'main menu'
score= 0
font_1= pygame.font.SysFont('arial', 40)
font_2= pygame.font.SysFont('arial', 70)

def game_over_page():
    # showing game over text
    game_over_text= font_2.render('Game Over', False, 'Black')
    game_over_rect= game_over_text.get_rect(midtop=(400, 150))
    screen.blit(game_over_text, game_over_rect)
    
	# drawing the main_menu button
    main_menu_text= font_1.render('Main Menu', False, 'Black')
    main_menu_rect= main_menu_text.get_rect(midtop=(400, 400))
    pygame.draw.rect(screen, 'darkkhaki', main_menu_rect)
    screen.blit(main_menu_text, main_menu_rect)

    #drwaing the score rect
    score_text= font_1.render(f'Score= {score}', False, 'Black')
    score_rect= score_text.get_rect(midtop=(400, 300))
    pygame.draw.rect(screen, 'darkkhaki', score_rect)
    screen.blit(score_text, score_rect)

    return main_menu_rect
    

def main_page():

    # drawing the restart button
    start_text= font_1.render('start', False, 'Black')
    restart_rect= start_text.get_rect(midtop=(400, 75))
    pygame.draw.rect(screen, 'darkkhaki', restart_rect)
    screen.blit(start_text, restart_rect)

    #drawing the exit button
    exit_text= font_1.render('Exit', False, 'Black')
    exit_rect= exit_text.get_rect(midtop=(400, 250))
    pygame.draw.rect(screen, 'darkkhaki', exit_rect)
    screen.blit(exit_text, exit_rect)


    return restart_rect, exit_rect

while True:
    # exit code
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_state == 'main menu':
            back_ground = pygame.image.load("Telegram Desktop/cute_snake.jpg")
            back_ground = fruit = pygame.transform.scale(back_ground, (800, 600))
            back_ground_rect=back_ground.get_rect(topleft = (0,0))
            #screen.fill('cadetblue2')
            screen.blit(back_ground,back_ground_rect)
            restart_rect, exit_rect= main_page()

            #restarting the game
            if event.type == pygame.MOUSEBUTTONDOWN and restart_rect.collidepoint(pygame.mouse.get_pos()):
                game_state = 'in game'
                main_game.snake.body = [pygame.math.Vector2(5, 13) * 40, pygame.math.Vector2(6, 13) * 40, pygame.math.Vector2(7, 13) * 40]
                main_game.snake.direction = pygame.math.Vector2(-40, 0)

            #exiting the game
            if event.type == pygame.MOUSEBUTTONDOWN and exit_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()
                exit()


        # moving snake by taking the user input
        elif game_state == 'in game':
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
            game_grid()
            main_game.draw_elements()

            #path finding
            body=[tuple(i) for i in main_game.snake.body]
            board= grid_def(body)
            all_path = [path(A_alg(body, fruit.pos, board), fruit.pos) if path(A_alg(body, fruit.pos, board), fruit.pos) else 0.000001 for fruit in main_game.fruits]
            relative_scores = [0.0000001 for i in range(len(main_game.fruits))]
            relative_scores = [main_game.fruits[i].score / len(all_path[i]) for i in range(len(main_game.fruits))]
            #best_ind = relative_scores.index(max(relative_scores))
            best_fruit = main_game.fruits[relative_scores.index(max(relative_scores))]
            grid= A_alg(body, best_fruit.pos, board)
            found_path= path(grid, best_fruit.pos)
            show_path(found_path)

            if found_path and event.type!= pygame.KEYDOWN:
                tile=found_path[1]
                head_x, head_y= body[0][0], body[0][1]
                main_game.snake.direction= (tile[0]*40 - head_x, tile[1]*40 - head_y)

        elif game_state == 'game over':
            main_menu_rect= game_over_page()
            if event.type == pygame.MOUSEBUTTONDOWN and main_menu_rect.collidepoint(pygame.mouse.get_pos()):
                game_state = 'main menu'

        elif game_state == 'pause':
            pass

    clock.tick(60)
    pygame.display.update()
