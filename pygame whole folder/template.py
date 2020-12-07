# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 09:13:05 2020

@author: stani
"""

#pygame template
import pygame
import os #use for different os pathways https://www.youtube.com/watch?v=fcryHcZE_sM&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw&index=3

WIDTH=960
HEIGHT=672
FPS=30

#define colours
WHITE=(255,255,255)
BLACK =(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
DARKGREY=(40,40,40)
LIGHTGREY=(100,100,100)
YELLOW=(255,255,0)

#TILES
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.image.load('astronaut.png')
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.center=(WIDTH/2, HEIGHT/2)
        
    
    def update(self):
        pass

#initialize pygame and create window
pygame.init()
pygame.mixer.init() #for sounds
screen=pygame.display.set_mode((WIDTH,HEIGHT))
#setting title
pygame.display.set_caption('Stranded') 
clock=pygame.time.Clock() #track the speed so the game is able to work the same on different devices

all_sprites=pygame.sprite.Group()
player=Player()
all_sprites.add(player)




#game loop
running=True
while running:
    clock.tick(FPS) #keep loop running at same speed
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #check for closing the window
            running=False
    
    #update
    all_sprites.update()
    #draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()
    
pygame.quit()


