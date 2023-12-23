import action as act
import init
from init import pygame, random

def setWall(grid, size):
    for i in range(size):
        grid[0][i].up = "wall"
        grid[i][0].left = "wall"
        grid[size-1][i].down = "wall"
        grid[i][size-1].right = "wall"
        
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

class agent():
    def __init__(self,x,y,size) -> None:
        self.current_direction = act.Action.RIGHT
        self.is_alive = True
        self.x_coord = x
        self.y_coord = y
        self.size = size
        self.check_win = False
        self.points = 0
        self.neighbor = []
        self.neighbor_action = []
    
    def get_neighbors(self, grid):
        self.neighbor = []
        dir = [(0, -1), (-1, 0), (1, 0), (0, 1)]
        
        i = 0
        for dir in dir:
            nx = self.x_coord + dir[0]
            ny = self.y_coord + dir[1]
            check = True

            if grid[nx][ny] == "wall":
                check = False

            if check == True:
                if i == 0: self.neighbor_action.append(act.Action.LEFT)
                if i == 1: self.neighbor_action.append(act.Action.UP)
                if i == 2: self.neighbor_action.append(act.Action.DOWN)
                if i == 3: self.neighbor_action.append(act.Action.RIGHT)
                self.neighbor.append(grid[nx][ny])
            
            i =  i + 1


    def move_agent(self, key,grid,window):
        current_x = self.x_coord
        current_y = self.y_coord
        if key == "w":
            if(self.current_direction == act.Action.UP):
                if(0 < self.x_coord):
                    self.x_coord -= 1
                    self.points -= 10
            self.current_direction = act.Action.UP
        
        if key == "s":
            if(self.current_direction == act.Action.DOWN):
                if(self.x_coord < self.size - 1):
                    self.x_coord +=1
                    self.points -= 10
            self.current_direction = act.Action.DOWN
        
        if key == "a":
            if(self.current_direction == act.Action.LEFT):
                if(0 < self.y_coord):
                    self.y_coord -=1
                    self.points -=10
            self.current_direction = act.Action.LEFT
        
        if key == "d":
            if(self.current_direction == act.Action.RIGHT):
                if( self.y_coord < self.size -1):
                    self.y_coord +=1
                    self.points -= 10
            self.current_direction = act.Action.RIGHT
        
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
        points_surface = font_top.render("Points: " + str(self.points), True, init.PINK)
        points_rect = points_surface.get_rect()
        points_rect.center = 400, 100//2
        
        init.WINDOW.fill(init.WHITE, points_rect)
        
        # Blit the text surface onto the screen
        init.WINDOW.blit(points_surface, points_rect)

        # Update the display only in the region where the points are
        pygame.display.flip()