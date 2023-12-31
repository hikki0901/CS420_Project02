import action as act
import init
from init import pygame, random
from kb import knownNode

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
        self.x_og = x
        self.y_og = y
        self.x_coord = x
        self.y_coord = y
        self.size = size
        self.check_win = False
        self.points = 0
        self.neighbor = []
        self.neighbor_action = []
        self.knowledge_base = []
        self.x_kb = 0
        self.y_kb = 0
        self.has_move = True
        self.has_shoot = False
        self.killing_wumpus = False
        self.percept = []
        self.count = 0

    def get_neighbors(self, grid):
        self.neighbor = []
        tmpMove = []
       
        if grid[self.x_coord][self.y_coord].left != "wall":
            node = knownNode(0,0,0,0,0,0)
            self.neighbor.append(node)
            tmpMove.append([0,-1])
        if grid[self.x_coord][self.y_coord].right != "wall":
            node = knownNode(0,0,0,0,0,0)
            self.neighbor.append(node)
            tmpMove.append([0, 1])
        if grid[self.x_coord][self.y_coord].down != "wall":
            node = knownNode(0,0,0,0,0,0)
            self.neighbor.append(node)
            tmpMove.append([1, 0])
        if grid[self.x_coord][self.y_coord].up != "wall":
            node = knownNode(0,0,0,0,0,0)
            self.neighbor.append(node)
            tmpMove.append([-1, 0])
        
    
        for i in range(len(self.neighbor)):
            self.neighbor[i].x = self.x_kb + tmpMove[i][0]
            self.neighbor[i].y = self.y_kb + tmpMove[i][1]
            for node in self.knowledge_base:
                if node.x == self.neighbor[i].x and node.y == self.neighbor[i].y:
                    self.neighbor[i].isPit = node.isPit
                    self.neighbor[i].isWumpus = node.isWumpus
                    self.neighbor[i].isBreeze = node.isBreeze
                    self.neighbor[i].isStench = node.isStench
                    self.neighbor[i].x_knowledge = node.x_knowledge
                    self.neighbor[i].y_knowledge = node.y_knowledge

    def add_or_modify_node (self, x, y, isPit, isWumpus, isBreeze, isStench, x_knowledge, y_knowledge):
        for node in self.knowledge_base:
            if node.x == x and node.y == y:
                if node.countVisit > 0:
                    if node.isWumpus == isWumpus and node.isPit == isPit: return
                if node.x_knowledge == x_knowledge and node.y_knowledge == y_knowledge and node.isWumpus == isWumpus and node.isPit == isPit: return
                if isPit == 3:
                    node.isPit = isPit
                else:
                    if node.isPit < 2:
                        node.isPit += isPit
                if isWumpus == 3:
                    node.isWumpus = isWumpus
                else:
                    if node.isWumpus < 2:
                        node.isWumpus += isWumpus
                node.isBreeze = isBreeze
                node.isStench = isStench
                node.x_knowledge = x_knowledge
                node.y_knowledge = y_knowledge
                self.percept.append(node)
                return
        newNode = knownNode(x, y, isPit, isWumpus, x_knowledge, y_knowledge)
        self.knowledge_base.append(newNode)
        self.percept.append(newNode)
                
    def addToKB(self, curNode):
        self.percept = []
        if curNode.is_breeze() and not curNode.is_stench():
            self.add_or_modify_node(self.x_kb, self.y_kb, 3, 3, 1, 0, self.x_kb, self.y_kb)
            if curNode.left != "wall":
                self.add_or_modify_node(self.x_kb, self.y_kb - 1, 1, 3, -1, -1, self.x_kb, self.y_kb)
            if curNode.right != "wall":
                self.add_or_modify_node(self.x_kb, self.y_kb + 1, 1, 3, -1, -1, self.x_kb, self.y_kb)
            if curNode.up != "wall":
                self.add_or_modify_node(self.x_kb - 1, self.y_kb, 1, 3, -1, -1, self.x_kb, self.y_kb)
            if curNode.down != "wall":
                self.add_or_modify_node(self.x_kb + 1, self.y_kb, 1, 3, -1, -1, self.x_kb, self.y_kb)

        if curNode.is_stench() and not curNode.is_breeze():
            self.add_or_modify_node(self.x_kb, self.y_kb, 3, 3, 0, 1, self.x_kb, self.y_kb)
            if curNode.left != "wall":
                self.add_or_modify_node(self.x_kb, self.y_kb - 1, 3, 1, -1, -1, self.x_kb, self.y_kb)
            if curNode.right != "wall":
                self.add_or_modify_node(self.x_kb, self.y_kb + 1, 3, 1, -1, -1, self.x_kb, self.y_kb)
            if curNode.up != "wall":
                self.add_or_modify_node(self.x_kb - 1, self.y_kb, 3, 1, -1, -1, self.x_kb, self.y_kb)
            if curNode.down != "wall":
                self.add_or_modify_node(self.x_kb + 1, self.y_kb, 3, 1, -1, -1, self.x_kb, self.y_kb)

        if curNode.is_stench() and curNode.is_breeze():
            self.add_or_modify_node(self.x_kb, self.y_kb, 3, 3, 1, 1, self.x_kb, self.y_kb)
            if curNode.left != "wall":
                self.add_or_modify_node(self.x_kb, self.y_kb - 1, 1, 1, -1, -1, self.x_kb, self.y_kb)
            if curNode.right != "wall":
                self.add_or_modify_node(self.x_kb, self.y_kb + 1, 1, 1, -1, -1, self.x_kb, self.y_kb)
            if curNode.up != "wall":
                self.add_or_modify_node(self.x_kb - 1, self.y_kb, 1, 1, -1, -1, self.x_kb, self.y_kb)
            if curNode.down != "wall":
                self.add_or_modify_node(self.x_kb + 1, self.y_kb, 1, 1, -1, -1, self.x_kb, self.y_kb)
        
        if not curNode.is_stench() and not curNode.is_breeze():
            self.add_or_modify_node(self.x_kb, self.y_kb, 3, 3, 0, 0, self.x_kb, self.y_kb)
            if curNode.left != "wall":
                self.add_or_modify_node(self.x_kb, self.y_kb - 1, 3, 3, -1, -1, self.x_kb, self.y_kb)
            if curNode.right != "wall":
                self.add_or_modify_node(self.x_kb, self.y_kb + 1, 3, 3, -1, -1, self.x_kb, self.y_kb)
            if curNode.up != "wall":
                self.add_or_modify_node(self.x_kb - 1, self.y_kb, 3, 3, -1, -1, self.x_kb, self.y_kb)
            if curNode.down != "wall":
                self.add_or_modify_node(self.x_kb + 1, self.y_kb, 3, 3, -1, -1, self.x_kb, self.y_kb)

    def checkWithKB(self, grid):
        self.get_neighbors(grid)
        tmpNeighbor = []

        for neighbor in self.neighbor:
            remove_node = False

            for node in self.knowledge_base:
                if node.x == neighbor.x and node.y == neighbor.y:
                    if node.isPit == 2:
                        remove_node = True
                        break 
                    else:
                        neighbor.isWumpus = node.isWumpus
                        neighbor.isPit = node.isPit
                        neighbor.countVisit = node.countVisit

            if not remove_node:
                tmpNeighbor.append(neighbor)

        self.neighbor = tmpNeighbor

    def move_agent(self, key,grid,window):
        Message = ""
        current_x = self.x_coord
        current_y = self.y_coord
        if key == "w":
            if(self.current_direction == act.Action.UP):
                Message = "GO UP"
                if(0 < self.x_coord):
                    self.x_coord -= 1
                    self.x_kb -= 1
                    self.points -= 10
            else: Message = "LOOK UP"
            self.current_direction = act.Action.UP
        
        elif key == "s":
            if(self.current_direction == act.Action.DOWN):
                Message = "GO DOWN"
                if(self.x_coord < self.size - 1):
                    self.x_coord +=1
                    self.x_kb += 1
                    self.points -= 10
            else: Message = "LOOK DOWN"
            self.current_direction = act.Action.DOWN
        
        elif key == "a":
            if(self.current_direction == act.Action.LEFT):
                Message = "GO LEFT"
                if(0 < self.y_coord):
                    self.y_coord -=1
                    self.y_kb -= 1
                    self.points -=10
            else: Message = "LOOK LEFT"
            self.current_direction = act.Action.LEFT
        
        elif key == "d":
            if(self.current_direction == act.Action.RIGHT):
                Message = "GO RIGHT"
                if( self.y_coord < self.size -1):
                    self.y_coord +=1
                    self.y_kb += 1
                    self.points -= 10
            else: Message = "LOOK RIGHT"
            self.current_direction = act.Action.RIGHT
        else:
            Message = "SHOOT!"
            if key == "space":
                self.points -= 100
                action_coord= [(0,0), (0,-1), (-1,0), (1,0), (0,1)]
                temp_x = self.x_coord + action_coord[self.current_direction.value][0]
                temp_y = self.y_coord + action_coord[self.current_direction.value][1]
                wumpus_kb_x = self.x_kb + action_coord[self.current_direction.value][0]
                wumpus_kb_y = self.y_kb + action_coord[self.current_direction.value][1]
                if( 0 <= temp_x < self.size and 0 <= temp_y < self.size):
                    if(grid[temp_x][temp_y].check_wumpus == True):
                        Message += ": SCREAM!!!"
                        self.add_or_modify_node(wumpus_kb_x, wumpus_kb_y, 3, 3, -1, -1, self.x_kb, self.y_kb)
                        print("SCREAM!!!")
                        wumpus_death = pygame.mixer.Sound('sound/scream.wav')
                        wumpus_death.play()
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
                    
        self.update_previous_node(grid,current_x,current_y,window) 
        self.draw_agent(grid,window, Message)   
    
    def move_to (self, neighbor, grid, window):
        x, y = self.x_kb, self.y_kb
        if neighbor.x - self.x_kb == -1:
            self.move_agent("w", grid, window) 
        if neighbor.x - self.x_kb == 1:
            self.move_agent("s", grid, window)
        if neighbor.y - self.y_kb == -1:
            self.move_agent("a", grid, window)          
        if neighbor.y - self.y_kb == 1:
            self.move_agent("d", grid, window)
        if self.x_kb != x or self.y_kb != y:
            neighbor.countVisit += 1
            self.has_move = True
        else: 
            self.has_move = False
            

    def move (self, grid, window):
        if self.has_move or self.has_shoot:
            self.addToKB(grid[self.x_coord][self.y_coord]) 
            self.has_shoot = False 
            if (len(self.percept) > 0): 
                for node in self.percept:
                    if node.isPit in [2,3]:
                        print(node.print_pit_status(self.count))
                    if node.isWumpus in [2,3]:
                        print(node.print_wumpus_status(self.count))
                print("---")
                self.draw_percept()
                    
        self.checkWithKB(grid)
        if len(self.neighbor) != 0:
            for node in self.neighbor:
                if node.isWumpus == 2:
                    while not self.has_shoot:
                        self.shoot(node, grid, window)
                    self.move_to(node, grid, window)
                    return
            count = sum(1 for node in self.neighbor if node.isWumpus == 1)
            if count - len(self.neighbor) <= 1:
                filtered_neighbor = [node for node in self.neighbor if node.isPit == 3 and node.isWumpus == 1]
                if len(filtered_neighbor) > 0:
                    while not self.has_shoot:
                        self.shoot(filtered_neighbor[0], grid, window)
                    self.move_to(filtered_neighbor[0], grid, window)
                    return
            filtered_neighbor = [node for node in self.neighbor if node.isPit == 3 and node.isWumpus != 1]
            if len(filtered_neighbor) > 0:
                self.neighbor = filtered_neighbor
            leastVisited = min(self.neighbor, key=lambda x: x.countVisit)
            for node in self.knowledge_base:
                if node.x == leastVisited.x and node.y == leastVisited.y:
                    self.move_to(node, grid, window)
    '''
    def shoot(self, neighbor, grid, window):
        x, y = self.x_kb, self.y_kb
        if neighbor.x - self.x_kb == -1 and self.current_direction != act.Action.UP:
            self.move_agent("w", grid, window) 
            self.has_shoot = False
            return
        if neighbor.x - self.x_kb == 1 and self.current_direction != act.Action.DOWN:
            self.move_agent("s", grid, window)
            self.has_shoot = False
            return
        if neighbor.y - self.y_kb == -1 and self.current_direction != act.Action.LEFT:
            self.move_agent("a", grid, window)      
            self.has_shoot = False
            return    
        if neighbor.y - self.y_kb == 1 and self.current_direction != act.Action.RIGHT:
            self.move_agent("d", grid, window)
            self.has_shoot = False
            return
        else:
            self.move_agent("space", grid, window)
            self.has_shoot = True
            return
    '''
    def shoot(self, neighbor, grid, window):
        x, y = self.x_kb, self.y_kb
        if neighbor.x - self.x_kb == -1 and self.current_direction != act.Action.UP:
            self.move_agent("w", grid, window) 
        if neighbor.x - self.x_kb == 1 and self.current_direction != act.Action.DOWN:
            self.move_agent("s", grid, window)
        if neighbor.y - self.y_kb == -1 and self.current_direction != act.Action.LEFT:
            self.move_agent("a", grid, window)      
        if neighbor.y - self.y_kb == 1 and self.current_direction != act.Action.RIGHT:
            self.move_agent("d", grid, window)

        self.move_agent("space", grid, window)
        pygame.time.delay(200)
        self.has_shoot = True

    def update_previous_node(self,grid,x,y,window):
        grid[x][y].check_agent=False
        grid[x][y].direction = 0
        grid[x][y].draw(window)
    
    def is_death(self):
        return self.is_alive == False
    
    def draw_agent(self,grid,window, Message):
        if(grid[self.x_coord][self.y_coord].check_gold == True):
            Message = "GOLD FOUND!"
        self.draw_points()
        self.draw_action(Message)
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
        self.draw_action(Message)
        print(Message)
        grid[self.x_coord][self.y_coord].direction = self.current_direction
        grid[self.x_coord][self.y_coord].draw(window)
    
    def draw_points(self):
        pygame.draw.rect(init.WINDOW, init.WHITE, init.point_area)
        font_top = pygame.font.Font('dlxfont.ttf', 14)
        points_surface = font_top.render("Points: " + str(self.points), True, init.PINK)
        points_rect = points_surface.get_rect()
        points_rect.center = 400, 100//2
        
        init.WINDOW.fill(init.WHITE, points_rect)
        
        # Blit the text surface onto the screen
        init.WINDOW.blit(points_surface, points_rect)

        # Update the display only in the region where the points are
        pygame.display.update()

    def draw_action(self, Message):
        pygame.draw.rect(init.WINDOW, init.WHITE, init.action_area)
        font_top = pygame.font.Font('dlxfont.ttf', 14)
        action_surface = font_top.render(Message, True, init.BLACK)
        action_rect = action_surface.get_rect()
        action_rect.center = 650, 100//2
        
        init.WINDOW.fill(init.WHITE, action_rect)
        
        # Blit the text surface onto the screen
        init.WINDOW.blit(action_surface, action_rect)

        # Update the display only in the region where the points are
        pygame.display.update()

    def draw_percept(self):
        y_offset = 0
        font_top = pygame.font.Font('dlxfont.ttf', 12)
        for node in self.percept:
            if node.isPit in [2,3]:
                self.count += 1
                tmp = node.print_pit_status(self.count)
                action_surface = font_top.render(tmp, True, init.BLACK)
                action_rect = action_surface.get_rect()
                action_rect.topleft = 525, 200 + y_offset
                init.WINDOW.fill(init.WHITE, action_rect)
                init.WINDOW.blit(action_surface, action_rect)
                y_offset += action_rect.height + 5
            if node.isWumpus in [2,3]:
                self.count += 1
                tmp = node.print_wumpus_status(self.count)
                action_surface = font_top.render(tmp, True, init.BLACK)
                action_rect = action_surface.get_rect()
                action_rect.topleft = 525, 200 + y_offset
                init.WINDOW.fill(init.WHITE, action_rect)
                init.WINDOW.blit(action_surface, action_rect)
                y_offset += action_rect.height + 5
        pygame.draw.rect(init.WINDOW, init.WHITE, init.percept_area)
        pygame.display.update()
        pygame.time.delay(1000)
