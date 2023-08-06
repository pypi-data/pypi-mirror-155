import asyncio
import importlib
import os
import pickle
import queue
import subprocess
import threading
import tkinter as tk
import webbrowser
from functools import partial
from itertools import zip_longest
from multiprocessing import Pipe, Process, Queue
from queue import Queue
from threading import Thread
from tkinter import *

import pygame
import pygame_menu
from pygame.locals import *
from pygame_menu._scrollarea import ScrollArea
from pygame_menu.baseimage import BaseImage
from pygame_menu.locals import *
from pygame_menu.widgets import *

from primaryschool.dirs import *
from primaryschool.dirs import user_screenshot_dir_path
from primaryschool.locale import _
from primaryschool.resource import (
    default_font,
    default_font_path,
    get_default_font,
    get_resource_path,
)
from primaryschool.settings import *
from primaryschool.subjects import subjects


class Player:
    def __init__(self):
        self.name = _("default_name")
        pass

    def get_name(self):
        return self.name

    def get_name_by_tk(self):
        self.show_name_entry()
        return self.get_name()

    def set_name(self, name):
        self.name = name

    def exit_player_name_tk(self, event=None):
        self.set_name(self.player_name_entry.get())
        self.tk_root.destroy()

    def show_name_entry(self):
        self.tk_root = tk.Tk()
        tk.Label(self.tk_root, text=_("Player name:")).pack(side=LEFT)
        self.player_name_entry = tk.Entry(self.tk_root, bd=5)
        self.player_name_entry.bind(
            "<Return>",
            self.exit_player_name_tk,
        )
        self.player_name_entry.pack(side=RIGHT)
        w, h = self.tk_root.winfo_reqwidth(), self.tk_root.winfo_reqheight()
        sw, sh = (
            self.tk_root.winfo_screenwidth(),
            self.tk_root.winfo_screenheight(),
        )
        self.tk_root.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")
        self.tk_root.resizable(False, False)
        self.tk_root.wm_protocol(
            "WM_DELETE_WINDOW",
            lambda: self.exit_player_name_tk(),
        )
        self.player_name_entry.focus_set()
        self.tk_root.mainloop()
