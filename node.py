import action as WA
import init
from init import pygame

class Node:
    def __init__(self, irow, jcol, width, height, size) -> None:
        self.color = init.WHITE
        self.neighbor=[]
        self.x = irow
        self.y = jcol
        self.width = width
        self.height = height
        self.visited =[]
        self.size = size
        self.text = ""
        self.visit_count = 0
        self.left = ""
        self.right = ""
        self.up = ""
        self.down = ""
        
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
            text_surface = init.tile_font.render(self.text, True, init.BLACK)
            text_rect = text_surface.get_rect(center=((self.y * self.width) + self.width // 2, (self.x * self.height + 100) + self.height // 2))
            window.blit(text_surface, text_rect)
        if(self.check_agent == True):
            
            if(self.direction ==WA.Action.LEFT):
                image = pygame.image.load('./assets/agent_left.png')
                
            if(self.direction ==WA.Action.UP):
                image = pygame.image.load('./assets/agent_up.png')
                
            if(self.direction ==WA.Action.RIGHT):
                image = pygame.image.load('./assets/agent_right.png')
        
            if(self.direction ==WA.Action.DOWN):
                image = pygame.image.load('./assets/agent_down.png')
            image = pygame.transform.scale(image, (self.width, self.height))
            window.blit(image,(self.y * self.width, self.x * self.height + 100, self.width, self.height+100)) 
            if (self.check_gold == False and self.check_wumpus == False and self.check_pit == False):  
                text_surface = init.tile_font.render(self.text, True, init.BLACK)
                text_rect = text_surface.get_rect(center=((self.y * self.width) + self.width // 2, (self.x * self.height + 100) + self.height // 2))
                window.blit(text_surface, text_rect)
            #pygame.draw.rect(window, RED, (self.y * self.width, self.x * self.height + 100, self.width, self.height + 100))
        if(self.check_open == False):
            pygame.draw.rect(window, init.GREY, (self.y * self.width, self.x * self.height + 100, self.width, self.height + 100))
            
       
    def set_text(self,text):
        self.text = text

    # set object: breeze, stench, pit, wumpus, gold, agent
    def set_pit_color(self):
        self.color = init.BLACK
    
    def set_wumpus_color(self):
        self.color = init.PINK
    
    def set_gold(self):
        self.color = init.YELLOW
    
    def set_stench_color(self):
        self.color = init.IRISBLUE
        
    def set_breeze_color(self):
        self.color = init.IRISBLUE
    
    def set_exist_color(self):
        self.color = init.BLUE
        
    def set_start_color(self):
        self.color = init.RED
    
    def set_nodeOpen_color(self):
        self.color = init.VSBLUE 
        
    def set_nodeVisited_color(self):
        self.color = init.YELLOW
        
    def set_path_color(self):
        self.color = init.RED
    
    def set_unvisible(self):
        self.color = init.GREY
        
    def is_gold(self):
        return self.color == init.YELLOW
    
    def is_exist(self):
        return self.color == init.BLUE
    
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