import asyncio
import importlib
import os
import pickle
import queue
import subprocess
import sys
import threading
import tkinter as tk
import uuid
import webbrowser
from functools import partial
from importlib import import_module
from itertools import zip_longest
from multiprocessing import Pipe, Process, Queue
from queue import Queue
from threading import Thread
from tkinter import *
from tkinter import ttk

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
from primaryschool.ready.abc import WidgetABC
from primaryschool.ready.common import tk_text_insert
from primaryschool.resource import (
    default_font,
    default_font_path,
    get_default_font,
    get_resource_path,
)
from primaryschool.settings import *
from primaryschool.settings_t import *
from primaryschool.subjects import subjects


class AboutToplevel(WidgetABC):
    def __init__(
        self,
        psready,
        w=None,
        h=None,
        x=None,
        y=None,
        title=None,
        place=True,
        set_text_content=True,
        resizable=(False, False),
        text_spacing1=8,
        text_spacing2=8,
    ):
        super().__init__(psready)
        self.w = w or self.psready.get_screenwidth(of=4)
        self.h = h or self.psready.get_screenheight(of=4)
        self.x = x or 3 * self.psready.get_screenwidth(of=8)
        self.y = y or 3 * self.psready.get_screenheight(of=8)
        self.withdraw = False
        self.toplevel = tk.Toplevel(self.root)
        self.toplevel.resizable(*resizable)
        self.toplevel.protocol("WM_DELETE_WINDOW", self.ok)
        self.scrollbar = tk.Scrollbar(self.toplevel)
        self.text = tk.Text(
            self.toplevel,
            spacing1=text_spacing1,
            spacing2=text_spacing2,
        )
        self.ok_btn = tk.Button(self.toplevel, text=_("OK"), command=self.ok)

        self.scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)

        self.set_title()
        self.set_geometry()

        if set_text_content:
            self.set_text_content()
        if place:
            self.place()

    def set_title(self, title=None):
        self.toplevel.title(title or _("About"))

    def set_geometry(self, geometry=None):
        self.toplevel.geometry(
            geometry or (f"{self.w}x{self.h}" + f"+{self.x}+{self.y}")
        )

    def get_text_ok_btn_space(self):
        return 8

    def get_text_h(self):
        return self.h - self.get_ok_btn_h() - self.get_text_ok_btn_space()

    def get_ok_btn_x(self):
        return int((self.w - self.get_ok_btn_w()) / 2)

    def get_ok_btn_y(self):
        return self.get_text_h() + self.get_text_ok_btn_space()

    def get_ok_btn_h(self):
        return self.ok_btn.winfo_reqheight()

    def get_ok_btn_w(self):
        return self.ok_btn.winfo_reqwidth()

    def get_scrollbar_w(self):
        return self.scrollbar.winfo_reqwidth()

    def get_text_w(self):
        return self.w - self.get_scrollbar_w()

    def ok(self):
        if self.withdraw:
            self.toplevel.deiconify()
        else:
            self.toplevel.withdraw()
        self.withdraw = not self.withdraw

    def get_text_content_len(self):
        return len(self.text.get("1.0", "end-1c"))

    def default_text_insert(
        self,
        content,
        newline=True,
        font=None,
        justify="center",
        foreground=None,
        background=None,
        cursor=None,
    ):
        return tk_text_insert(
            self.text,
            content,
            newline=newline,
            font=font,
            justify=justify,
            foreground=foreground,
            background=background,
            cursor=cursor,
        )

    def set_text_content(self):

        self.default_text_insert(
            content=app_name_t,
            font="None 18",
        )
        self.default_text_insert(
            content=app_version,
            font="None 10",
        )
        self.default_text_insert(
            content=app_description_t,
            font="None 10",
        )
        app_url_tag = self.default_text_insert(
            content=app_url,
            font="None 10",
            foreground="blue",
            cursor="shuttle",
        )
        self.text.tag_bind(app_url_tag, "<1>", self.open_app_url)

        self.default_text_insert(
            content=_("Author:"), font="None 10", justify="center"
        )

        self.default_text_insert(
            content=app_author, font="None 10", justify="center"
        )

        self.default_text_insert(
            content=_("Contributors:"), font="None 10", justify="center"
        )

        for app_contributor in app_contributors[1:]:
            self.default_text_insert(
                content=app_contributor, font="None 10", justify="center"
            )

        self.text.config(state="disabled")

    def open_app_url(self, event):
        webbrowser.open(app_url)

    def place(self):
        self.scrollbar.place(
            x=self.get_text_w(), y=0, height=self.get_text_h()
        )
        self.text.place(
            x=0, y=0, width=self.get_text_w(), height=self.get_text_h()
        )
        self.ok_btn.place(y=self.get_ok_btn_y(), x=self.get_ok_btn_x())


