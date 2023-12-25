import init
from init import pygame

import action as WA

import button as btn

import node as node_lib
import agent as agent_lib

import drawer
                    
def main(window, width, height):
    file = 'input.txt'
    temp_grid,size = drawer.read_grid_from_file(file)
    grid = drawer.make_grid_color(size,width,height,temp_grid)
    agent_lib.setWall(grid, size)
    agent,x_agent,y_agent = agent_lib.random_agent(size,grid)
    click4 = False
    click3 = False
    one_press = True
    
    move_left = False
    move_up = False
    move_down = False
    move_right = False
    kill_press =False

    new_game = False
    run = True
    window.fill(init.WHITE)
    agent.draw_agent(grid,window)
    while run:
        pygame.draw.rect(window, init.WHITE, init.game_area)
        # move to the exist room
        if(agent.check_win):
            drawer.draw_update(window,grid,size,width,height) 
            drawer.draw_game_over_message(window,"WINNER","GOOD JOB!")
            pygame.time.delay(500)
            new_game = True

        # kill by pit or wumpus
        if(agent.is_alive == False):
            drawer.draw_update(window,grid,size,width,height) 
            drawer.draw_game_over_message(window,"CHICKEN","GAME OVER")
            pygame.time.delay(500)
            new_game = True
            
        
        if(new_game == True):
            pygame.draw.rect(window, init.WHITE, init.header_area)
            grid= drawer.make_grid_color(size, width, height, temp_grid)
            
            if(agent.check_win):
                agent,x_agent,y_agent = agent_lib.random_agent(size,grid)
            else:
                agent = agent_lib.previous_agent(size,grid,x_agent,y_agent)
            
            agent.draw_agent(grid,window)
            new_game = False

        restart = btn.Button(30, 25, "Restart", click4)
        run = btn.Button(190, 25, "Run", click3)
        drawer.draw_update(window,grid,size,width,height)     
        
        if(pygame.mouse.get_pressed()[0]) and one_press:
            one_press = False           
                
            if(restart.is_click()):
                pygame.draw.rect(window, init.WHITE, init.header_area)
                click4 = True
                
                grid= drawer.make_grid_color(size, width, height, temp_grid)
                agent,x_agent,y_agent = agent_lib.random_agent(size,grid)
                agent_lib.setWall(grid, size)
                agent.draw_agent(grid,window)

            if(run.is_click()):
                click3 = True
                if agent.has_move:
                    agent.addToKB(grid[agent.x_coord][agent.y_coord]) 
                agent.checkWithKB(grid)
                if len(agent.neighbor) != 0:
                    print ("neighbor: ")
                    for node in agent.neighbor:
                        print (node.x, node.y, node.countVisit)
                    leastVisited = min(agent.neighbor, key=lambda x: x.countVisit)
                    print(leastVisited.countVisit)
                    for node in agent.knowledge_base:
                        if node.x == leastVisited.x and node.y == leastVisited.y:
                            agent.move_to(node, grid, window)
                
                
        # keys = pygame.key.get_pressed()
        # pygame.key.set_repeat(0)
        
        # # Check for key presses and play game manual
        # if keys[pygame.K_a] and not move_left:
        #     move_left = True
        #     agent.move_agent('a', grid,window)
        # elif not keys[pygame.K_a]:
        #     move_left = False

        # if keys[pygame.K_w] and not move_up:
        #     move_up = True
        #     agent.move_agent('w', grid,window)
        # elif not keys[pygame.K_w]:
        #     move_up = False

        # if keys[pygame.K_s] and not move_down:
        #     move_down = True
        #     agent.move_agent('s', grid,window)
        # elif not keys[pygame.K_s]:
        #     move_down = False

        # if keys[pygame.K_d] and not move_right:
        #     move_right = True
        #     agent.move_agent('d', grid,window)
        # elif not keys[pygame.K_d]:
        #     move_right = False
        
        # if keys[pygame.K_SPACE] and not kill_press:
        #     kill_press = True
        #     agent.move_agent('space', grid,window)
        # elif not keys[pygame.K_SPACE]:
        #     kill_press = False
        
        if(not pygame.mouse.get_pressed()[0]) and not one_press:
            one_press = True
            click4 = False
            click3 = False
            restart.remove_click()
            restart.draw()
             
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
    pygame.quit()
    
if __name__ == "__main__":
    main(init.WINDOW, init.WIDTH, init.HEIGHT-100)