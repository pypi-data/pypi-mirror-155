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
)
from primaryschool.subjects import *
from primaryschool.subjects._abc_ import GameBase
from primaryschool.subjects._common_.shootingbase import *

# primaryschool.subjects.yuwen.g_mind_hunter
module_str = __name__

name_t = _("Mind hunter")

difficulties = [
    _("< 10 + 10"),  # 0
    _("< 50 + 50"),  # 1
    _("< 100 + 100"),  # 2
    _("< 10 - 10"),  # 3
    _("< 50 - 50"),  # 4
    _("< 100 - 100"),  # 5
    _("< 10 * 10"),  # 6
    _("< 50 * 50"),  # 7
    _("< 100 * 100"),  # 8
    _("< 10 / 10"),  # 9
    _("< 50 / 50"),  # 10
    _("< 100 / 100"),  # 11
    _("< 10 ? 10"),  # 12
    _("< 50 ? 50"),  # 13
    _("< 100 ? 100"),  # 14
]


help_t = _(
    """
Enter the calculation result, press Enter to confirm.
"""
)

times_sign = "\u00d7"
division_sign = "\u00f7"


class MhTargetsManager(TargetsManager):
    def __init__(self, shtbase):
        super().__init__(shtbase, intercept_keycode=0xD)
        self.wave = ShootingWave(self)

    def get_pmt_formulas(self, _max, _oper, count=None):  # for plus/minus/time
        f = []
        count = count if count else self.target_count
        _max_sqrt = int(_max**0.5)
        for _ in range(self.target_count + 1):
            _oper_ = random.choice(_oper) if isinstance(_oper, list) else _oper
            num0 = random.randint(0, _max)
            num1 = random.randint(0, _max)
            if _oper_ == "-":
                num0 = max(num0, num1)
                num1 = min(num0, num1)
            if _oper_ == times_sign:
                num0 = random.randint(0, _max_sqrt)
                num1 = random.randint(0, _max_sqrt)
            f.append(str(num0) + " " + _oper_ + " " + str(num1))

        return f

    def blit_intercepting(self, moving_surfaces):
        self.wave.draw(moving_surfaces.intercept_frame_counter)

    def get_division_formulas(self, _max, count=None):
        _d = []
        count = count if count else self.target_count
        for i in range(_max + 1):
            for j in range(1, _max + 1):
                if i % j == 0:
                    _d.append((i, j))
        return [
            str(a) + " " + division_sign + " " + str(b)
            for a, b in random.choices(_d, k=self.target_count)
        ]

    def get_result(self, formula):
        a, oper, b = formula.split(" ")
        return str(
            int(a) + int(b)
            if oper == "+"
            else int(a) - int(b)
            if oper == "-"
            else int(a) * int(b)
            if oper == times_sign
            else int(int(a) / int(b))
        )

    def get_targets(self, d: int = 0, count=20):
        formulas = None
        if d < 15:
            _rem, _quo = d % 3, d // 3
            _max = 10 if _rem == 0 else 50 if _rem == 1 else 100
            _oper = (
                "+"
                if _quo == 0
                else "-"
                if _quo == 1
                else times_sign
                if _quo == 2
                else division_sign
                if _quo == 3
                else "?"
            )
            if _oper in ["+", "-", times_sign]:
                formulas = self.get_pmt_formulas(_max, _oper)
            elif _oper == division_sign:
                formulas = self.get_division_formulas(_max)
            else:  # ?
                _d_opers_count = random.choices(
                    ["+", "-", times_sign, division_sign], k=self.target_count
                ).count(division_sign)
                formulas = self.get_pmt_formulas(
                    _max, ["+", "-", times_sign]
                ) + self.get_division_formulas(_max, _d_opers_count)

            return [(self.get_result(f), f) for f in formulas]


class MindHunter(ShootingBase):
    def __init__(self, ps):
        self.name_t = name_t
        self.difficulties = difficulties
        self.module_str = module_str
        super().__init__(ps)

    def get_targets_manager(self):
        return MhTargetsManager(self)

    def key_clean(self, code):
        return self.keycode_in_return(code) or self.keycode_in_num(code)


def enjoy(ps):
    return MindHunter(ps)
