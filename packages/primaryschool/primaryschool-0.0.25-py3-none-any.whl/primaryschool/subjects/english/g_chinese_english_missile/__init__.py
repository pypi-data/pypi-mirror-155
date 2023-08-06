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
from primaryschool.subjects.english.g_chinese_english_missile.words import (
    cn_ps_e_words,
)

# primaryschool.subjects.yuwen.g_pinyin_missile
module_str = __name__

name_t = _("Chinese-English Missile")

difficulties = [
    _("Grade 3.1"),  # 0
    _("Grade 3.2"),  # 1
    _("Grade 4.1"),  # 2
    _("Grade 4.2"),  # 3
    _("Grade 5.1"),  # 4
    _("Grade 5.2"),  # 5
    _("Grade 6.1"),  # 6
    _("Grade 6.2"),  # 7
    _("All grades"),  # 8
]


help_t = _(
    """
Enter the corresponding words of the Chinese characters.
"""
)


class ZhCNEmTargetsManager(TargetsManager):
    def __init__(self, shtbase):
        super().__init__(shtbase, lang_code="zh_CN")
        self.wave = ShootingWave(self)

    def blit_intercepting(self, moving_surfaces):
        self.wave.draw(moving_surfaces.intercept_frame_counter)

    def get_cn_ps_e_words(self, g_index: int):
        words = []
        if g_index < 8:
            words = cn_ps_e_words[g_index]
        elif g_index == 8:
            words = sum(cn_ps_e_words, [])
        return sum(words, [])

    def get_targets(self, d: int = 0, count=30):
        return self.get_cn_ps_e_words(d)


class ZhCNEnglishMissile(ShootingBase):
    def __init__(self, ps):
        self.name_t = name_t
        self.difficulties = difficulties
        self.module_str = module_str
        super().__init__(ps)

    def get_targets_manager(self):
        return ZhCNEmTargetsManager(self)

    def key_clean(self, code):
        return (
            self.keycode_in_pure_num(code)
            or self.keycode_in_alpha(code)
            or self.keycode_in_space(code)
            or self.keycode_in_hyphen(code)
        )


def enjoy(ps):
    return ZhCNEnglishMissile(ps)
