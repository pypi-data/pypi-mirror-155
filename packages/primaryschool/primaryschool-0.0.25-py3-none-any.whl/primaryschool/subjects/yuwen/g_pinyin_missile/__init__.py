import copy
import os
import pickle
import random
import sys
from datetime import datetime, timedelta
from typing import Any, List, Optional, Sequence, Text, Tuple, Union, overload

import pygame
import pygame_menu
from pygame.locals import *
from xpinyin import Pinyin

from primaryschool.dirs import *
from primaryschool.locale import _
from primaryschool.resource import (
    default_font,
    default_font_path,
    get_default_font,
    get_font_path,
    get_resource_path,
)
from primaryschool.subjects import *
from primaryschool.subjects._abc_ import GameBase
from primaryschool.subjects._common_.shootingbase import *
from primaryschool.subjects.yuwen.words import cn_ps_c, cn_ps_c_bb
from primaryschool.subjects.yuwen.yumu import p_a, p_e, p_i, p_o, p_u, p_v

# primaryschool.subjects.yuwen.g_pinyin_missile
module_str = __name__

name_t = _("Pinyin Missile")
default_difficulty_index = 16
difficulties = [
    _("Grade 1.1"),  # 0
    _("Grade 1.2"),  # 1
    _("Grade 2.1"),  # 2
    _("Grade 2.2"),  # 3
    _("Grade 3.1"),  # 4
    _("Grade 3.2"),  # 5
    _("Grade 4.1"),  # 6
    _("Grade 4.2"),  # 7
    _("Grade 5.1"),  # 8
    _("Grade 5.2"),  # 9
    _("Grade 6.1"),  # 10
    _("Grade 6.2"),  # 11
    _("Low level"),  # 12
    _("High level"),  # 13
    _("All grades"),  # 14
    _("All Chinese characters"),  # 15
    _("Grade 1.1 (30 characters)"),  # 16
    _("Grade 1.2 (30 characters)"),  # 17
    _("Grade 2.1 (30 characters)"),  # 18
    _("Grade 2.2 (30 characters)"),  # 19
    _("Grade 3.1 (30 characters)"),  # 20
    _("Grade 3.2 (30 characters)"),  # 21
    _("Grade 4.1 (30 characters)"),  # 22
    _("Grade 4.2 (30 characters)"),  # 23
    _("Grade 5.1 (30 characters)"),  # 24
    _("Grade 5.2 (30 characters)"),  # 25
    _("Grade 6.1 (30 characters)"),  # 26
    _("Grade 6.2 (30 characters)"),  # 27
    _("Low level (30 characters)"),  # 28
    _("High level (30 characters)"),  # 29
    _("All grades (30 characters)"),  # 30
    _("All Chinese characters (30 characters)"),  # 31
]

help_t = _(
    """
Enter the pinyin corresponding to the Chinese character, and enter the number
after the pinyin to indicate the tone.
"""
)

pinyin = Pinyin()

cn_ps_chars = cn_ps_c_bb


class PmInputSurface(InputSurface):
    def __init__(
        self,
        shtbase,
        font_lang_code=None,
        font_bold=False,
        border_radius=5,
        border_width=1,
        border_color=(200, 20, 30, 60),
    ):
        super().__init__(
            shtbase,
            font_lang_code,
            font_bold,
            border_radius,
            border_width,
            border_color,
        )
        self.candidates = []
        self.p_a = p_a
        self.p_o = p_o
        self.p_e = p_e
        self.p_i = p_i
        self.p_u = p_u
        self.p_v = p_v
        self.aoeiuv = [
            self.p_a,
            self.p_o,
            self.p_e,
            self.p_i,
            self.p_u,
            self.p_v,
        ]

    def get_input(self):
        _input = super().get_input()
        _new_input = _input
        for yms in self.aoeiuv:
            if yms[0] in _input:
                for i, _ym in enumerate(yms[1:]):
                    _new_input += f"  ({i+1})" + _input.replace(yms[0], _ym)
                break
        return _input if _input == _new_input else "(0)" + _new_input


class PmTargetsManager(TargetsManager):
    def __init__(self, shtbase):
        super().__init__(shtbase, lang_code="zh_CN")
        self.wave = ShootingWave(self)
        self.set_interval(2)
        self.set_moving_speed((0, 0.7))

    def blit_intercepting(self, moving_surfaces):
        self.wave.draw(moving_surfaces.intercept_frame_counter)

    def get_targets(self, d: int = 0, count=30):

        targets = None
        _base_len = int(len(difficulties) / 2)
        g_index = d
        if g_index < _base_len:
            if g_index == _base_len - 1:
                targets = self.get_rand_words(self.rand_word_count)
            if 0 <= g_index < _base_len - 1:
                targets = self.get_cn_ps_words(g_index)
        else:
            g_index = g_index - _base_len
            if g_index == _base_len - 1:
                targets = random.choices(
                    self.get_rand_words(self.rand_word_count), k=30
                )
            if 0 <= g_index < _base_len - 1:
                targets = random.choices(self.get_cn_ps_words(g_index), k=30)

        _targets = []
        for t in targets:
            p = pinyin.get_pinyins(t, tone_marks="numbers")
            p.append(t)
            _targets.append(tuple(p))

        return _targets

    def get_cn_ps_words(self, g_index: int):
        words = []
        if g_index < 12:
            words = cn_ps_chars[g_index]
        elif g_index == 12:
            words = sum(cn_ps_chars[0:6], [])
        elif g_index == 13:
            words = sum(cn_ps_chars[6:16], [])
        elif g_index == 14:
            words = sum(cn_ps_chars[0:16], [])
        return sum(words, [])

    def get_rand_words(self, n):
        return [chr(random.randint(0x4E00, 0x9FBF)) for i in range(0, n)]


class PinyinMissile(ShootingBase):
    def __init__(self, ps):
        self.name_t = name_t
        self.difficulties = difficulties
        self.module_str = module_str
        super().__init__(ps)

    def get_targets_manager(self):
        return PmTargetsManager(self)

    def get_input_surface(self):
        return PmInputSurface(self)

    def key_clean(self, code):
        return self.keycode_in_pure_num(code) or self.keycode_in_alpha(code)


def enjoy(ps):
    return PinyinMissile(ps)
