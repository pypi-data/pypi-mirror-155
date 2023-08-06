import os
import sys

import pygame

from primaryschool import project_path
from primaryschool.locale import _, sys_lang_code

resource_dir_path = os.path.abspath(os.path.dirname(__file__))
project_font_dir_path = os.path.join(resource_dir_path, "fonts")

pygame.font.init()


class Resource:
    def __init__(self):

        self.default_font_size = 50
        self.sys_font_names = pygame.font.get_fonts()
        self.locale_font_paths = self.get_locale_font_paths()
        self.resource_dir_names = ["imgs", "audios", "fonts"]
        self.resource_paths = self.get_resource_paths()

    def get_sys_font_name_like(self, _like_name):
        for f in self.sys_font_names:
            if _like_name.lower() in f.lower():
                return f
        return self.sys_font_names[0]

    def get_font_path(self, lang_code="", show_not_found=False):
        lang_code = sys_lang_code if len(lang_code) < 1 else lang_code
        for k, v in self.locale_font_paths.items():
            if lang_code == k:
                return v

        if show_not_found:
            from tkinter import Tk, messagebox

            root = Tk()
            messagebox.showerror(
                _("No font found"), _("Could not find font of %s.") % lang_code
            )
            root.destroy()

        return self.locale_font_paths["default"]

    def get_resource_paths(self):
        resource_paths = []
        for root, dirs, files in os.walk(resource_dir_path, topdown=False):
            for n in self.resource_dir_names:
                # imgs/xx_XX/xx.xx, for locale resources.
                if (root.endswith(n) or root.split(os.sep)[-2] == n) and len(
                    dirs
                ) < 1:
                    for name in files:
                        resource_paths.append(os.path.join(root, name))
        return sorted(resource_paths, key=len)

    def get_resource_path(self, name):
        assert os.sep not in name
        for f in self.resource_paths:
            if f.endswith(name):
                return f

    def get_locale_font_paths(self):
        return {
            "default": pygame.font.match_font(
                self.get_sys_font_name_like("mono")
            ),
            "zh_CN": pygame.font.match_font(
                self.get_sys_font_name_like(
                    sys.platform == "darwin"
                    and "heiti"
                    or sys.platform == "win32"
                    and "yahei"
                    or "cjk"
                )
            ),
        }


r = Resource()
default_font_path = r.get_font_path()


def get_default_font(size=None):
    return pygame.font.Font(default_font_path, size or r.default_font_size)


def get_font_path(lang_code, show_not_found=False):

    return r.get_font_path(lang_code, show_not_found)


def get_sys_font_by_lang_code(lang_code=None, size=None):

    size = size or r.default_font_size
    return (
        pygame.font.Font(get_font_path(lang_code), size)
        if lang_code
        else get_default_font()
    )


def get_resource_path(name):
    return r.get_resource_path(name)


default_font = get_default_font()
