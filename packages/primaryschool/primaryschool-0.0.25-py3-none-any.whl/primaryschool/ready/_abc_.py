import asyncio
import importlib
import os
import pickle
import queue
import subprocess
import threading
import tkinter as tk
import webbrowser
from abc import ABC
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
from primaryschool.ready.psready import PSReady
from primaryschool.resource import (
    default_font,
    default_font_path,
    get_default_font,
    get_resource_path,
)
from primaryschool.settings import *
from primaryschool.subjects import subjects


class MenuBase(ABC):
    def __init__(self, ps, title=None):
        self.ps = ps
        self.title = title or _("PrimarySchool")
        self._menu = self.ps.get_default_menu(self.title)

    def add_widgets(self):
        pass
