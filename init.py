from queue import PriorityQueue
import random
import matplotlib.pyplot as plt
import pygame
from enum import Enum

pygame.init()

WIDTH = 800
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
pygame.display.set_caption("WUMPUS WORLD")
font = pygame.font.Font('dlxfont.ttf', 12)
tile_font = pygame.font.Font('dlxfont.ttf', 12)
Error_area = pygame.Rect((WIDTH - 300) // 4-50, HEIGHT//2 -35, 350, 120)
game_area = pygame.Rect(0,100,WIDTH,HEIGHT-100) 
header_area = pygame.Rect(0,0,WIDTH,50)
point_area = pygame.Rect(300,5,200,70)
action_area = pygame.Rect(510,25,290,50)
percept_area = pygame.Rect(510,110,290,50)