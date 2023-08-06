import asyncio
import importlib
import os
import pickle
import queue
import subprocess
import sys
import threading
import tkinter as tk
import webbrowser
from datetime import datetime, timedelta
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
from primaryschool.ready._abc_ import MenuBase
from primaryschool.ready.psready import PSReady
from primaryschool.resource import (
    default_font,
    default_font_path,
    get_default_font,
    get_resource_path,
)
from primaryschool.settings import *
from primaryschool.subjects import subjects

app_description_t = _("app_description_t")


class SaveMenu(MenuBase):
    def __init__(self, ps):
        self.ps = ps
        self.surface = self.ps.surface
        self.title = _("Save game?")
        self._menu = self.ps.get_default_menu(self.title)
        self.save = False

    def add_widgets(self):

        self._menu.add.button(
            _("Save and return"),
            self.save_the_game,
            font_name=self.ps.font_path,
        )
        self._menu.add.button(
            _("Continue"), self.continue_the_game, font_name=self.ps.font_path
        )
        self._menu.add.button(
            _("Return to play menu"),
            self.to_play_menu,
            font_name=self.ps.font_path,
        )

    def to_play_menu(self):
        self.ps.play_menu._menu.full_reset()
        self.ps.play_menu._menu.enable()
        self.ps.play_menu._menu.mainloop(self.surface)

    def save_the_game(self):
        self.ps.subject_game.save(self.ps)
        self._menu.disable()
        self.to_play_menu()

    def continue_the_game(self):
        self._menu.disable()


class ScoreMenu(MenuBase):
    def __init__(self, ps, title=_("Score"), _test=False):
        super().__init__(ps, title)
        self._pass = False
        self.screenshot_path = None
        self._test = _test
        self.to_play_menu = self.ps.save_menu.to_play_menu
        self.score = 0

    def set_pass(self, _pass):
        self._pass = _pass

    def get_greeting(self):
        return (
            _("Success! Dear %s, you are so awesome!")
            if self.get_score_pass()
            else _("Dear %s, practice makes perfect, keep trying!")
        ) % self.ps.player_name

    def set_cost_str(self, cost_str):
        self.cost_str = cost_str

    def update_widgets(self, score, _pass, cost_str, screenshot_path):
        self.set_score(score)
        self.set_pass(_pass)
        self.set_cost_str(cost_str)
        self.set_screenshot_path(screenshot_path)

        self.pass_label.set_title(self.get_greeting())
        self.score_label.set_title(self.get_score())
        self.cost_label.set_title(self.get_datetime_diff())

    def get_screenshot_path(self):
        return self.screenshot_path

    def set_screenshot_path(self, path):
        self.screenshot_path = path

    def take_screenshot(self):
        if not self.screenshot_path:
            print(_("Screenshot path is not set."))
            return
        pygame.image.save(self.ps.surface, self.get_screenshot_path())
        if self._test:
            print(_("Screenshot saved."))
        self.save_screenshot_button.set_title(_("Screenshot Saved!"))

    def set_score_pass(self, _pass=False):
        self._pass = _pass

    def add_widgets(self):
        self.pass_label = self._menu.add.label("", max_char=-1)
        self.score_label = self._menu.add.label("", max_char=-1)
        self.cost_label = self._menu.add.label("", max_char=-1)
        self.save_screenshot_button = self._menu.add.button(
            _("Save Screenshot"),
            self.take_screenshot,
        )
        self.return_button = self._menu.add.button(
            _("Return"),
            self.to_play_menu,
        )

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score

    def get_score_pass(self):
        return self._pass

    def get_datetime_diff(self):
        return _("Cost: ") + self.cost_str


