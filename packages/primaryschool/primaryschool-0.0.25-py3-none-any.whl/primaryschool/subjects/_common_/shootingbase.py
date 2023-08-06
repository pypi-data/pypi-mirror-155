import copy
import os
import pickle
import random
import sys
from datetime import datetime, timedelta
from operator import *
from typing import Any, List, Optional, Sequence, Text, Tuple, Union, overload

import pygame
import pygame_menu
from pygame.locals import *

from primaryschool.dirs import *
from primaryschool.locale import _, sys_lang_code
from primaryschool.resource import (
    default_font,
    default_font_path,
    get_default_font,
    get_font_path,
    get_sys_font_by_lang_code,
)
from primaryschool.subjects import *
from primaryschool.subjects._abc_ import GameBase
from primaryschool.subjects._common_.keycode import PsKeyCode
from primaryschool.subjects._common_.media import *


class ShootingWave:
    def __init__(self, _manager):

        self.manager = _manager
        self.shtbase = self.manager.shtbase
        self.ps = self.shtbase.ps
        self.intercept_interval = self.manager.intercept_interval
        self.surface = self.shtbase.surface
        self.w_height = self.shtbase.w_height
        self.w_height_of_2 = self.shtbase.w_height_of_2
        self.w_width_of_2 = self.shtbase.w_width_of_2
        self.w_centrex_y = self.shtbase.w_centrex_y
        self.color = (0, 255, 0, 20)
        self.width = 5

        self.max_radius = self.get_max_radius()

    def set_color(self, color):
        self.color = color

    def get_max_radius(self):
        return (self.w_height**2 + self.w_width_of_2**2) ** 0.5

    def set_width(self, width):
        assert isinstance(width, int)
        self.width = widgets

    def draw(self, frame_counter):
        if frame_counter >= self.intercept_interval:
            return
        _radius = self.max_radius / (self.intercept_interval - frame_counter)
        pygame.draw.circle(
            self.surface,
            self.color,
            self.w_centrex_y,
            _radius,
            width=self.width,
        )