class PSReady:
    def __init__(self, player_name=None):
        self.player_name = player_name or _("default_name")
        self.root = Tk()
        self.psframe = tk.Frame(self.root)
        self.abouttoplevel = None
        self.psframe_padx = (10, 10)
        self.psframe_pady = (10, 10)
        self.data = self.get_ready_data()

    def is_default_player_name(self):
        return self.player_name == _("default_name")

    def get_ready_data(self):
        """
        Warning:
        The pickle module is not secure. Only unpickle data you trust.
        """
        with open(get_ready_data_path(), "rb") as f:
            self.data = pickle.load(f, encoding="UTF-8")
        return self.data

    def set_ready_data(self):
        with open(get_ready_data_path(), "wb") as f:
            pickle.dump(self.data, f)

    def get_screenwidth(self, of=1):
        return int(self.root.winfo_screenwidth() / of)

    def get_screenheight(self, of=1):
        return int(self.root.winfo_screenheight() / of)

    def set_title(self, title=None):
        self.root.title(title or _("PrimarySchool"))

    def get_player_name(self):
        return (
            self.is_default_player_name()
            and self.data.get("player_name", self.player_name)
            or self.player_name
        )

    def exit_command(self):
        self.exit()

    def about_command(self):
        if self.abouttoplevel:
            self.abouttoplevel.ok()
        else:
            self.abouttoplevel = AboutToplevel(self)

    def add_widgets(self, ps_name_label=None):

        self.ps_name_label = ps_name_label or tk.Label(
            self.psframe, text=_("PrimarySchool"), font=("None", 24)
        )
        self.ps_name_label.grid(row=0, columnspan=2)

        tk.Label(self.psframe, text=_("Player name:")).grid(row=1, column=0)
        self.player_name_entry = tk.Entry(self.psframe)
        self.player_name_entry.insert(0, self.get_player_name())
        self.player_name_entry.grid(row=1, column=1)

        tk.Button(self.psframe, text=_("GO"), command=self.exit_command).grid(
            row=2, column=1, sticky="e"
        )

        tk.Button(
            self.psframe, text=_("About"), command=self.about_command
        ).grid(row=2, column=0, sticky="w")

        self.psframe.grid(
            row=0, column=0, padx=self.psframe_padx, pady=self.psframe_pady
        )

    def bind_widgets(self):
        self.player_name_entry.bind(
            "<Return>",
            self.exit,
        )
        pass

    def get_input(self):
        self.set_title()
        self.add_widgets()
        self.bind_widgets()
        self.mainloop()

    def set_player_name(self, name):
        self.player_name = name
        self.data["player_name"] = self.player_name

    def focus_set(self):
        self.player_name_entry.focus_set()

    def set_inputs(self):
        self.set_player_name(self.player_name_entry.get())

    def exit(self, event=None):
        self.set_inputs()
        self.set_ready_data()
        self.root.destroy()

    def sys_exit(self):
        self.root.destroy()
        sys.exit(0)

    def mainloop(self):
        w, h = self.root.winfo_reqwidth(), self.root.winfo_reqheight()
        sw, sh = (
            self.root.winfo_screenwidth(),
            self.root.winfo_screenheight(),
        )
        self.root.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")
        self.root.resizable(False, False)
        self.root.wm_protocol(
            "WM_DELETE_WINDOW",
            lambda: self.sys_exit(),
        )
        if self.player_name_entry:
            self.player_name_entry.focus_set()

        self.root.mainloop()
