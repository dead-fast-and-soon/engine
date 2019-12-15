
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

    def render(self, delta: float):
        """
        Render this Entity.

        Args:
            delta (float): [description]
        """
        self.root_component.render(delta)

    def update(self, delta: float):
        """
        Update this Entity.

        Args:
            delta (float): [description]
        """
        self.on_update(delta)
        self.root_component.update(delta)

    # --------------------------------------------------------------------------
    # Events (to be overridden by subclasses)
    # --------------------------------------------------------------------------

    @BaseObject.position.getter  # type: ignore
    def position(self) -> Vector:
        return self.root_component.position

    @BaseObject.position.setter  # type: ignore
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

    @staticmethod
    def spawnable(old_init: typing.Callable) -> typing.Callable:
        """
        Implicitly adds parameters needed to call `Entity.__init__()`.

        Args:
            old_init (typing.Callable): the original __init__ function

        Returns:
            typing.Callable: the new __init__ function
        """
        def wrapped_entity_init(self, *args,
                                pos: tuple, scene: Scene, **kwargs):
            Entity.__init__(self, scene=scene, pos=pos)
            old_init(self, *args, **kwargs)

        return wrapped_entity_init
