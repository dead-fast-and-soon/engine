
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

    def collect_components(self,
                           comp: Component = None) -> typing.List[Component]:
        """
        Retrieve all components in the heirarchy as a single list.

        Returns:
            typing.List[Component]: a list of all components in this entity
        """
        if comp is None: comp = self.root_component
        components = [comp]

        for child in comp.children:
            components += self.collect_components(child)

        return list(set(components))  # delete duplicate objects

    def update(self, delta: float):
        """
        Update this Entity.

        Args:
            delta (float): the time difference from the last tick
        """
        self.on_update(delta)
        self.root_component.update(delta)

    # --------------------------------------------------------------------------
    # Events (to be overridden by subclasses)
    # --------------------------------------------------------------------------

    @property  # type: ignore
    def position(self) -> Vector:
        return self.root_component.position

    @position.setter  # type: ignore
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
