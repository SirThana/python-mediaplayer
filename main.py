#!/usr/bin/python
import tkinter as Tkinter
from tkinter import ttk
global root
root = Tkinter.Tk()
# Code to add widgets will go here...

menu_options = {'Music': ['Playlists', 'Artists', 'Albums', 'Songs', 'Podcasts', 'Genres', 'Composers', 'Audiobooks']}


def main():
    key, value = next(iter(menu_options.items()))
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    # ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text=key, command=root.destroy).grid(column=0, row=1)

    root.mainloop()
    
main()

