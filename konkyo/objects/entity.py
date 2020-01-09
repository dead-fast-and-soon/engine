
from __future__ import annotations

from konkyo.structs.vector import Vector
from konkyo.objects.base import ScriptableObject
from konkyo.mixins.nameable import Nameable
from konkyo.objects.component import Component
import konkyo
import konkyo.utils

from typing import TYPE_CHECKING, Type, List, Callable

if TYPE_CHECKING:
    from konkyo.scene import Scene


class Entity(ScriptableObject, Nameable):
    """
    An Entity is a game object that is composed of multiple components.
    """
    def __init__(self, pos: tuple, scene: Scene, name: str = None,
                 *args, **kwargs):
        """
        Create an Entity.

        Args:
            pos (tuple, optional): the position to spawn this entity
        """
        super().__init__(pos=pos, name=name, *args, **kwargs)

        # the Scene that spawned this entity
        self.scene: Scene = scene

        # the root Component of this entity
        self.root_component: Component = Component(pos=pos, name='Root')

    def create_component(self, cmp_class: Type[konkyo.T],
                         pos: tuple = (0, 0), *args, **kwargs) -> konkyo.T:
        kwargs['scene'] = self.scene  # manually add scene
        comp = konkyo.create_component(cmp_class, pos,
                                       parent=self.root_component,
                                       *args, **kwargs)
        self.scene._register_components([comp])
        return comp

    # --------------------------------------------------------------------------
    # Events (to be overridden by subclasses)
    # --------------------------------------------------------------------------

    @property  # type: ignore
    def position(self) -> Vector:
        return self.root_component.position

    @position.setter  # type: ignore
    def position(self, pos: tuple):
        self.root_component.position = pos  # type: ignore

    def on_key_press(self, symbol, modifier):
        """Called every time a key is pressed."""
        pass

    def on_key_release(self, symbol, modifier):
        """Called every time a key was released."""
        pass

    def console_set(self, line_number: int, message: str):
        """
        Shortcut method to `self.scene.game.console.line()`.

        Args:
            line_number: the line number to set
            message: the message to set that line to.
        """
        self.scene.game.console.line(line_number, message)