class TargetSurface:
    def __init__(
        self,
        shtbase,
        _manager,
        tkeys,
        tlock,
        dest=None,
        end_pos=None,
        key_lock_ignore_case=True,
    ):
        self.shtbase = shtbase
        self.key_lock_ignore_case = key_lock_ignore_case
        self.ps = self.shtbase.ps
        self.FPS = self.ps.FPS
        self.manager = _manager
        self.intercept_chr = self.manager.intercept_keycode and chr(
            self.manager.intercept_keycode
        )
        self.moving_speed = self.manager.moving_speed
        self.defense_surface = None
        self.tlock = tlock
        self.tkeys = (
            [k.lower() for k in tkeys] if self.key_lock_ignore_case else tkeys
        )
        self.font_color = (200, 22, 98)
        self.font = self.manager.font
        self.circle_color = (100, 20, 25, 20)
        self.circle_width = 4
        self.intercepted = False
        self.intercept_frame_counter = 0
        self.laser_color = self.manager.laser_color
        self.laser_width = self.manager.laser_width
        self.surface = self.get_surface()
        self.size = self.get_size()
        self.start_pos = self.dest = dest if dest else self.get_default_pos()
        self.end_pos = end_pos if end_pos else self.get_default_end_pos()
        self.moving_counter = 0
        self.center = self.get_center()
        self.bg_color = (20, 10, 200, 100)

    def set_dest(self, dest):
        self.dest = dest

    def set_start_pos(self, pos, reset_dest=False):
        self.start_pos = pos
        if reset_dest:
            self.dest = self.start_pos

    def set_end_pos(self, pos):
        self.end_pos = pos

    def get_default_pos(self):
        return self.get_random_dest_top()

    def get_default_end_pos(self):
        return (None, self.shtbase.w_height - self.shtbase.defense_surface.h)

    def set_circle_color(self, color):
        self.circle_color = color

    def set_circle_width(self, width):
        assert isinstance(width, int)
        self.circle_width = width

    def arrived(self):
        if self.end_pos[0]:
            return self.get_x() + self.get_w() >= self.end_pos[0]
        if self.end_pos[1]:
            return self.get_y() + self.get_h() >= self.end_pos[1]

    def get_surface(self):
        return self.font.render(self.tlock, False, self.font_color)

    def get_x(self):
        return self.dest[0]

    def get_y(self):
        return self.dest[1]

    def get_w(self):
        return self.size[0]

    def get_h(self):
        return self.size[1]

    def get_default_bg_points(self, tip_height=55):
        return [
            (self.get_x(), self.get_y()),
            (self.get_x() + self.get_w(), self.get_y()),
            (self.get_x() + self.get_w(), self.get_y() + self.get_h()),
            (
                self.get_x() + self.get_w() / 2,
                self.get_y() + self.get_h() + tip_height,
            ),
            (self.get_x(), self.get_y() + self.get_h()),
        ]

    def draw_bg(self):
        pygame.draw.polygon(
            self.ps.surface, self.bg_color, self.get_default_bg_points()
        )

    def calc_dest(self, _add):
        return

    def move(self, _add=(1, 1), rel=True, use_func=False):

        if use_func:
            self.dest = self.calc_dest(_add)
        elif rel:
            self.dest[0] += _add[0]
            self.dest[1] += _add[1]
        else:
            self.set_dest(_add)
        self.center = self.get_center()
        self.draw_bg()

    def set_laser_color(self, laser_color):
        self.laser_color = laser_color

    def get_laser_color():
        return self.laser_color

    def draw_laser_line(self):
        if self.defense_surface is None:
            self.defense_surface = self.shtbase.defense_surface
        assert self.defense_surface is not None
        pygame.draw.line(
            self.ps.surface,
            self.laser_color,
            self.defense_surface.center,
            self.center,
            self.laser_width,
        )

    def get_center(self):
        return [
            self.get_x() + self.get_w() / 2,
            self.get_y() + self.get_h() / 2,
        ]

    def get_circle_radius(self):
        return self.get_w() / 2

    def circle(self):
        pygame.draw.circle(
            self.shtbase.surface,
            self.circle_color,
            self.center,
            self.get_circle_radius(),
            width=self.circle_width,
        )

    def intercept(self, _result, ignore_case=True):
        if len(_result) < 1:
            return self.intercepted

        if self.intercept_chr is None or _result.endswith(self.intercept_chr):

            if self.intercept_chr:
                _result = _result.replace(self.intercept_chr, "").strip()
            else:
                _result = _result.strip()

            self.intercepted = _result.lower() in self.tkeys

        return self.intercepted

    def get_size(self):
        return self.surface.get_size()

    def set_random_dest_top(self):
        self.dest = self.get_random_dest_top()

    def get_random_dest_top(self):
        return [random.randint(0, self.shtbase.w_width - self.get_w()), 0]

    def copy(self):
        _new = copy.copy(self)
        _new.surface = self.surface.copy()
        _new.set_random_dest_top()
        return _new


