import pygame as pg


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pg.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text("*", 15, self.cursor_rect.x, self.cursor_rect.y)
            
    def blit_screen(self):
        self.game.window.blit(self.game.screen, (0, 0))
        pg.display.update()
        self.game.reset_keys()




class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_dispplay = True
        self.game.font_name = self.game.font_title
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.screen.fill(self.game.BLACK)
            self.game.draw_text("Stranded", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 -20)
            self.game.draw_text("Play Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

        if self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"


    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
            elif self.state == "Options":
                pass
            elif self.state == "Credits":
                pass
"""
class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Volume"
        self.volx, voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
"""
