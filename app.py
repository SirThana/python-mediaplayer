import tkinter as tk 
import socket
import json
import time
from datetime import timedelta
from select import select
from tkinter import ttk
# from view_model import *
from PIL import ImageTk, Image
from sys import platform
import os
import re as re
from pudb import set_trace

MENU_PAGE_SIZE = 6

# Screen render types
MENU_RENDER_TYPE = 0
NOW_PLAYING_RENDER = 1
SEARCH_RENDER = 2

# Menu line item types
LINE_NORMAL = 0
LINE_HIGHLIGHT = 1
LINE_TITLE = 2

LARGEFONT =("ChicagoFLF", 90) 
MED_FONT =("ChicagoFLF", 70) 
SCALE = 1
SPOT_GREEN = "#1DB954"
SPOT_BLACK = "#191414"
SPOT_WHITE = "#FFFFFF"

UDP_IP = "127.0.0.1"
UDP_PORT = 9090

DIVIDER_HEIGHT = 3

UP_KEY_CODE = 8255233 if platform == "darwin" else 111
DOWN_KEY_CODE = 8320768 if platform == "darwin" else 116
LEFT_KEY_CODE = 8124162 if platform == "darwin" else 113
RIGHT_KEY_CODE = 8189699 if platform == "darwin" else 114
PREV_KEY_CODE = 2818092 if platform == "darwin" else 0
NEXT_KEY_CODE = 3080238 if platform == "darwin" else 0
PLAY_KEY_CODE = 3211296 if platform == "darwin" else 0

SCREEN_TIMEOUT_SECONDS = 60

wheel_position = -1
last_button = -1

last_interaction = time.time()
screen_on = True

class tkinterApp(tk.Tk): 
      
    # __init__ function for class tkinterApp  
    def __init__(self, *args, **kwargs):  
        global LARGEFONT, MED_FONT, SCALE
        # __init__ function for class Tk 
        tk.Tk.__init__(self, *args, **kwargs)

        if (platform == 'darwin'):
            self.geometry("320x240")
            SCALE = 0.3
        else:
            self.attributes('-fullscreen', True)
            SCALE = self.winfo_screenheight() / 930

        LARGEFONT =("ChicagoFLF", int(72 * SCALE))
        MED_FONT =("ChicagoFLF", int(52 * SCALE))
        # creating a container 
        container = tk.Frame(self)   
        container.pack(side = "top", fill = "both", expand = True)  
   
        container.grid_rowconfigure(0, weight = 1) 
        container.grid_columnconfigure(0, weight = 1) 
   
        # initializing frames to an empty array 
        self.frames = {}   
   
        # iterating through a tuple consisting 
        # of the different page layouts 
   
    # to display the current frame passed as 
    # parameter 
    def show_frame(self, cont): 
        frame = self.frames[cont] 
        frame.tkraise() 

class Rendering():
    def __init__(self, type):
        self.type = type

    def unsubscribe(self):
        pass

class LineItem():
    def __init__(self, title = "", line_type = LINE_NORMAL, show_arrow = False):
        self.title = title
        self.line_type = line_type
        self.show_arrow = show_arrow
        
class MenuPage():
    def __init__(self, header, previous_page, has_sub_page, is_title = False):
        self.index = 0
        self.page_start = 0
        self.header = header
        self.has_sub_page = has_sub_page
        self.previous_page = previous_page
        self.is_title = is_title

    def total_size(self):
        return 0

    def page_at(self, index):
        return None

    def nav_prev(self):
        pass

    def nav_next(self):
        pass

    def nav_play(self):
        pass
    
    def get_index_jump_up(self):
        return 1

    def get_index_jump_down(self):
        return 1

    def nav_up(self):
        jump = self.get_index_jump_up()
        if(self.index >= self.total_size() - jump):
            return
        if (self.index >= self.page_start + MENU_PAGE_SIZE - jump):
            self.page_start = self.page_start + jump
        self.index = self.index + jump

    def nav_down(self):
        jump = self.get_index_jump_down()
        if(self.index <= (jump - 1)):
            return
        if (self.index <= self.page_start + (jump - 1)):
            self.page_start = self.page_start - jump
            if (self.page_start == 1):
                self.page_start = 0
        self.index = self.index - jump

    def nav_select(self):
        return self.page_at(self.index)

    def nav_back(self):
        return self.previous_page

    def render(self):
        lines = []
        total_size = self.total_size()
        for i in range(self.page_start, self.page_start + MENU_PAGE_SIZE):
            if (i < total_size):
                page = self.page_at(i)
                if (page is None) :
                    lines.append(LineItem())
                else:
                    line_type = LINE_TITLE if page.is_title else \
                        LINE_HIGHLIGHT if i == self.index else LINE_NORMAL
                    lines.append(LineItem(page.header, line_type, page.has_sub_page))
            else:
                lines.append(LineItem())
        return MenuRendering(lines=lines, header=self.header, page_start=self.index, total_count=total_size)

class MenuRendering(Rendering):
    def __init__(self, header = "", lines = [], page_start = 0, total_count = 0):
        super().__init__(MENU_RENDER_TYPE)
        self.lines = lines
        self.header = header
        self.page_start = page_start
        self.total_count = total_count
        self.now_playing = []
        self.has_internet = True

class RootPage(MenuPage):
    def __init__(self, previous_page):
        super().__init__("Ari's ipod", previous_page, has_sub_page=True)
        self.pages = [
         "Playlists",
         "Now playing"
        ]
        self.index = 0
        self.page_start = 0
    
    def get_pages(self):
        return self.pages
    
    def total_size(self):
        return len(self.get_pages())

    def page_at(self, index):
        return self.get_pages()[index]

page = RootPage(None)
app = tkinterApp() 

def screen_sleep():
    global screen_on
    screen_on = False
    os.system('xset -display :0 dpms force off')

def screen_wake():
    global screen_on
    screen_on = True
    os.system('xset -display :0 dpms force on')


def render(app, render):
    pass
    

def app_main_loop():
    global app, page, loop_count, last_interaction, screen_on
    try:
        loop_count += 1
        if (loop_count >= 300):
            if (time.time() - last_interaction > SCREEN_TIMEOUT_SECONDS and screen_on):
                screen_sleep()
            render(app, page.render())
            loop_count = 0
    except:
        pass
    finally:
        app.after(2, app_main_loop)
