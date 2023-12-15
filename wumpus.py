from queue import PriorityQueue
import random
import matplotlib.pyplot as plt
import pygame

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

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move your step")
font = pygame.font.Font('freesansbold.ttf', 18)
tile_font = pygame.font.Font('freesansbold.ttf', 10)
Error_area = pygame.Rect(WIDTH // 4-50, HEIGHT//2 -35, 400, 120)

class Button:
    def __init__(self, x, y, text, click):
        self.x = x
        self.y = y
        self.text = text
        self.click = click
        self.draw()
        
    def draw(self):
        text_button = font.render(self.text, True, BLACK)
        button = pygame.rect.Rect((self.x, self.y), (120, 50))
        if self.click:
            pygame.draw.rect(window, GREEN, button, 0,5)
        else:
            pygame.draw.rect(window, IRISBLUE, button, 0,5)
        window.blit(text_button,(self.x +20, self.y + 15))
    
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
        
        #check open node or not
        self.check_open = False
  
    def increment_visit_count(self):
        self.visit_count +=1
    
    def set_heatmap_color(self):
        intensity = min(192, int(self.visit_count * 36))
        self.color = (192-intensity,250-intensity,244-intensity)
    
    def get_pos(self):
        return self.x, self.y
        
    def draw(self, window):
        
        if(self.check_open):
            pygame.draw.rect(window, self.color, (self.y * self.width, self.x * self.height + 100, self.width, self.height + 100))
            text_surface = tile_font.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=((self.y * self.width) + self.width // 2, (self.x * self.height + 100) + self.height // 2))
            window.blit(text_surface, text_rect)
        else:
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


#read data from file
def read_grid_from_file(file_path):
    grid = []
    with open(file_path,'r') as file:  
        size = int(file.readline().strip())
        for i in range(size):
            data = file.readline().strip().split('.')
            grid.append(data)
            
    return grid,size

def random_agent(size,grid_color):
    while True:
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        if(grid_color[x][y].check_pit == False and grid_color[x][y].check_breeze == False and
           grid_color[x][y].check_wumpus == False and grid_color[x][y].check_gold == False and
           grid_color[x][y].check_exist == False):
            grid_color[x][y].check_open = True
            return grid_color[x][y]
            
    

# generate stench, breeze
def generate_factor_inputfile(grid_color, size):
    dir =[(1,0),(-1,0),(0,1),(0,-1)]
    for i in range(size):
        for j in range(size):
            if(grid_color[i][j].text == "P"):
                for direct in dir:
                    x = i + direct[0]
                    y = j + direct[1]
                    
                    if(0 <= x < size and 0 <= y < size):
                        if(grid_color[x][y].is_stench()):
                            grid_color[x][y].set_text("B,S")
                        else:
                            grid_color[x][y].set_text("B")
                            grid_color[x][y].set_breeze_color()
                            
                        grid_color[x][y].check_breeze = True

            if(grid_color[i][j].text == "W"):
                for direct in dir:
                    x = i + direct[0]
                    y = j + direct[1]
                    
                    if(0 <= x < size and 0 <= y < size):
                        if(grid_color[x][y].is_breeze()):
                            grid_color[x][y].set_text("B,S")
                        else:
                            grid_color[x][y].set_text("S")
                            grid_color[x][y].set_stench_color()
                        
                        grid_color[x][y].check_stench = True
    grid_color[size-1][0].check_exist == True
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
                node.set_text(str(grid[i][j]))
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
    agent = random_agent(size,grid)
    agent.set_start_color()
    click1 = False
    click4 = False
    one_press = True
    
    count = 0

    run = True
    while run:
        window.fill(WHITE)
        start_button = Button(10, 10, "Start", click1)
        restart = Button(140, 10, "restart", click4)
        draw_update(window,grid,size,width,height)     
        
        if(pygame.mouse.get_pressed()[0]) and one_press:
            one_press = False             
            if(start_button.is_click()):
                click1 = True
                click4 = False
                restart.remove_click()
                restart.draw()
                
            if(restart.is_click()):
                click4 = True
                click1 = False
                start_button.remove_click()
                start_button.draw()
                grid= make_grid_color(size, width, height, temp_grid)
            
            
        if(not pygame.mouse.get_pressed()[0]) and not one_press:
            one_press = True
             
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
    pygame.quit()
    
if __name__ == "__main__":
    main(window, WIDTH,HEIGHT-100)