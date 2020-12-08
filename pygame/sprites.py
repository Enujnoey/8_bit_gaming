import pygame as pg
from random import uniform, choice, randint, random
from settings import *
from tilemap import *
import pytweening as tween
from itertools import chain
vec = pg.math.Vector2



class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
       # self.hit_rect = PLAYER_HIT_RECT
       # self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
       # self.rot = 0
        #self.last_shot = 0
        #self.health = PLAYER_HEALTH
       # self.weapon = 'pistol'
        #self.damaged = False

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

  #  def shoot(self):
    #    now = pg.time.get_ticks()
      #  if now - self.last_shot > WEAPONS[self.weapon]['rate']:
       #     self.last_shot = now
        #    dir = vec(1, 0).rotate(-self.rot)
         #   pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
         #   self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
          #  for i in range(WEAPONS[self.weapon]['bullet_count']):
           #     spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
           #     Bullet(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['damage'])
           #     snd = choice(self.game.weapon_sounds[self.weapon])
            #    if snd.get_num_channels() > 2:
             #       snd.stop()
             #   snd.play()
           # MuzzleFlash(self.game, pos)

   # def hit(self):
     #   self.damaged = True
      #  self.damage_alpha = chain(DAMAGE_ALPHA * 4)

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

   # def add_health(self, amount):
    #    self.health += amount
     #   if self.health > PLAYER_HEALTH:
      #      self.health = PLAYER_HEALTH

#class Mob(pg.sprite.Sprite):
 #   def __init__(self, game, x, y):
  #      self._layer = MOB_LAYER
   #     self.groups = game.all_sprites, game.mobs
    #    pg.sprite.Sprite.__init__(self, self.groups)
     #   self.game = game
      #  self.image = game.mob_img.copy()
       # self.rect = self.image.get_rect()
        #self.rect.center = (x, y)
        #self.hit_rect = MOB_HIT_RECT.copy()
        #self.hit_rect.center = self.rect.center
        #self.pos = vec(x, y)
       # self.vel = vec(0, 0)
        #self.acc = vec(0, 0)
        #self.rect.center = self.pos
        #self.rot = 0
        #self.health = MOB_HEALTH
        #self.speed = choice(MOB_SPEEDS)
       # self.target = game.player

   # def avoid_mobs(self):
    #    for mob in self.game.mobs:
     #       if mob != self:
      #          dist = self.pos - mob.pos
       #         if 0 < dist.length() < AVOID_RADIUS:
        #            self.acc += dist.normalize()

  #  def update(self):
 #       target_dist = self.target.pos - self.pos
  #      if target_dist.length_squared() < DETECT_RADIUS**2:
   #         if random() < 0.002:
    #            choice(self.game.zombie_moan_sounds).play()
     #       self.rot = target_dist.angle_to(vec(1, 0))
      #      self.image = pg.transform.rotate(self.game.mob_img, self.rot)
       #     self.rect.center = self.pos
        #    self.acc = vec(1, 0).rotate(-self.rot)
         #   self.avoid_mobs()
          #  self.acc.scale_to_length(self.speed)
           # self.acc += self.vel * -1
      #      self.vel += self.acc * self.game.dt
       #     self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        #    self.hit_rect.centerx = self.pos.x
        #    collide_with_walls(self, self.game.walls, 'x')
         #   self.hit_rect.centery = self.pos.y
         #   collide_with_walls(self, self.game.walls, 'y')
          #  self.rect.center = self.hit_rect.center
       # if self.health <= 0:
        #    choice(self.game.zombie_hit_sounds).play()
         #   self.kill()
          #  self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))

   # def draw_health(self):
    #    if self.health > 60:
     #       col = GREEN
      #  elif self.health > 30:
       #     col = YELLOW
       # else:
        #    col = RED
     #   width = int(self.rect.width * self.health / MOB_HEALTH)
      #  self.health_bar = pg.Rect(0, 0, width, 7)
      #  if self.health < MOB_HEALTH:
       #     pg.draw.rect(self.image, col, self.health_bar)

#class Bullet(pg.sprite.Sprite):
 #   def __init__(self, game, pos, dir, damage):
  #      self._layer = BULLET_LAYER
   #     self.groups = game.all_sprites, game.bullets
    #    pg.sprite.Sprite.__init__(self, self.groups)
     #   self.game = game
      #  self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
 #       self.rect = self.image.get_rect()
  #      self.hit_rect = self.rect
   #     self.pos = vec(pos)
    #    self.rect.center = pos
     #   #spread = uniform(-GUN_SPREAD, GUN_SPREAD)
      #  self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9, 1.1)
   #     self.spawn_time = pg.time.get_ticks()
    #    self.damage = damage

  #  def update(self):
   #     self.pos += self.vel * self.game.dt
    #    self.rect.center = self.pos
     #   if pg.sprite.spritecollideany(self, self.game.walls):
   #         self.kill()
    #    if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
     #       self.kill()

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

#class MuzzleFlash(pg.sprite.Sprite):
 #   def __init__(self, game, pos):
  #      self._layer = EFFECTS_LAYER
   #     self.groups = game.all_sprites
    #    pg.sprite.Sprite.__init__(self, self.groups)
     #   self.game = game
      #  size = randint(20, 50)
  #      self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
   #     self.rect = self.image.get_rect()
    #    self.pos = pos
     #   self.rect.center = pos
      #  self.spawn_time = pg.time.get_ticks()

  #  def update(self):
   #     if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
    #        self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1
