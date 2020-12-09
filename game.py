import pygame as pg
from menu import MainMenu

class Game():
    def __init__(self):
        pg.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.RIGHT_KEY, self.LEFT_KEY, self.ACTION_KEY, self.START_KEY = False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1440, 896
        self.screen = pg.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pg.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_title = "OpenSansPXBold.ttf"
        self.font_dialog = "OpenSansPX.ttf"
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.curr_menu = MainMenu(self)

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.screen.fill(self.BLACK)
            self.draw_text("Thanks for playing", 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.screen, (0,0))
            pg.display.update()
            self.reset_keys()


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.runnig, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pg.KEYDOWN:
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


    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.RIGHT_KEY, self.LEFT_KEY, self.ACTION_KEY, self.START_KEY = False, False, False, False, False, False


    def draw_text(self, text, size, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_surface, text_rect)


