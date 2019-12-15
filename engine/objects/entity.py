
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

    def __init__(self, scene: Scene, pos: tuple = (0, 0),
                 *args, **kwargs):
        """Spawns an entity.

        Args:
            pos (tuple, optional): the position to spawn this entity

        """
        super().__init__(pos=pos)

        # the Scene that spawned this entity
        self.scene: Scene = scene

        # the root Component of this entity
        self.root_component: Component = Component(pos=pos)

    # --------------------------------------------------------------------------
    # Events (to be overridden by subclasses)
    # --------------------------------------------------------------------------

    @BaseObject.property.getter  # type: ignore
    def position(self) -> Vector:
        return self.root_component.position

    @BaseObject.property.setter  # type: ignore
    def position(self, pos: tuple):
        self.root_component.position = pos

    def on_key_press(self, symbol, modifier):
        """Called every time a key is pressed."""
        pass

    def on_key_release(self, symbol, modifier):
        """Called every time a key was released."""
        pass

    def on_update(self, delta: float):
        """
        Called every tick.

        Args:
            delta (float): the difference in time from the last tick
        """
        pass
