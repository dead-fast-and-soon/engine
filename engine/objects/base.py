"""
Contains classes used for GameObjects.
A GameObject is an object with an in-game visual representation.
A GameObject can contain one or more Components.
"""

from typing import Optional, List, Union
from structs.vector import Vector


class BaseObject():
    """
    BaseObject is the base class for an object with an in-game position.
    """
    def __init__(self, pos: tuple = (0, 0)):
        """
        Initializes a Component.

        Args:
            pos (tuple, optional): . Defaults to (0, 0).
        """
        self._pos: Vector = Vector.createFrom(pos)

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def position(self) -> Vector:
        return self._pos

    @position.setter
    def position(self, position: Union[tuple, Vector]):
        """Set the position of this element. This will also set the position
        of any child elements.

        Args:
            pos (Union[tuple, Vector]): [description]
        """
        self._pos = Vector(position)
        self.on_position_change()

    def on_position_change(self):
        """Called when this object's position changes."""
        pass
