import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30

#define some color
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MY GAME")
clock = pygame.time.Clock()

#game loop
GAMEOVER = False
while GAMEOVER == False:
	#Process
	#Update
	#Render
	screen.fill(BLACK)