"""Contains scene-related classes."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Type
import pyglet

from structs.point import Point

if TYPE_CHECKING:
    from engine.game import Game
    from engine.entity import Entity
    from engine.component import Element, Component, SceneComponent


class Scene:
    """Represents a scene containing components.

    A Scene manages a list of components and is responsible for rendering them.
    Internally, this uses a Batch provided by Pyglet. This reduces the amount
    of draw calls for all components in this Scene to one.
    """

    def __init__(self, game: Game):
        """Construct a scene.

        A scene consists of a list of components.
        """
        self.game: Game = game

        # the batch to use to render
        self.batch = pyglet.graphics.Batch()

        # a list of extra raw components to render (debug)
        self.components: List[SceneComponent] = []

    def render(self, delta: float):
        """Render this scene.

        This method will call this scene's batch draw, as well as
        every component's onRender() methods.

        Args:
            delta (float): the time (in seconds) that passed since
                           the last frame

        """
        self.batch.draw()  # render everything in the batch

        for component in self.components:
            component.onRender(delta)

    def update(self, delta: float):
        """Update this scene.

        This method will call every component's onUpdate() methods.

        Args:
            delta (float): the time (in seconds) that passed since
                           the last tick
        """
        self.onUpdate(delta)

        for component in self.components:
            component.onUpdate(delta)

    def spawnComponent(self, cmp_class: Type[SceneComponent],
                       pos: tuple = (0, 0), *args, parent: Element = None,
                       **kwargs) -> SceneComponent:
        """Create a component from its class.

        Args:
            cmp_class (Type[SceneComponent]): the class of the component
            pos (tuple, optional): the position to spawn the component
            parent (Element, optional): the parent of this component

        Returns:
            SceneComponent: the component that was spawned
        """
        kwargs['pos'] = pos
        kwargs['scene'] = self
        kwargs['parent'] = parent

        # print('args: ' + str(args) + str(kwargs))
        # if hasattr(self.game, 'console'):
        #     self.game.console.log('spawned component')

        component = cmp_class(*args, **kwargs)

        if parent is not None:  # add it to the parent's children
            parent.children.append(component)

        self.components.append(component)
        return component

    def destroyComponent(self, *components: SceneComponent):
        """Remove an entity and all its components from this scene."""
        self.components.remove(*components)
        for component in components:
            print(
                f'destroying entity {type(component).__name__} '
                f'({len(component.children)} components)'
            )
            component.onDestroy()

            for child in component.children:
                if type(child) is SceneComponent:
                    self.destroy(child)  # type: ignore

    @property
    def component_count(self) -> int:
        """Return the total amount of components being rendered."""
        num = 0
        for component in self.components:
            num += len(component.children)
        return num + len(self.components)

    # --------------------------------------------------------------------------
    #  Event Methods
    # --------------------------------------------------------------------------

    def onLoad(self):
        """This method is called when this scene is loaded.

        Overriding this method eliminates the need to override __init__().
        """
        pass

    def onUpdate(self, delta: float):
        """This method is called on every tick."""
        pass
