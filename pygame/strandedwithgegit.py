# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 10:34:02 2020

@author: styssk
"""

import pygame as pg  #need to install ;a library used to run pygame functions
import sys 
from os import path #used to find files in different OS
import pytmx #need to install ; used to format the map
import pytweening as tween #need to install; used to move the items up and down
vec = pg.math.Vector2

# define colors  if needed(R, G, B)

# game settings
WIDTH = 1440  
HEIGHT = 896 
FPS = 60 #used together with clock to ensure that the game will run at the same speed on different devices
TITLE = "Stranded"

#GRID SETTINGS
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 250
PLAYER_IMG = 'astronaut128.png'

#ITEM PROPERTIES
ITEM_IMAGES={'battery': 'battery.png'}
BOB_RANGE=20
BOB_SPEED=2
#LAYERS
WALL_LAYER=1
PLAYER_LAYER=2
ITEMS_LAYER=1

#FOG SETTINGS
NIGHT_COLOR=(20,20,20)
LIGHT_RADIUS=(2000,2000)
LIGHT_MASK='light_350_med.png'




#CLASSES
class Player(pg.sprite.Sprite): #sprite framework by pygame
    def __init__(self, game, x, y):
        self._layer=PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups) #needed for the sprite to work
        self.game = game
        self.image = game.player_img #what the sprite looks like
        self.rect = self.image.get_rect() #rectangle enclosing the sprite
        self.rect.center=(x,y)
        self.vx, self.vy = 0, 0
        self.x = x
        self.y = y

    def get_keys(self): #used for player movement
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        

    def collide_with_walls(self, dir):
        if dir == 'x': #wall colission on the x axis
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y': #wall colission on the y axis
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self._layer=WALL_LAYER
        self.groups =game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect =pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y 
        
class Item(pg.sprite.Sprite):
    def __init__(self,game,pos,type):
        self._layer=ITEMS_LAYER
        self.groups=game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game=game
        self.image=game.item_images[type]
        self.rect=self.image.get_rect()
        self.type=type
        self.pos=pos
        self.rect.center=pos
        self.tween=tween.easeInOutSine
        self.step=0
        self.dir=1
        
    def update(self):
        offset=BOB_RANGE * (self.tween(self.step/BOB_RANGE) -0.5)
        self.rect.centery=self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step=0
            self.dir *= -1
            

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        
class TiledMap:
    def __init__(self,filename):
        tm=pytmx.load_pygame(filename,pixelalpha=True)
        self.width=tm.width * tm.tilewidth
        self.height=tm.height * tm.tileheight
        self.tmxdata=tm
        
    def render(self,surface):
        ti= self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer,pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile= ti(gid)
                    if tile:
                        surface.blit(tile,(x * self.tmxdata.tilewidth,y * self.tmxdata.tileheight))
    def make_map(self):
        temp_surface= pg.Surface((self.width,self.height))
        self.render(temp_surface)
        return temp_surface

class Camera(): #class for the camera that follows the player
    def __init__(self,width,height):
        self.camera=pg.Rect(0,0,width,height)
        self.width=width
        self.height=height
        
    def apply(self,entity):
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self,rect):
        return rect.move(self.camera.topleft)
    
    def update(self,target):
        x= -target.rect.x + int(WIDTH/2)
        y= -target.rect.y + int(HEIGHT/2)
        self.camera=pg.Rect(x,y,self.width,self.height)         


class Game:
    def __init__(self):
        pg.init() #initializes the pygame library
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) #creates the window
        pg.display.set_caption(TITLE) #sets the title
        self.clock = pg.time.Clock() #sets the clock
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
         game_folder = path.dirname(__file__)
         img_folder = path.join(game_folder, 'img')
         snd_folder = path.join(game_folder, 'snd')
         music_folder = path.join(game_folder, 'music')
         self.map_folder = path.join(game_folder, 'maps')
         self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
         #make the other folders https://www.youtube.com/watch?v=fcryHcZE_sM&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw&index=3
         self.item_images={}
         for item in ITEM_IMAGES:
             self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
         #field ov vision
         self.fog=pg.Surface((WIDTH,HEIGHT))
         self.fog.fill(NIGHT_COLOR)
         self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
         self.light_mask=pg.transform.scale(self.light_mask,LIGHT_RADIUS)
         self.light_rect=self.light_mask.get_rect()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates() #groups sprites to make drawing easier
        self.walls = pg.sprite.Group() #groups walls
        self.items = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'map.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects: 
            obj_center=vec(tile_object.x + tile_object.width /2, tile_object.y + tile_object.height /2)
            if tile_object.name == 'player':
                self.player=Player(self,obj_center.x,obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name in ['battery', 'IDcard']:
                Item(self, obj_center, tile_object.name)
        self.camera=Camera(self.map.width,self.map.height)

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 #loops run at the same speed
            self.events()
            self.update()
            self.draw()

    def quit(self): #quits the game
        pg.quit()
        sys.exit()
        
# update portion of the game loop
    def update(self):
        battery_count=0
        ID_count=0
        self.all_sprites.update() #update all sprites
        self.camera.update(self.player) #updates camera
        hits=pg.sprite.spritecollide(self.player,self.items, False)
        for hit in hits:
            if hit.type == 'battery':
                hit.kill()
                battery_count +=1
            if hit.type == 'IDcard':
                ID_count +=1
                hit.kill()
                # I need to do hits for radiation and doors
#screen fog
    def render_fog(self):
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center=self.camera.apply(self.player).center
        self.fog.blit(self.light_mask,self.light_rect)
        self.screen.blit(self.fog,(0,0),special_flags=pg.BLEND_MULT)
   
    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image,self.camera.apply(sprite)) #draws all sprites
            #field of vision -has to be done before the HUD
            self.render_fog()
            #HUD to be done
        pg.display.flip() #after drawing everything (double buffering)

    def events(self):
        # check events
        for event in pg.event.get():  #events for closing ht window
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()