
from __future__ import annotations

from structs.vector import Vector
from engine.objects.base import BaseObject
from engine.objects.component import Component

import typing

if typing.TYPE_CHECKING:
    from engine.game.scene import Scene


class Entity(BaseObject):
    """
    An Entity is a game object that is composed of multiple components.
    """

    def __init__(self, pos: tuple = (0, 0), *args, **kwargs):
        """Spawns an entity.

        Args:
            pos (tuple, optional): the position to spawn this entity

        """
        super().__init__(pos=pos)

        self.root_component: Component = Component()

    # --------------------------------------------------------------------------
    # Events (to be overridden by subclasses)
    # --------------------------------------------------------------------------

    def on_key_press(self, symbol, modifier):
        """Called every time a key is pressed."""
        pass

    def on_key_release(self, symbol, modifier):
        """Called every time a key was released."""
        pass
