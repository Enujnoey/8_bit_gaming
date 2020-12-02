import pygame
pygame.init()

#GAMESETTINGS
WIDTH=1440
HEIGHT=896

#Window Setup
win = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Stranded")




"""
Define Classes on the top
"""

#Our Player
class player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5 # speed
        self.left = False #for the sprite() and movement
        self.right = False
        self.walkCount = 0

"""
class MoveImages(self):
    def __init__(self):
        walkleft = []
        walfright = []

    def getting imange and append it to the walkleft/walkright list 
"""



"""
Define Functions under this comment
"""

def reDrawGameWindow():
    win.fill((0,0,0))
    pygame.draw.rect(win, ("green"), (square.x,square.y,square.    width,square.height))
    pygame.display.update()



#Setup player 
square = player(670,410,80,100)

#Main loop
run = True
while run:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and square.x > square.vel:
        square.x -= square.vel

    if keys[pygame.K_RIGHT] and square.x < WIDTH - square.width - square.vel:
        square.x += square.vel

    if keys[pygame.K_UP] and square.y > square.vel:
        square.y -= square.vel

    if keys[pygame.K_DOWN] and square.y < HEIGHT - square.height - square.vel:
        square.y += square.vel

    reDrawGameWindow()
pygame.quit()
