
from __future__ import annotations

import typing


class InputHandler:

    def __init__(self):
        """
        Create an input handler.
        """
        self._keys = [False for i in range(65520)]

    def __getitem__(self, key: int):

        return self._keys[key]

    def set_key(self, key: int, state: bool):

        self._keys[key] = state
