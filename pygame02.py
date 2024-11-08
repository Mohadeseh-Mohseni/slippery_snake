import sys
import math
import pygame
import random
from sys import exit

   
# backtracking section

def is_safe(pose, body,path):
    if pose[0] <= -40 or pose[0] >= 800 or pose[1] <=-40  or pose[1] >= 600:
        return False
    if pose in body or pose in path:
        return False
    return True

def choose_dir(fruit_pose, head_pose):
    if fruit_pose[0] < head_pose[0] and fruit_pose[1] <= head_pose[1]:
        directions=[(-40, 0),(0,-40),(40, 0),(0,40)]
    elif fruit_pose[0] < head_pose[0] and fruit_pose[1] >= head_pose[1]:
        directions=[(-40, 0),(0,40),(40, 0),(0,-40)]
    elif fruit_pose[0] > head_pose[0] and fruit_pose[1] >= head_pose[1]:
        directions=[(40, 0),(0,40),(-40, 0),(0,-40)]
    elif fruit_pose[0] == head_pose[0] and fruit_pose[1] > head_pose[1]:
        directions=[(0,40),(0,40),(-40, 0),(0,-40)]
    elif fruit_pose[0] == head_pose[0] and fruit_pose[1] < head_pose[1]:
        directions=[(0,-40),(0,40),(-40, 0),(0,40)]
    else:
        directions=[(40, 0),(0,-40),(-40, 0),(0,40)]
    return directions

def shortest_path_util(head_pose,body,fruit_pose, path, cnt):
    if head_pose==fruit_pose:
        return True
    directions= choose_dir(fruit_pose, head_pose)
    for dir in directions:
        new_pose=(head_pose[0]+dir[0],head_pose[1]+dir[1])
        new_body=[new_pose]+body[:-1]
        tail=body[-1]
        if is_safe(new_pose,new_body[1:],path):
            cnt+=1
            path.append(new_pose)
            body=new_body
            head_pose=new_pose
            if shortest_path_util(head_pose,body,fruit_pose, path, cnt):
                return path
            cnt-=1
            path=path[:-1]
            body=body[1:]+[tail]

def shortest_path(head_pose, body, fruit_pose):
    cnt=0
    path=[]
    best_cnt= math.inf
    best_path=[]
    if shortest_path_util(head_pose, body, fruit_pose, path, cnt):
        if cnt< best_cnt:
            best_cnt= cnt
            best_path= path

    return best_path

def show_path(path):
    i=0
    color=(200,125,i)
    for i,sq in enumerate(path):
        i=int(i*3)
        color=(i,0,150)
        tile= pygame.Surface((40,40))
        tile.fill(color)
        tile.set_alpha(65)
        screen.blit(tile, sq)



class Fruit:
    def __init__(self):
        self.x = random.randint(0, 19) * 40 # go forward by steps size = 40
        self.y = random.randint(0, 14) * 40
        self.pos = pygame.math.Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit = pygame.image.load('C:\\Users\\Administrator\\Downloads\\2.png').convert_alpha()													
        fruit = pygame.transform.scale(fruit, (40, 40))
        fruit_rect = fruit.get_rect(topleft = self.pos)
        screen.blit(fruit, fruit_rect)

class Snake:
    def __init__(self):
        self.body = [pygame.math.Vector2(5, 13) * 40, pygame.math.Vector2(6, 13) * 40, pygame.math.Vector2(7, 13) * 40]
        self.direction = pygame.math.Vector2(-40, 0)
        self.color = (0, 153, 255)
        self.new_block = False

    def draw_snake(self):
        for i,block in enumerate(self.body):
            if i==0:
                head=pygame.image.load("C:\\Users\\Administrator\\Downloads\\open_mouth.png")
                head=pygame.transform.scale(head, (38, 38))
                head= pygame.transform.flip(head, True, False)											# remember to delete
                directions={(-40, 0):(0,0),(40, 0):(1,0),(0,-40):(0,0),(0, 40):(0,0)}
                head = pygame.transform.flip(head, directions[tuple(self.direction)][0], directions[tuple(self.direction)][1])
                if tuple(self.direction)==(0, 40):
                    head=pygame.transform.rotate(head,90)
                if tuple(self.direction)==(0, -40):
                    head=pygame.transform.rotate(head,-90)
                head_rect = head.get_rect(topleft = block + (1,1))
                screen.blit(head, head_rect)
            elif i==len(self.body)-1:
                tail=pygame.image.load("C:\\Users\\Administrator\\Downloads\\tail1.png")
                tail= pygame.transform.flip(tail, True, False)												# remember to delete
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
        global score
        if self.fruit.pos == self.snake.body[0]:
            score+=1
            while True:
                possible_pose = (random.randint(0, 19) * 40, random.randint(0, 14) * 40)
                if possible_pose not in self.snake.body:
                    break
            self.fruit.pos=possible_pose   
            self.snake.add_block()
            

    def check_game_over(self):
        if self.snake.body[0].x <= -40 or self.snake.body[0].x >= 800 or self.snake.body[0].y <= -40 or self.snake.body[0].y >= 600:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
                
    def game_over(self):
        global game_state
        game_state= 'game over'
        




main_game = MAIN()
pygame.init()
screen = pygame.display.set_mode((800, 600))

def grid():
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
    restart_rect= start_text.get_rect(midtop=(400, 100))
    pygame.draw.rect(screen, 'darkkhaki', restart_rect)
    screen.blit(start_text, restart_rect)

    #drawing the exit button
    exit_text= font_1.render('Exit', False, 'Black')
    exit_rect= exit_text.get_rect(midtop=(400, 400))
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
            screen.fill('cadetblue2')
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
            grid()
            main_game.draw_elements()
            if main_game.snake.body:
                body=[tuple(i) for i in main_game.snake.body]
                sh_path=shortest_path(body[0],body,tuple(main_game.fruit.pos))
                show_path(sh_path)
            if sh_path and event.type!= pygame.KEYDOWN:
                tile=sh_path[0]
                head_x, head_y= body[0][0], body[0][1]
                main_game.snake.direction= (tile[0]-head_x, tile[1]- head_y)

        elif game_state == 'game over':
            main_menu_rect= game_over_page()
            if event.type == pygame.MOUSEBUTTONDOWN and main_menu_rect.collidepoint(pygame.mouse.get_pos()):
                game_state = 'main menu'

        elif game_state == 'pause':
            pass

    clock.tick(60)
    pygame.display.update()