class PlayMenu(MenuBase):
    def __init__(
        self,
        ps,
        show_open_screenshots_button=True,
    ):
        self.ps = ps
        self.show_open_screenshots_button = show_open_screenshots_button
        self.title = _("Play Game")
        self.player_name = self.ps.player_name
        self.player_name_button = None
        self._menu = self.ps.get_default_menu(self.title)
        self.subjects = self.ps.subjects
        self.subject_games = self.ps.subject_games
        self.subject_index = self.ps.subject_index = 0
        self.subject_game_index = self.ps.subject_game_index
        self.difficulty_index = self.ps.difficulty_index
        self.subject = self.ps.subject
        self.subject_game = self.ps.subject_game
        self.subject_dropselect = None
        self.subject_game_dropselect = None
        self.difficulty_dropselect = None
        self.continue_button = None
        self.selection_box_bgcolor = (255, 255, 255)
        self.help_label = None
        self.help_label_font = get_default_font(20)
        self.esc_lael_font = get_default_font(16)
        self.esc_lael_font.set_bold(True)
        self.help_label_bg = (228, 0, 252, 30)
        self.help_label_border_color = (228, 0, 252, 200)

    def open_screenshots_dir(self):
        _open = (
            sys.platform == "darwin"
            and "open"
            or sys.platform == "win32"
            and "explorer"
            or "xdg-open"
        )
        subprocess.Popen([_open, user_screenshot_dir_path])

    def add_widgets(self):
        self.player_name_button = self._menu.add.button(
            _("Name :") + self.ps.get_player_name(),
            font_name=self.ps.font_path,
        )

        self.subject_dropselect = self._menu.add.dropselect(
            title=_("Subject :"),
            items=[(s.name_t, index) for index, s in enumerate(self.subjects)],
            font_name=self.ps.font_path,
            default=0,
            selection_box_bgcolor=self.selection_box_bgcolor,
            placeholder=_("Select a Subject"),
            onchange=self.on_subject_dropselect_change,
        )
        self.subject_game_dropselect = self._menu.add.dropselect(
            title=_("Game :"),
            items=[
                (g.name_t, index) for index, g in enumerate(self.subject_games)
            ],
            font_name=self.ps.font_path,
            default=0,
            selection_box_bgcolor=self.selection_box_bgcolor,
            placeholder=_("Select a game"),
            onchange=self.on_subject_game_dropselect_change,
        )

        self.difficulty_dropselect = self._menu.add.dropselect(
            title=_("Difficulty :"),
            items=[
                (d, index)
                for index, d in enumerate(self.subject_games[0].difficulties)
            ],
            font_name=self.ps.font_path,
            default=0,
            selection_box_bgcolor=self.selection_box_bgcolor,
            placeholder=_("Select a difficulty"),
            onchange=self.on_difficulty_dropselect_change,
        )
        self.update_selection_box_width()
        self.set_difficulty_index()

        self._menu.add.button(
            _("Play"), self.play_btn_onreturn, font_name=self.ps.font_path
        )

        self.continue_button = self._menu.add.button(
            _("Continue"),
            self.continue_btn_onreturn,
            font_name=self.ps.font_path,
        )
        self.update_continue_button()

        self.exit_button = self._menu.add.button(
            _("Exit"),
            self.ps.sys_exit,
            font_name=self.ps.font_path,
        )

        self.help_label = self._menu.add.label(
            "", font_name=self.help_label_font, max_char=-1
        )
        self.update_help_label()

        self._menu.add.label(
            _("After starting the game, press ESC to return."),
            font_name=self.esc_lael_font,
            font_color=(255, 0, 0),
            max_char=-1,
        )

        if self.show_open_screenshots_button:
            self._menu.add.button(
                _("Screenshots >>"),
                self.open_screenshots_dir,
                font_name=self.ps.font_path,
                align=pygame_menu.locals.ALIGN_RIGHT,
                background_color=(200, 200, 200, 200),
                font_color=(220, 20, 100),
            )

    def update_selection_box_width(self):
        for ds in [
            self.subject_dropselect,
            self.subject_game_dropselect,
            self.difficulty_dropselect,
        ]:

            ds._selection_box_width = (
                max([b.get_width() for b in ds._option_buttons])
                + ds._selection_box_inflate[0]
            )
            ds._make_selection_drop()
            ds.render()

    def play_btn_onreturn(self):
        self.start_the_game()

    def continue_btn_onreturn(self):
        self.start_copied_game()

    def update_continue_button(self):
        if self.subject_game.has_copy():
            self.continue_button.show()
        else:
            self.continue_button.hide()

    def update_subject_game_dropselect(self):
        self.subject_game_dropselect.update_items(
            [(g.name_t, index) for index, g in enumerate(self.subject.games)]
        )
        self.subject_game_dropselect.set_value(self.subject_game_index)

    def update_difficulty_dropselect(self):
        self.difficulty_dropselect.update_items(
            [
                (d, index)
                for index, d in enumerate(self.subject_game.difficulties)
            ]
        )
        self.difficulty_dropselect.set_value(self.difficulty_index)

    def update_help_label(self):
        self.help_label.set_title(self.subject_game.help_t.strip())
        self.help_label.set_background_color(self.help_label_bg)
        self.help_label.set_border(2, self.help_label_border_color)

    def start_copied_game(self):
        self.subject_game.load(self.ps)

    def start_the_game(self):
        self.subject_game.play(self.ps)

    def on_difficulty_dropselect_change(self, value, index):
        self.set_difficulty_index(index)

    def on_subject_dropselect_change(self, item, index):
        self.set_subject_index(index)

    def on_subject_game_dropselect_change(self, item, index):
        self.set_subject_game_index(index)

    def set_subject_index(self, index=0):
        self.subject_index = self.ps.subject_index = index
        self.subject = self.ps.subject = self.subjects[self.subject_index]
        self.subject_games = self.ps.subject_games = self.subject.games
        self.set_subject_game_index()
        self.update_subject_game_dropselect()
        self.update_selection_box_width()

    def set_subject_game_index(self, index=0):
        self.subject_game_index = self.ps.subject_game_index = index
        self.subject_game = self.ps.subject_game = self.subject.games[
            self.subject_game_index
        ]
        self.update_continue_button()
        self.set_difficulty_index()
        self.update_help_label()

    def set_difficulty_index(self, index=0):
        self.difficulty_index = self.ps.difficulty_index = (
            index if index != 0 else self.subject_game.default_difficulty_index
        )
        self.update_difficulty_dropselect()


