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
    """Represents a scene containing components and/or entities."""

    def __init__(self, game: Game):
        """Construct a scene.

        A scene consists of a list of components and/or entities to render.
        """
        self.game: Game = game

        # the batch to use to render
        self.batch = pyglet.graphics.Batch()

        # a list of extra raw components to render (debug)
        self.components: List[SceneComponent] = []

    def renderScene(self, delta: float):
        """Render this scene.

        Args:
            delta (float): the time (in seconds) it took
                           to render the last frame

        """
        self.batch.draw()  # render everything in the batch

        for component in self.components:
            component.onRender(delta)

    def spawnComponent(self, cmp_class: Type[SceneComponent],
                       pos: tuple = (0, 0), *args, parent: Element = None,
                       **kwargs) -> SceneComponent:
        """Create a component from its class."""
        kwargs['pos'] = pos
        kwargs['scene'] = self
        kwargs['parent'] = parent

        # print('args: ' + str(args) + str(kwargs))

        component = cmp_class(*args, **kwargs)

        if parent is not None:  # add it to the parent's children
            parent.children.append(component)

        self.components.append(component)
        return component

    def spawnEntity(self, ent_class: Type[Entity], pos: tuple = (0, 0),
                    parent: Element = None, *args, **kwargs) -> Entity:
        """Spawn an entity into the scene.

        Args:
            ent_class (typing.Type[Entity]): the classtype of the entity
            pos (tuple, optional): the position to spawn the entity

        Returns:
            Entity: the entity that was spawned

        """
        kwargs['pos'] = pos
        kwargs['scene'] = self
        kwargs['parent'] = parent

        entity = ent_class(*args, **kwargs)
        self.game.log(
            f'spawning entity {type(entity).__name__} @ '
            f'({pos[0]}, {pos[1]}) '
            f'with {len(entity.children)} components'
        )
        self.components.append(entity)
        return entity

    def destroy(self, *components: SceneComponent):
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
