import agent as agent_lib
import node as node_lib
import init
from init import pygame

# Show the game over screen to notify players
def draw_game_over_message(window,text1,text2):
    pygame.draw.rect(window, init.RED, init.Error_area, 0, 40)
    font1 = pygame.font.Font('dlxfont.ttf', 42)
    text = font1.render(text1, True, init.YELLOW)
    text_rect = text.get_rect(center=(init.WIDTH // 2 - 5, init.HEIGHT // 2))
    font2 = pygame.font.Font('dlxfont.ttf', 32)
    text_level = font2.render(text2, True, init.YELLOW)
    text_level_rect = text_level.get_rect(center=(init.WIDTH // 2, init.HEIGHT // 2+54))
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
                
#draw each node of grid
def make_grid_color(size, width, height, grid):
    grid_color = []
    for i in range(size):
        grid_color.append([])
        for j in range(size):
            node = node_lib.Node(i, j, width // size, height // size,size)

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
    
    grid_color = agent_lib.generate_factor_inputfile(grid_color,size)
                
    return grid_color 

def draw_grid_line(window, size, width, height):
    gap1 = height // size
    gap2 = width // size
        
    for i in range(size):
        pygame.draw.line(window, init.BLACK, (0, i * gap1 + 100), (width, i * gap1 +100))
        for j in range(size):
            pygame.draw.line(window, init.BLACK, (j * gap2, 100), (j * gap2, height+100))

def draw_update(window, grid, size, width, height):   
    for i in grid:
        for node in i:
            node.draw(window)
            
    draw_grid_line(window, size, width, height)
    pygame.display.update()