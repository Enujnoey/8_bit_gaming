"""
Created on Mon Dec  7 10:34:02 2020

@author: styssk, enujnoey

code modified from https://www.youtube.com/playlist?list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i
"""

import pygame as pg  #need to install ;a library used to run pygame functions
import sys #used to quit the game in different OS
from os import path #used to find files in different OS
from menu import *
import pytmx #need to install ; used to format the map
import pytweening as tween #need to install; used to move the items up and down
vec = pg.math.Vector2

# define colors  if needed(R, G, B)

# game settings
WIDTH = 1440  #screen width
HEIGHT = 896 #screen height
FPS = 60 #used together with clock to ensure that the game will run at the same speed on different devices
TITLE = "Stranded" #Title

#GRID SETTINGS 
TILESIZE = 64 #The map is based on a grid as it makes it easier to format
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 250 #how fast the player moves
PLAYER_IMG = 'astronaut128.png' #what the player looks like

#ITEM PROPERTIES
ITEM_IMAGES = {'battery': 'battery.png',
               'IDcard': 'idcard.png',
               'rejuvcapsule': 'rejuv.png',
               'endofchapter': 'smalllight.png'} # a dictionary to hold the items
BOB_RANGE=20 #used to move the item up and down so it's more noticable
BOB_SPEED=2
#LAYERS
WALL_LAYER=1
PLAYER_LAYER=2 #the player is on top of the items
ITEMS_LAYER=1

#FOG SETTINGS
NIGHT_COLOR=(20,20,20) # how dark is the environmet
LIGHT_RADIUS=(4000,4000) #how big is the visible area
LIGHT_MASK='light_350_med.png' #the image used for the visible area

battery_count=1 #used to count the batteries
endofchapter_count=0 #used as a condition to change stages
ID_count=0 # used to count the IDcards
ch1_playing=True #not implemented . this was supposed to be the original condition to change stages
ch3_playing=False #not implemented . this was supposed to be the original condition to change stages
ch4_playing=False #not implemented . this was supposed to be the original condition to change stages
ch5_playing=False #not implemented . this was supposed to be the original condition to change stages


#CLASSES
class Player(pg.sprite.Sprite): #sprite framework by pygame
    def __init__(self, game, x, y): #initializing the player class
        self._layer=PLAYER_LAYER #assigning the layer
        self.groups = game.all_sprites #adding the player to the sprite group
        pg.sprite.Sprite.__init__(self, self.groups) #needed for the sprite to work
        self.game = game
        self.image = game.player_img #what the sprite looks like
        self.rect = self.image.get_rect() #rectangle enclosing the sprite
        self.rect.center=(x,y) #rectangle coordinates
        self.vx, self.vy = 0, 0 #used for movement
        self.x = x #player position
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

class Obstacle(pg.sprite.Sprite): #used to assign the obstacles from the map
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
        
class Item(pg.sprite.Sprite): #class for the items
    def __init__(self,game,pos,type):
        self._layer=ITEMS_LAYER
        self.groups=game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game=game
        self.image=game.item_images[type]
        self.rect=self.image.get_rect()
        self.type=type #which item from the dictionary
        self.pos=pos #where is the item
        self.rect.center=pos #where is the item's rectangle
        self.tween=tween.easeInOutSine #used to move the item
        self.step=0
        self.dir=1
        
    def update(self): #used to move the item
        offset=BOB_RANGE * (self.tween(self.step/BOB_RANGE) -0.5)
        self.rect.centery=self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step=0
            self.dir *= -1
            

class Map: #used to create the map
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        
class TiledMap: #used to load the map from Tiled
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


class Game: #class for the Game itself
    def __init__(self):
        pg.init() #initializes the pygame library
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) #creates the window
        pg.display.set_caption(TITLE) #sets the title
        self.clock = pg.time.Clock() #sets the clock
        pg.key.set_repeat(500, 100) #used to hold a key instead of pressing it multiple times
        self.load_data()
        #for the menu setting
        self.window = pg.Surface((WIDTH, HEIGHT))
        self.font_title = "OpenSansPXBold.ttf"
        self.font_dialog = "OpenSansPX.ttf"
        self.DISPLAY_W = WIDTH
        self.DISPLAY_H = HEIGHT
        self.running, self.playing = True, False #Set two loops for the menus 
        self.UP_KEY, self.DOWN_KEY, self.RIGHT_KEY, self.LEFT_KEY, self.ACTION_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False, False 
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        
    def load_data(self):
        game_folder = path.dirname(__file__) #assigns the game folder 
        img_folder = path.join(game_folder, 'img') #assigns the image folder
        snd_folder = path.join(game_folder, 'snd') #assigns the sound folder
        music_folder = path.join(game_folder, 'music') #assigns the music folder
        self.map_folder = path.join(game_folder, 'maps') #assigns the mape folder
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha() #converts and loads the player image
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
        self.map = TiledMap(path.join(self.map_folder, 'map.tmx')) #uses a file for the map
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:  #assigns objects from the map program to python
            obj_center=vec(tile_object.x + tile_object.width /2, tile_object.y + tile_object.height /2)
            if tile_object.name == 'player':
                self.player=Player(self,obj_center.x,obj_center.y)
            elif tile_object.name == 'player_ch3' and ch3_playing ==True:
                self.player=Player(self,obj_center.x,obj_center.y)
            elif tile_object.name == 'player_ch4' and ch4_playing ==True:
                self.player=Player(self,obj_center.x,obj_center.y)
            elif tile_object.name == 'player_ch5' and ch5_playing ==True:
                self.player=Player(self,obj_center.x,obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name in ['battery', 'IDcard','rejuvcapsule','endofchapter']:
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
        global battery_count
        global ID_count
        global endofchapter_count
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
            if hit.type == 'endofchapter':
                endofchapter_count +=1
                hit.kill()
            if hit.type == 'rejuvcapsule':
                pass  #reduce radiation
        for tile_object in self.map.tmxdata.objects: 
            obj_center=vec(tile_object.x + tile_object.width /2, tile_object.y + tile_object.height /2)
            if tile_object.name == 'player_ch3' and endofchapter_count ==1:
                self.player=Player(self,obj_center.x,obj_center.y)
                endofchapter_count=-3
            elif tile_object.name == 'player_ch4' and endofchapter_count ==-2:
                self.player=Player(self,obj_center.x,obj_center.y)
                endofchapter_count=-5
            elif tile_object.name == 'player_ch5' and endofchapter_count ==-4 and ID_count ==1:
                self.player=Player(self,obj_center.x,obj_center.y)
                endofchapter_count=-7

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

    def draw_text(self,text, size, x, y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text, True, (255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def events(self):
        # check events
        for event in pg.event.get():  #events for closing ht window
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_RETURN:
                    self.START_KEY = True
                if event.key == pg.K_SPACE:
                    self.ACTION_KEY = True
                if event.key == pg.K_UP:
                    self.UP_KEY = True
                if event.key == pg.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pg.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pg.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pg.K_BACKSPACE:
                    self.BACK_KEY = True


    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.RIGHT_KEY, self.LEFT_KEY, self.ACTION_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False, False

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while g.running:
    g.curr_menu.display_menu() # bug when we press enter
    g.new()
    g.run()
    g.show_go_screen()
