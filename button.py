import init
from init import pygame

class Button:
    def __init__(self, x, y, text, click):
        self.x = x
        self.y = y
        self.text = text
        self.click = click
        self.draw()
        
    def draw(self):
        text_button = init.font.render(self.text, True, init.BLACK)
        button = pygame.rect.Rect((self.x, self.y), (160, 50))
        if self.click:
            pygame.draw.rect(init.WINDOW, init.GREEN, button, 0,5)
        else:
            pygame.draw.rect(init.WINDOW, init.IRISBLUE, button, 0,5)
        init.WINDOW.blit(text_button,(self.x +20, self.y + 15))
    
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