class TargetsManager:
    def __init__(
        self,
        shtbase,
        frame_counter=None,
        lang_code=None,
        intercept_keycode=None,
    ):

        self.shtbase = shtbase
        self.ps = self.shtbase.ps
        self.FPS = self.ps.FPS
        self.moving_surfaces = []
        self.frame_counter = frame_counter or 30
        self.difficulty_index_p1 = self.shtbase.difficulty_index + 1
        self.interval = 2.0 * self.shtbase.FPS
        self.intercept_interval = 0.3 * self.shtbase.FPS
        self.moving_speed = (0, 0.6)
        self.intercepted_color = (175, 10, 175, 100)
        self.laser_color = (0, 0, 255, 90)
        self.laser_width = 2
        self.font_size = 50
        self.lang_code = lang_code or sys_lang_code
        self.font_path = get_font_path(self.lang_code)
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.surfaces = []
        self.intercept_keycode = intercept_keycode
        self.target_count = 20

    def set_moving_speed(self, speed=(0, 1)):
        """
        The number of pixels moved per frame.
        """
        self.moving_speed = speed

    def get_moving_speed(self):
        return self.moving_speed

    def set_interval(self, interval=1.8):
        """
        interval: The time interval at which the target appears, in seconds.
        """
        self.interval = interval * self.shtbase.FPS

    def get_interval(self):
        return self.interval

    def set_intercept_keycode(self, Pskeycode):
        self.intercept_keycode = keycode

    def get_targets(self, d: int = 0, count=20):
        """
        return [(key,key,key,key,...,lock)]
        """
        raise NotImplementedError()

    def save(self, _copy):
        _copy["0x0"] = [(s.tkeys, s.tlock, s.dest) for s in self.surfaces]
        _copy["0x1"] = [
            (ms.tkeys, ms.tlock, ms.dest) for ms in self.moving_surfaces
        ]
        return _copy

    def set_all_surfaces_none(self):
        self.surfaces = self.moving_surfaces = []

    def load(self, _copy):
        self.set_all_surfaces_none()
        for keys, lock, dest in _copy["0x0"]:
            self.surfaces.append(TargetSurface(self.shtbase, self, keys, lock))
        for keys, lock, dest in _copy["0x1"]:
            self.moving_surfaces.append(
                TargetSurface(self.shtbase, self, keys, lock, dest)
            )

    def set_lang_code(self, lang_code):
        self.lang_code = lang_code

    def set_target_count(self, target_count):
        self.target_count = target_count
        self.shtbase.set_target_count(target_count)

    def moving_surfaces_blit(self):
        pass

    def set_font_size(self, size):
        assert isinstance(size, int)
        self.font_size = size

    def get_font_size(self):
        return self.font_size

    def get_target_surfaces(self):
        _targets = self.get_targets(self.shtbase.difficulty_index)
        self.set_target_count(len(_targets))

        return [
            TargetSurface(self.shtbase, self, t[0:-1], t[-1]) for t in _targets
        ]

    def set_surfaces(self):
        self.surfaces = self.get_target_surfaces()
        self.set_target_count(len(self.surfaces))

    def get_surfaces(self):
        if not self.surfaces:
            self.set_surfaces()
        return self.surfaces

    def count(self):
        return len(self.surfaces)

    def get_random_surface(self):
        random_ws = self.surfaces[random.randint(0, self.count - 1)]
        return random_ws.copy()

    def pop_surface(self):
        return self.surfaces.pop()

    def add_moving_surfaces(self):
        ws = self.pop_surface()
        self.moving_surfaces.append(ws)
        self.frame_counter = 0

    def blit_intercepting(self, moving_surfaces):
        pass

    def blit(self):
        if len(self.surfaces) > 0:
            if len(self.moving_surfaces) < 1:
                self.add_moving_surfaces()
            if self.frame_counter >= self.interval:
                self.add_moving_surfaces()

        for w in self.moving_surfaces:
            if w.intercepted:
                if w.intercept_frame_counter >= self.intercept_interval:
                    self.moving_surfaces.remove(w)
                self.blit_intercepting(w)
                w.surface = w.font.render(
                    w.tlock, False, self.intercepted_color
                )
                self.shtbase.surface.blit(w.surface, w.dest)
                w.circle()
                w.draw_laser_line()
                w.intercept_frame_counter += 1
                continue

            if w.intercept(self.shtbase._input):
                self.shtbase._input = ""
                self.shtbase.input_surface._update()
                self.shtbase.surface.blit(w.surface, w.dest)
                self.shtbase.win_count += 1
                continue

            if w.arrived():
                if self.shtbase.defense_surface.flicker() < 1:
                    self.moving_surfaces.remove(w)
                    self.shtbase.lose_count += 1
                    continue

            w.move(self.moving_speed)
            self.shtbase.surface.blit(w.surface, w.dest)
            self.moving_surfaces_blit()

        self.frame_counter += 1


