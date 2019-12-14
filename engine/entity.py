
from __future__ import annotations

from structs.vector import Vector
from engine.component import SceneComponent, Element

import typing

if typing.TYPE_CHECKING:
    from engine.game.scene import Scene


class Entity(SceneComponent):
    """An in-game object that is composed of multiple components."""

    def __init__(self, scene: Scene, pos: tuple = (0, 0), *args, **kwargs):
        """Spawns an entity.

        Args:
            pos (tuple, optional): the position to spawn this entity

        """
        super().__init__(scene=scene, pos=pos)

    # --------------------------------------------------------------------------
    # Events (to be overridden by subclasses)
    # --------------------------------------------------------------------------

    def onKeyPress(self, symbol, modifier):
        """Called every time a key is pressed."""
        pass

    def onKeyRelease(self, symbol, modifier):
        """Called every time a key was released."""
        pass