class PrimarySchool:
    def __init__(
        self,
        surface=None,
        mode_flags=pygame.RESIZABLE,
        player_name=None,
        caption=_("PrimarySchool"),
        show_play_menu=True,
    ):
        if not pygame.get_init():
            pygame.init()
        self.show_play_menu = show_play_menu
        self.caption = caption
        pygame.display.set_caption(self.caption)
        self.running = True
        self.surface = (
            surface
            or getattr(self, "surface", None)
            or pygame.display.set_mode((0, 0), mode_flags)
        )
        self.w_width, self.w_height = self.surface.get_size()
        self.w_width_of_2 = self.w_width / 2
        self.w_height_of_2 = self.w_height / 2
        self.w_centrex_y = [self.w_width_of_2, self.w_height]
        self.FPS = 30
        self.player_name = player_name or _("default_name")
        self.clock = pygame.time.Clock()
        self.subjects = subjects
        self.subject_games = self.subjects[0].games
        self.subject_index = 0
        self.subject_game_index = 0
        self.difficulty_index = 0
        self.subject = self.subjects[0]
        self.subject_game = self.subject_games[0]
        self.font_path = default_font_path
        self.font = default_font
        self.bg_img = None
        self.play_menu = PlayMenu(self)
        self.save_menu = SaveMenu(self)
        self.score_menu = ScoreMenu(self)

    def set_player_name(self, name):
        self.player_name = name

    def get_player_name(self):
        return self.player_name

    def sys_exit(self):
        sys.exit(0)

    def add_widgets(self):
        self.play_menu.add_widgets()
        self.save_menu.add_widgets()
        self.score_menu.add_widgets()

    def set_bg_img(self, src_name="0x1.png"):
        self.bg_img = BaseImage(
            get_resource_path(src_name), pygame_menu.baseimage.IMAGE_MODE_FILL
        )

    def get_bg_img(self):
        if not self.bg_img:
            self.set_bg_img()
        return self.bg_img

    def get_default_menu(self, title, **kwargs):
        theme = pygame_menu.themes.THEME_BLUE.copy()
        theme.title_font = theme.widget_font = self.font
        theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        theme.background_color = self.get_bg_img()
        return pygame_menu.Menu(
            title, self.w_width, self.w_height, theme=theme, **kwargs
        )

    def clear_screen(self):
        self.surface.fill((255, 255, 255))
        pygame.display.update()

    def run(self):

        self.add_widgets()

        while self.running:
            self.clock.tick(self.FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            if self.show_play_menu:
                if self.play_menu._menu.is_enabled():
                    self.play_menu._menu.mainloop(self.surface)

            pygame.display.flip()


def go():
    psready = PSReady()
    psready.get_input()
    PrimarySchool(player_name=psready.player_name).run()
