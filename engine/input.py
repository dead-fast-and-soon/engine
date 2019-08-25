
from __future__ import annotations

import pyglet
import typing


class Input:
    """A wrapper for the KeyStateHandler class provided by Pyglet."""

    def __init__(self):
        self.keys: typing.Dict = {}

    def __getitem__(self, key):
        return self.keys.get(key, False)

    def __setitem__(self, key, value):
        self.keys[key] = value
