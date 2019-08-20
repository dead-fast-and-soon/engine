from __future__ import annotations

from engine.camera import ScreenCamera
from structs.point import Point
from engine.component import Component

import typing

if typing.TYPE_CHECKING:
    from engine.camera import Camera


class Entity:
    """An in-game object."""

    def __init__(self, pos: tuple = (0, 0), *args, **kwargs):
        """Spawns an entity.

        Args:
            pos (tuple, optional): the position to spawn this entity

        """
        # the position of this entity
        self.pos = Point.createFrom(pos)

        # the components that this entity should render
        self.components: typing.List[Component] = []

    def addComponent(self, *components):
        """Add a component to this entity."""
        self.components.append(*components)

    def removeComponent(self, *components):
        """Remove a component from this entity."""
        self.components.remove(*components)

    def renderEntity(self, delta: float):
        """Render all components attached to this entity."""
        for component in self.components:
            component.render(delta)

    def updateEntity(self, delta: float):
        """Update this entity."""
        self.onUpdate(delta)

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Events (to be overridden by subclasses)
    # --------------------------------------------------------------------------

    def onSpawn(self):
        """Called when this entity is spawned."""
        pass

    def onKeyPress(self, symbol, modifier):
        """Called every time a key is pressed."""
        pass

    def onUpdate(self, delta: float):
        """Called on every tick."""
        pass
