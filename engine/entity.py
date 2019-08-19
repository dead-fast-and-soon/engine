from __future__ import annotations

from engine.view import HudView
from structs.point import Point

import typing

if typing.TYPE_CHECKING:
    from engine.view import View
    from engine.component import Component
    from engine.game.scene import Scene


class Entity:
    """
    An in-game object.
    """

    def __init__(
        self, x: float = 0.0, y: float = 0.0, *,
        pos: typing.Optional[typing.Union[Point, tuple]]=None,
        view: View, scene: Scene
    ):
        if pos is None:
            pos = Point(x, y)
        else:
            pos = Point.createFrom(pos)

        # the position of this entity
        self.pos = pos

        # the View to use when rendering this entity
        self.view = view

        # the Scene that spawned this entity
        self.scene: Scene = scene

        # the components that this entity should render
        self.components: typing.List[Component] = []

    def destroyEntity(self):
        """
        This method will delete this entity.
        """
        self.scene.destroyEntity(self)

    def addComponent(self, *components):
        self.components.append(*components)

    def removeComponent(self, *components):
        self.components.remove(*components)

    def renderEntity(self, delta: float):
        """
        Renders all components attached to this entity.
        """
        for component in self.components:
            component.render(delta)

    def updateEntity(self, delta: float):
        """
        Updates this entity.
        """
        self.onUpdate(delta)

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Events (to be overridden by subclasses)
    # --------------------------------------------------------------------------

    def onSpawn(self):
        """
        This method will run once when the entity is spawned.
        """
        pass

    def onKeyPress(self, symbol, modifier):
        """
        This method is called every time a key was pressed.
        """
        pass

    def onUpdate(self, delta: float):
        """
        This method is called on every tick.
        """
        pass
