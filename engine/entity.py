from __future__ import annotations

from engine.camera import ScreenCamera
from structs.point import Point
from engine.component import SceneComponent, Element

import typing

if typing.TYPE_CHECKING:
    from engine.game.scene import Scene
    from engine.camera import Camera


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
