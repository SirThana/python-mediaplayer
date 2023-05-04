#!/usr/bin/python
import tkinter as tk
from tkinter import ttk
import tkinter as Tkinter
import tkinter.font as fnt
import collections
from pudb import set_trace

global font_size
font_size = 20

menu_options = {'Music':
    [{'Playlists': [{'c': 'y', 'x': 5}]}, {'Artists': [{'a': 'b'}, [5, 5]]}, 'Albums', 'Songs',
     'Podcasts', 'Genres', 'Composers', 'Audiobooks']}

def load(key, curr_col, curr_row, options, bs):
    if not key:
        # special case where the key can't load more data, 
        # but should instead do something special
        pass
    curr_col += 1
    for n, opt in enumerate(options):
        if type(opt) == dict:
            # set_trace()
            key, value = next(iter(opt.items()))
            tk.Button(frm, text=key, font=fnt.Font(size=font_size), command=lambda i=n: load(key, curr_col, 1, value, i)).grid(column=curr_col, row=curr_row)
            curr_row += 1
        else:
            tk.Button(frm, text=opt, font=fnt.Font(size=font_size), command=window.destroy).grid(column=curr_col, row=curr_row)
            curr_row += 1

def main():
    global curr_col
    global curr_row
    global window
    global frm
    curr_col = 0
    curr_row = 1
    window = Tkinter.Tk()
    window.geometry("500x500")
    frm = ttk.Frame(window, padding=10)
    frm.grid()

    key, value = next(iter(menu_options.items()))
    btn = tk.Button(frm, text=key, font=fnt.Font(size=font_size), command=lambda: load(key, curr_col, curr_row, value, 1)).grid(column=curr_col, row=curr_row)
    # btn['command'] = load(key, curr_col, curr_row)


    window.mainloop()

    
main()

