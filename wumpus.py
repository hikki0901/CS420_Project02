from queue import PriorityQueue
import random
import matplotlib.pyplot as plt
import pygame
from enum import Enum



class Action(Enum):
    LEFT = 1
    UP = 2
    DOWN = 3
    RIGHT = 4
    SHOOT = 5

pygame.init()

WIDTH = 500
HEIGHT= 600

ROW = 10
COL = 10

RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (15, 10, 222)
GREY = (128, 128, 128)
VSBLUE = (192,250,244)
IRISBLUE = (0, 181, 204)
PINK = (255, 105, 180)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move your step")
font = pygame.font.Font('dlxfont.ttf', 18)
tile_font = pygame.font.Font('dlxfont.ttf', 12)
Error_area = pygame.Rect(WIDTH // 4-50, HEIGHT//2 -35, 350, 120)
game_area = pygame.Rect(0,100,WIDTH,HEIGHT-100) 
header_area = pygame.Rect(0,0,WIDTH,100)
class Button:
    def __init__(self, x, y, text, click):
        self.x = x
        self.y = y
        self.text = text
        self.click = click
        self.draw()
        
    def draw(self):
        text_button = font.render(self.text, True, BLACK)
        button = pygame.rect.Rect((self.x, self.y), (160, 50))
        if self.click:
            pygame.draw.rect(WINDOW, GREEN, button, 0,5)
        else:
            pygame.draw.rect(WINDOW, IRISBLUE, button, 0,5)
        WINDOW.blit(text_button,(self.x +20, self.y + 15))
    
    def is_click(self) -> bool:
        mouse = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button = pygame.rect.Rect(self.x, self.y, 120, 50)
        if(left_click and button.collidepoint(mouse)):
            return True
        else:
            return False
        
    def set_click(self):
        self.click = True
        
    def remove_click(self):
        self.click = False
        
    def return_click(self) -> bool:
        return self.click

class Node:
    def __init__(self, irow, jcol, width, height, size) -> None:
        self.color = WHITE
        self.neighbor=[]
        self.x = irow
        self.y = jcol
        self.width = width
        self.height = height
        self.visited =[]
        self.size = size
        self.text = ""
        self.visit_count = 0
        
        # feature of node: stench,breeze, pit, wumpus
        self.check_pit = False
        self.check_breeze = False
        self.check_stench = False
        self.check_wumpus = False
        self.check_gold = False
        self.check_exist = False
        self.check_agent = False
        self.image = ''
        
        #direction of agent
        self.direction = 0
           
        #check open node or not
        self.check_open = False
    
    def set_image(self):
        if(self.check_pit):
            self.image = pygame.image.load('./assets/pit.png')
        elif(self.check_wumpus):
            self.image = pygame.image.load('./assets/wumpus.png')
        elif(self.check_gold):
            self.image = pygame.image.load('./assets/gold.png')
        else:
            self.image = pygame.image.load('./assets/terrain.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
    def increment_visit_count(self):
        self.visit_count +=1
    
    def set_heatmap_color(self):
        intensity = min(192, int(self.visit_count * 36))
        self.color = (192-intensity,250-intensity,244-intensity)
    
    def get_pos(self):
        return self.x, self.y
        
    def draw(self, window):
        self.set_image()
        if(self.check_open):
            window.blit(self.image,(self.y * self.width, self.x * self.height + 100, self.width, self.height+100))
            text_surface = tile_font.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=((self.y * self.width) + self.width // 2, (self.x * self.height + 100) + self.height // 2))
            window.blit(text_surface, text_rect)
        if(self.check_agent == True):
            
            if(self.direction ==Action.LEFT):
                image = pygame.image.load('./assets/agent_left.png')
                
            if(self.direction ==Action.UP):
                image = pygame.image.load('./assets/agent_up.png')
                
            if(self.direction ==Action.RIGHT):
                image = pygame.image.load('./assets/agent_right.png')
        
            if(self.direction ==Action.DOWN):
                image = pygame.image.load('./assets/agent_down.png')
            image = pygame.transform.scale(image, (self.width, self.height))
            window.blit(image,(self.y * self.width, self.x * self.height + 100, self.width, self.height+100)) 
            if (self.check_gold == False and self.check_wumpus == False and self.check_pit == False):  
                text_surface = tile_font.render(self.text, True, BLACK)
                text_rect = text_surface.get_rect(center=((self.y * self.width) + self.width // 2, (self.x * self.height + 100) + self.height // 2))
                window.blit(text_surface, text_rect)
            #pygame.draw.rect(window, RED, (self.y * self.width, self.x * self.height + 100, self.width, self.height + 100))
        if(self.check_open == False):
            pygame.draw.rect(window, GREY, (self.y * self.width, self.x * self.height + 100, self.width, self.height + 100))
            
       
    def set_text(self,text):
        self.text = text

    # set object: breeze, stench, pit, wumpus, gold, agent
    def set_pit_color(self):
        self.color = BLACK
    
    def set_wumpus_color(self):
        self.color = PINK
    
    def set_gold(self):
        self.color = YELLOW
    
    def set_stench_color(self):
        self.color = IRISBLUE
        
    def set_breeze_color(self):
        self.color = IRISBLUE
    
    def set_exist_color(self):
        self.color = BLUE
        
    def set_start_color(self):
        self.color = RED
    
    def set_nodeOpen_color(self):
        self.color = VSBLUE 
        
    def set_nodeVisited_color(self):
        self.color = YELLOW
        
    def set_path_color(self):
        self.color = RED
    
    def set_unvisible(self):
        self.color = GREY
        
    def is_gold(self):
        return self.color == YELLOW
    
    def is_exist(self):
        return self.color == BLUE
    
    def is_breeze(self):
        return self.check_breeze
    
    def is_wumpus(self):
        return self.check_wumpus
    
    def is_stench(self):
        return self.check_stench
    
    def is_gold(self):
        return self.check_gold

    def __lt__(self, other):
        return False



class agent():
    def __init__(self,x,y,size) -> None:
        self.current_direction = Action.RIGHT
        self.is_alive = True
        self.x_coord = x
        self.y_coord = y
        self.size = size
        self.check_win = False
        self.points = 0
        
    def move_agent(self, key,grid,window):
        current_x = self.x_coord
        current_y = self.y_coord
        if key == "w":
            if(self.current_direction == Action.UP):
                if(0 < self.x_coord):
                    self.x_coord -= 1
                    self.points -= 10
            self.current_direction = Action.UP
        
        if key == "s":
            if(self.current_direction == Action.DOWN):
                if(self.x_coord < self.size - 1):
                    self.x_coord +=1
                    self.points -= 10
            self.current_direction = Action.DOWN
        
        if key == "a":
            if(self.current_direction == Action.LEFT):
                if(0 < self.y_coord):
                    self.y_coord -=1
                    self.points -=10
            self.current_direction = Action.LEFT
        
        if key == "d":
            if(self.current_direction == Action.RIGHT):
                if( self.y_coord < self.size -1):
                    self.y_coord +=1
                    self.points -= 10
            self.current_direction = Action.RIGHT
        
        if key == "space":
            self.points -= 100
            action_coord= [(0,0),(0,-1), (-1,0),(1,0),(0,1)]
            temp_x = self.x_coord + action_coord[self.current_direction.value][0]
            temp_y = self.y_coord + action_coord[self.current_direction.value][1]
            if( 0 <= temp_x < self.size and 0 <= temp_y < self.size):
                if(grid[temp_x][temp_y].check_wumpus == True):
                    grid[temp_x][temp_y].check_wumpus = False
                    grid[temp_x][temp_y].text = ""
                    grid[temp_x][temp_y].image = pygame.image.load('./assets/terrain.png')
                    for d in action_coord:
                        x_hint = temp_x + d[0]
                        y_hint = temp_y + d[1]
                        if( 0 <= x_hint < self.size and 0 <= y_hint < self.size):
                            grid[x_hint][y_hint].check_stench = False
                            if(grid[x_hint][y_hint].text == "B,S"):
                                grid[x_hint][y_hint].text = "B"
                            else:
                                grid[x_hint][y_hint].text = ""
                    
                    grid = generate_factor_inputfile(grid,self.size)       
                    
        print(self.x_coord,self.y_coord)       
        
        self.update_previous_node(grid,current_x,current_y,window) 
        self.draw_agent(grid,window)   

    # # reload map after kill wumpus
    # def reload_map(self,grid):
    #     for i in range(self.size):
    #         for j in range(self.size):
    #             if(grid[i][j].check_wumpus == True):
    #                 dir = [(-1,0),(0,-1),(1,0),(0,1)]
    #                 for d in dir:
    #                     x_stench = i + d[0]
    #                     y_stench = j + d[1]
    #                     if (0<= x_stench <self.size and 0<= y_stench < self.size):
    #                         grid[x_stench][y_stench].check_stench = True 
       
    def update_previous_node(self,grid,x,y,window):
        grid[x][y].check_agent=False
        grid[x][y].direction = 0
        grid[x][y].draw(window)
    
    def is_death(self):
        return self.is_alive == False
    
    def draw_agent(self,grid,window):
        self.draw_points()
        grid[self.x_coord][self.y_coord].check_agent = True
        grid[self.x_coord][self.y_coord].check_open =True
        if(grid[self.x_coord][self.y_coord].check_wumpus == True
           or grid[self.x_coord][self.y_coord].check_pit == True):
            self.points -=10000 # death
            self.is_alive = False
        if(grid[self.x_coord][self.y_coord].check_exist == True):
            self.check_win = True
        if(grid[self.x_coord][self.y_coord].check_gold == True):
            self.points += 1000 # gain gold
            grid[self.x_coord][self.y_coord].check_gold = False
        self.draw_points()
        
        
        ## draw map
        grid[self.x_coord][self.y_coord].direction = self.current_direction
        grid[self.x_coord][self.y_coord].draw(window)
    
    def draw_points(self):
        font_top = pygame.font.Font('dlxfont.ttf', 14)
        points_surface = font_top.render("Points: " + str(self.points), True, PINK)
        points_rect = points_surface.get_rect()
        points_rect.center = 400, 100//2
        
        WINDOW.fill(WHITE, points_rect)
        
        # Blit the text surface onto the screen
        WINDOW.blit(points_surface, points_rect)

        # Update the display only in the region where the points are
        pygame.display.flip()
        

# Show the game over screen to notify players
def draw_game_over_message(window,text1,text2):
    pygame.draw.rect(window,RED, Error_area,0,40)
    font1 = pygame.font.Font('dlxfont.ttf', 42)
    text = font1.render(text1, True, YELLOW)
    text_rect = text.get_rect(center=(WIDTH // 2 - 5, HEIGHT // 2))
    font2 = pygame.font.Font('dlxfont.ttf', 32)
    text_level = font2.render(text2, True, YELLOW)
    text_level_rect = text_level.get_rect(center=(WIDTH // 2, HEIGHT // 2+54))
    window.blit(text, text_rect)
    window.blit(text_level, text_level_rect)
    
    pygame.display.flip()
    

#read data from file
def read_grid_from_file(file_path):
    grid = []
    with open(file_path,'r') as file:  
        size = int(file.readline().strip())
        for i in range(size):
            data = file.readline().strip().split('.')
            grid.append(data)
            
    return grid,size

# random the position of agent
def random_agent(size,grid_color):
    while True:
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        if(grid_color[x][y].check_pit == False and grid_color[x][y].check_breeze == False and
           grid_color[x][y].check_wumpus == False and grid_color[x][y].check_gold == False and
           grid_color[x][y].check_exist == False):
            grid_color[x][y].check_open = True
            manual_agent = agent(x,y,size)
            return manual_agent,x,y

# When game over, players play the current map and agent (old map)
def previous_agent(size,grid_color,x,y):
    if(grid_color[x][y].check_pit == False and grid_color[x][y].check_breeze == False and
           grid_color[x][y].check_wumpus == False and grid_color[x][y].check_gold == False and
           grid_color[x][y].check_exist == False):
            grid_color[x][y].check_open = True
            manual_agent = agent(x,y,size)
            return manual_agent
         
# generate stench, breeze
def generate_factor_inputfile(grid_color, size):
    dir =[(1,0),(-1,0),(0,1),(0,-1)]
    for i in range(size):
        for j in range(size):
            if(grid_color[i][j].check_pit == True):
                for direct in dir:
                    x = i + direct[0]
                    y = j + direct[1]
                    
                    if(0 <= x < size and 0 <= y < size):
                        if(grid_color[x][y].is_stench()):
                            grid_color[x][y].set_text("B,S")
                        else:
                            grid_color[x][y].set_text("B")
                            
                        grid_color[x][y].check_breeze = True

            if(grid_color[i][j].check_wumpus == True):
                for direct in dir:
                    x = i + direct[0]
                    y = j + direct[1]
                    
                    if(0 <= x < size and 0 <= y < size):
                        if(grid_color[x][y].is_breeze()):
                            grid_color[x][y].set_text("B,S")
                        else:
                            grid_color[x][y].set_text("S")
                        
                        grid_color[x][y].check_stench = True
    grid_color[size-1][0].check_exist = True
    return grid_color
                
#draw each node of grid
def make_grid_color(size, width, height, grid):
    grid_color = []
    for i in range(size):
        grid_color.append([])
        for j in range(size):
            node = Node(i, j, width // size, height // size,size)

            if(grid[i][j] == "P"):
                node.set_pit_color()
                node.set_text(str(grid[i][j]))
                node.check_pit = True

            if(grid[i][j] == "W"):
                node.set_wumpus_color()
                node.set_text(str(grid[i][j]))
                node.check_wumpus = True

            if(grid[i][j] == "G"):
                node.set_gold()
                node.check_gold = True

            grid_color[i].append(node)
    
    grid_color = generate_factor_inputfile(grid_color,size)
                
    return grid_color 

def draw_grid_line(window, size, width, height):
    gap1 = height // size
    gap2 = width // size
        
    for i in range(size):
        pygame.draw.line(window, BLACK, (0, i * gap1 + 100), (width, i * gap1 +100))
        for j in range(size):
            pygame.draw.line(window, BLACK, (j * gap2, 100), (j * gap2, height+100))

def draw_update(window, grid, size, width, height):   
    for i in grid:
        for node in i:
            node.draw(window)
            
    draw_grid_line(window, size, width, height)
    pygame.display.update()
                    
def main(window, width, height):
    file = 'input.txt'
    temp_grid,size = read_grid_from_file(file)
    grid = make_grid_color(size,width,height,temp_grid)
    agent,x_agent,y_agent = random_agent(size,grid)
    click4 = False
    one_press = True
    
    move_left = False
    move_up = False
    move_down = False
    move_right = False
    kill_press =False

    new_game = False
    run = True
    window.fill(WHITE)
    agent.draw_agent(grid,window)
    while run:
        pygame.draw.rect(window, WHITE, game_area)
        # move to the exist room
        if(agent.check_win):
            draw_update(window,grid,size,width,height) 
            draw_game_over_message(window,"WINNER","GOOD JOB!")
            pygame.time.delay(500)
            new_game = True

        # kill by pit or wumpus
        if(agent.is_alive == False):
            draw_update(window,grid,size,width,height) 
            draw_game_over_message(window,"CHICKEN","GAME OVER")
            pygame.time.delay(500)
            new_game = True
            
        
        if(new_game == True):
            pygame.draw.rect(window, WHITE, header_area)
            grid= make_grid_color(size, width, height, temp_grid)
            
            if(agent.check_win):
                agent,x_agent,y_agent = random_agent(size,grid)
            else:
                agent = previous_agent(size,grid,x_agent,y_agent)
            
            agent.draw_agent(grid,window)
            new_game = False

        restart = Button(30, 25, "Restart", click4)
        draw_update(window,grid,size,width,height)     
        
        if(pygame.mouse.get_pressed()[0]) and one_press:
            one_press = False           
                
            if(restart.is_click()):
                pygame.draw.rect(window, WHITE, header_area)
                click4 = True
                
                grid= make_grid_color(size, width, height, temp_grid)
                agent,x_agent,y_agent = random_agent(size,grid)
                agent.draw_agent(grid,window)
                       
        keys = pygame.key.get_pressed()
        pygame.key.set_repeat(0)
        
        # Check for key presses and play game manual
        if keys[pygame.K_a] and not move_left:
            move_left = True
            agent.move_agent('a', grid,window)
        elif not keys[pygame.K_a]:
            move_left = False

        if keys[pygame.K_w] and not move_up:
            move_up = True
            agent.move_agent('w', grid,window)
        elif not keys[pygame.K_w]:
            move_up = False

        if keys[pygame.K_s] and not move_down:
            move_down = True
            agent.move_agent('s', grid,window)
        elif not keys[pygame.K_s]:
            move_down = False

        if keys[pygame.K_d] and not move_right:
            move_right = True
            agent.move_agent('d', grid,window)
        elif not keys[pygame.K_d]:
            move_right = False
        
        if keys[pygame.K_SPACE] and not kill_press:
            kill_press = True
            agent.move_agent('space', grid,window)
        elif not keys[pygame.K_SPACE]:
            kill_press = False
        
        
        if(not pygame.mouse.get_pressed()[0]) and not one_press:
            one_press = True
            click4 = False
            restart.remove_click()
            restart.draw()
             
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
    pygame.quit()
    
if __name__ == "__main__":
    main(WINDOW, WIDTH,HEIGHT-100)