class InputSurface:
    def __init__(
        self,
        shtbase,
        font_lang_code=None,
        font_bold=False,
        border_radius=5,
        border_width=1,
        border_color=(200, 20, 30, 60),
    ):

        self.shtbase = shtbase
        self.ps = self.shtbase.ps
        self.font_size = 55
        self.font_lang_code = font_lang_code or self.shtbase.font_lang_code
        self.font = (
            get_sys_font_by_lang_code(self.font_lang_code)
            if self.font_lang_code
            else get_default_font(self.font_size)
        )
        self.font_color = (200, 22, 98)
        self.surface = None
        self.frame_counter = 0
        self.x, self.y = self.dest = (0, 0)
        self.w, self.h = self.rect = (0, 0)
        self.border_radius = border_radius
        self.border_width = border_width
        self.border_color = border_color
        self.font_bold = font_bold

        self.font.set_bold(self.font_bold)

    def set_rect(self, rect=None):
        self.update_rect(rect)

    def update_rect(self, rect=None):
        self.w, self.h = self.rect = rect or self.surface.get_size()

    def update_dest(self, dest=None):
        self.x, self.y = self.dest = dest or (
            self.shtbase.w_width_of_2 - self.w / 2,
            self.shtbase.w_height - self.h,
        )

    def get_input(self, strip=True):
        _input = self.shtbase._input
        if strip:
            return _input.strip()
        else:
            return _input

    def set_input(self, input_str):
        self.shtbase._input = input_str

    def _update(self, _input=None):
        _input = _input or self.get_input()
        self.surface = self.font.render(_input, False, self.font_color)

    def _blit(self):
        pygame.draw.rect(
            self.shtbase.surface,
            color=self.border_color,
            rect=(self.x, self.y, self.w, self.h),
            width=self.border_width,
            border_radius=self.border_radius,
        )

    def blit(self):
        if self.surface is None:
            return

        self.update_rect()
        self.update_dest()
        self._blit()

        self.shtbase.surface.blit(self.surface, self.dest)


class DefenseSurface:
    def __init__(self, shtbase, original_color=None):
        self.shtbase = shtbase
        self.ps = self.shtbase.ps
        self.h = self.shtbase.w_height / 20
        self.surface = pygame.Surface((self.shtbase.w_width, self.h))
        self.original_color = original_color or self.get_default_color()
        self.color = self.original_color
        self.emitter_radius = self.h / 2
        self.emitter_color = None

        self.flicker_interval = 1 * self.ps.FPS  # 2s
        self.flicker_counter = 0
        self.flicker_color = [self.color, (250, 0, 0)]
        self.flicker_color_step = (
            (self.flicker_color[1][0] - self.flicker_color[0][0])
            / self.flicker_interval,
            (self.flicker_color[1][1] - self.flicker_color[0][1])
            / self.flicker_interval,
            (self.flicker_color[1][2] - self.flicker_color[0][2])
            / self.flicker_interval,
        )

        self.center = self.get_center()

    def get_default_color(self):
        return (10, 200, 99)

    def flicker(self):
        self.flicker_counter += 1
        self.color = (
            min(
                int(
                    self.flicker_color[0][0]
                    + self.flicker_color_step[0] * self.flicker_counter
                ),
                255,
            ),
            min(
                int(
                    self.flicker_color[0][1]
                    + self.flicker_color_step[1] * self.flicker_counter
                ),
                255,
            ),
            min(
                int(
                    self.flicker_color[0][2]
                    + self.flicker_color_step[2] * self.flicker_counter
                ),
                255,
            ),
        )
        if self.flicker_counter >= self.flicker_interval:
            self.flicker_counter = 0
            self.color = self.original_color
        return self.flicker_counter

    def set_emitter_color(self, color=(255, 0, 0, 50)):
        self.emitter_color = color

    def get_emitter_color(self):
        return self.emitter_color

    def get_center(self):
        return [self.ps.w_width_of_2, self.ps.w_height - self.h / 2]

    def draw_emitter(self):
        self.emitter_color = (
            self.set_emitter_color()
            if self.shtbase.targets_manager is None
            else self.shtbase.targets_manager.laser_color
        )
        pygame.draw.circle(
            self.ps.surface,
            self.emitter_color,
            self.center,
            self.emitter_radius,
        )

    def blit(self):
        self.surface.fill(self.color)
        self.shtbase.surface.blit(
            self.surface, (0, self.shtbase.w_height - self.h)
        )
        self.draw_emitter()


