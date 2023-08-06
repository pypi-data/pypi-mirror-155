import os
import sys
from importlib import import_module

from primaryschool.dirs import *
from primaryschool.locale import _

subject_module_prefix = "primaryschool.subjects."
subject_dir_path = os.path.abspath(os.path.dirname(__file__))

media_dir_path = os.path.join(subject_dir_path, "media")
img_dir_path = os.path.join(media_dir_path, "img")
default_game_image_path = os.path.join(img_dir_path, "0x2.png")
default_subject_image_path = os.path.join(img_dir_path, "0x3.png")


def game_is_valid(subject_name, game_name):
    return game_name.startswith("g_") and os.path.exists(
        os.path.join(subject_dir_path, subject_name, game_name, "__init__.py")
    )


def subject_is_valid(subject_path, subject):
    return (
        os.path.isdir(subject_path)
        and not subject.startswith("_")
        and not subject == "media"
    )


def get_subject_tree():
    subject_names = []
    game_modules = []

    for _subject in os.listdir(subject_dir_path):
        _subject_path = os.path.join(subject_dir_path, _subject)

        if not subject_is_valid(_subject_path, _subject):
            continue

        no_game = True
        for _game in os.listdir(_subject_path):
            if not game_is_valid(_subject, _game):
                continue
            no_game = False
            game_modules.append(subject_module_prefix + _subject + "." + _game)

        # Subject without game is ignored.
        if not no_game:
            subject_names.append(_subject)

    return subject_names, game_modules


subject_names, game_modules = get_subject_tree()


class Game:
    def __init__(self, module_str, subject, ps=None):
        self.module_str = module_str
        self.subject = subject
        self.ps = ps
        self.module = import_module(self.module_str)
        self._game = None
        self.name = self.module_str.split(".")[-1]
        self.name_t = getattr(self.module, "name_t")
        self.image_path = getattr(
            self.module, "image_path", default_game_image_path
        )
        self.help_t = getattr(self.module, "help_t")
        self.difficulties = getattr(self.module, "difficulties")
        self.default_difficulty_index = getattr(
            self.module, "default_difficulty_index", 0
        )

    def get_game(self, ps):
        assert ps
        if not self._game:
            self._game = self.module.enjoy(ps)
        return self._game

    def play(self, ps):
        assert ps
        ps.play_menu._menu.disable()
        ps.play_menu._menu.full_reset()
        self._game = None
        self.get_game(ps).play()

    def save(self, ps):
        assert ps
        self.get_game(ps).save()

    def load(self, ps):
        assert ps
        ps.play_menu._menu.disable()
        ps.play_menu._menu.full_reset()
        self.get_game(ps).load()

    def has_copy(self):
        return os.path.exists(get_copy_path(self.module_str))


class Subject:
    def __init__(self, name):
        self.name = name
        self.module = import_module(subject_module_prefix + self.name)
        self.name_t = self.module.name_t
        self.image_path = getattr(
            self.module, "image_path", default_subject_image_path
        )
        self.games = []

    def set_games(self):
        for g in game_modules:
            if g.startswith(subject_module_prefix + self.name):
                self.games.append(Game(g, self))

    def get_games(self):
        if len(self.games) < 1:
            self.set_games()
        return self.games

    def get_name_t(self):
        self.name_t = self.module.name_t
        return self.name_t


subjects = [Subject(n) for n in subject_names]


all_games = sum([s.get_games() for s in subjects], [])
