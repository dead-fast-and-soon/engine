"""
Contains classes used for GameObjects.
A GameObject is an object with an in-game visual representation.
A GameObject can contain one or more Components.
"""

from typing import Optional, List, Union
from konkyo.mixins.scriptable import Scriptable
from konkyo.structs.vector import Vector
import konkyo.utils


class GameObject():
    """
    GameObject is the base class for an object with an in-game position.
    """

    def __init__(self, *args, pos: tuple, **kwargs):
        """
        Initializes a Component.

        Args:
            pos (tuple, optional): the initial world position of the object
        """
        super(GameObject, self).__init__(*args, **kwargs)
        self._pos: Vector = Vector(pos)

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def position(self) -> Vector:
        return self._pos

    @position.setter
    def position(self, position: Union[tuple, Vector]):
        """
        Set the world position of this object.

        Args:
            pos (Union[tuple, Vector]): [description]
        """
        self._pos = Vector(position)
        self.on_position_change()

    def on_position_change(self):
        """
        Called when this object's position changes.
        """
        pass


class ScriptableObject(GameObject, Scriptable):
    """
    A game object that can recieve updates every tick.
    """

    def __init__(self, *args, pos: tuple, **kwargs):
        super().__init__(*args, **kwargs, pos=pos)