class InfoSurface:
    def __init__(self, shtbase):
        self.shtbase = shtbase
        self.ps = shtbase.ps
        self.surface = self.ps.surface
        self.game_info_dest = (10, 10)
        self.game_info = (
            self.shtbase.name_t
            + "/"
            + self.shtbase.difficulties[self.ps.difficulty_index]
        )
        self.game_info_color = (255, 0, 255, 10)
        self.font_size = 25
        self.font = get_default_font(self.font_size)

        self.font = get_default_font(self.font_size)

        self.game_info_surface = self.font.render(
            self.game_info, False, self.game_info_color
        )

    def get_win_info(self):
        return (
            "|"
            + _("win: ")
            + str(self.shtbase.win_count)
            + "|"
            + _("lose: ")
            + str(self.shtbase.lose_count)
            + "|"
            + _("remain: ")
            + str(self.shtbase.targets_manager.count())
            + "|"
            + _("total: ")
            + str(self.shtbase.target_count)
            + "|"
        )

    def get_win_info_dest(self):
        _w, _ = self.win_info_surface.get_size()
        return [self.ps.w_width - _w, 0]

    def blit(self):
        self.win_info_surface = self.font.render(
            self.get_win_info(), False, self.game_info_color
        )

        self.surface.blit(self.game_info_surface, self.game_info_dest)
        self.surface.blit(self.win_info_surface, self.get_win_info_dest())


class ShootingBase(GameBase, PsKeyCode):
    def __init__(self, ps, font_lang_code=None):
        assert hasattr(self, "name_t")
        assert hasattr(self, "difficulties")
        assert hasattr(self, "module_str")

        self.ps = ps
        # window
        self.w_width = self.ps.w_width
        self.w_height = self.ps.w_height
        self.w_height_of_2 = self.ps.w_height_of_2
        self.w_width_of_2 = self.ps.w_width_of_2
        self.w_centrex_y = self.ps.w_centrex_y
        self.running = True
        self.FPS = self.ps.FPS
        self.clock = self.ps.clock
        self.player_name = self.ps.player_name
        self._load = False

        self._pass_value = 60

        self.font_lang_code = font_lang_code or sys_lang_code

        self.subject = self.ps.subject
        self.subject_index = self.ps.subject_index
        self.subject_game_index = self.ps.subject_game_index
        self.difficulty_index = self.ps.difficulty_index

        self.play_menu = self.ps.play_menu
        self.save_menu = self.ps.save_menu
        self.score_menu = self.ps.score_menu
        self.surface = self.ps.surface

        self._input = ""
        self.font = get_sys_font_by_lang_code(self.font_lang_code, 45)
        self.info_surface = self.get_info_surface()
        self.defense_surface = self.get_defense_surface()
        self.input_surface = self.get_input_surface()
        self.copy_path = get_copy_path(self.module_str)

        self.last_timedelta = timedelta(0)
        self.start_time = datetime.now()
        self.end_time = None

        self.targets_manager = self.get_targets_manager()
        self.win_count = 0
        self.lose_count = 0
        self.target_count = 0
        self.score = 0
        self.print_game_info()
        self.screenshot_path = get_default_screenshot_path(
            self.module_str, self.ps.player_name
        )

    def get_screenshot_path(self):
        return self.screenshot_path

    def set_screenshot_path(self, path):
        self.screenshot_path = path

    def set_pass_value(self, value=60):
        self._pass_value = value

    def get_pass_value(self):
        return self._pass_value

    def set_score_surface(self, score_surface=None):
        self.score_surface = score_surface or ScoreSurface(self)

    def get_score_surface(self):
        score_surface = (
            hasattr(self, "score_surface")
            and self.score_surface
            or ScoreSurface(self)
        )
        return score_surface

    def get_player_name(self):
        return self.player_name

    def set_player_name(self, name):
        self.player_name = self.ps.player_name = name

    def set_input(self, content=""):
        self._input = content

    def set_font_lang_code(self, font_lang_code):
        self.font_lang_code = font_lang_code
        self.font = get_sys_font_by_lang_code(self.font_lang_code, 45)

    def get_info_surface(self):
        return InfoSurface(self)

    def get_input_surface(self):
        return InputSurface(self)

    def get_defense_surface(self):
        return DefenseSurface(self)

    def get_targets_manager(self):
        raise NotImplementedError()

    def set_target_count(self, count):
        self.target_count = count

    def print_game_info(self):
        print(
            self.subject.name_t,
            self.name_t,
            self.difficulties[self.difficulty_index],
        )

    def key_clean(self, code):
        return 48 <= code <= 57 or code == 45

    def copy_time(self, _copy, save=False, key="0x3"):
        _copy[key] = (datetime.now() - self.start_time) + self.last_timedelta
        if save:
            with open(self.copy_path, "wb") as f:
                pickle.dump(_copy, f)

    def get_prev_time(self, _copy=None, key="0x3"):
        if not _copy:
            with open(self.copy_path, "rb") as f:
                _copy = pickle.load(f)
        return _copy[key]

    def load(self):
        try:
            self._load = True
            with open(self.copy_path, "rb") as f:
                _copy = pickle.load(f)
            self.targets_manager.load(_copy)
            self.target_count, self.win_count, self.lose_count = _copy["0x2"]
            self.last_timedelta = self.get_prev_time(_copy)
            self.start()
        except Exception as e:
            print(e)

    def save(self):
        _copy = {}
        self.targets_manager.save(_copy)
        _copy["0x2"] = (self.target_count, self.win_count, self.lose_count)
        self.copy_time(_copy)

        # https://docs.python.org/3/library/pickle.html?highlight=pickle
        # Warning:
        # The pickle module is not secure. Only unpickle data you trust.
        with open(self.copy_path, "wb") as f:
            pickle.dump(_copy, f)

    def _start(self):
        if not self._load:
            self.targets_manager.set_surfaces()

    def play(self):
        self._load = False
        self.targets_manager.surfaces = []
        self.targets_manager.moving_surfaces = []
        self.targets_manager.set_surfaces()
        self.start()

    def get_score(self):
        self.score = int(100 * self.win_count / self.target_count)
        return self.score

    def get_pass(self):
        return self.score >= self._pass_value

    def get_cost_str(self):
        if not self.end_time:
            self.end_time = self.ps.end_time = datetime.now()
        diff = self.end_time - self.start_time + self.last_timedelta
        _h, _rem = divmod(diff.seconds, 3600)
        _min, _sec = divmod(_rem, 60)
        return f"{_h}:{_min}:{_sec}"

    def all_targets_gone(self):
        return self.win_count + self.lose_count >= self.target_count

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.save_menu._menu.enable()
                    self.last_timedelta += datetime.now() - self.start_time
                    self.save_menu._menu.mainloop(self.surface)
                    self.start_time = datetime.now()
                    return
                elif e.key == pygame.K_BACKSPACE:
                    self._input = self._input[0:-1]
                    self.input_surface._update()
                    return
                elif self.key_clean(e.key):
                    self._input += chr(e.key)
                    self.input_surface._update()
                    return

    def start(self):

        self._start()

        while self.running:
            self.clock.tick(self.FPS)

            self.surface.fill((0, 0, 0))

            events = pygame.event.get()
            self.handle_events(events)

            if self.play_menu._menu.is_enabled():
                self.play_menu._menu.update(events)

            if self.all_targets_gone():
                self.score_menu.update_widgets(
                    score=self.get_score(),
                    _pass=self.get_pass(),
                    cost_str=self.get_cost_str(),
                    screenshot_path=self.get_screenshot_path(),
                )
                self.score_menu._menu.enable()
                self.score_menu._menu.update(events)
                self.score_menu._menu.mainloop(self.surface)
            else:
                self.info_surface.blit()
                self.defense_surface.blit()
                self.targets_manager.blit()
                self.input_surface.blit()

            pygame.display.update()
