"""Contains scene-related classes."""

from __future__ import annotations
from structs.point import Point
import typing

if typing.TYPE_CHECKING:
    from engine.game import Game
    from engine.entity import Entity
    from engine.component import Component


class Scene:
    """Represents a scene containing components and/or entities."""

    def __init__(self, game: Game):
        """Construct a scene.

        A scene consists of a list of components and/or entities to render.
        """
        self.game: Game = game

        # the list of entities currently spawned
        self.entities: typing.List[Entity] = []

        # a list of extra raw components to render (debug)
        self.components: typing.List[Component] = []

    def renderScene(self, delta: float):
        """Render this scene.

        Args:
            delta (float): the time (in seconds) it took
                           to render the last frame

        """
        for entity in self.entities:
            entity.renderEntity(delta)

        # also render debug components
        for component in self.components:
            component.render(delta)

    def spawnEntity(self, ent_class: typing.Type[Entity], pos: tuple = (0, 0),
                    *args, **kwargs) -> Entity:
        """Spawn an entity into the scene.

        Args:
            ent_class (typing.Type[Entity]): the classtype of the entity
            pos (tuple, optional): the position to spawn the entity

        Returns:
            Entity: the entity that was spawned

        """
        kwargs['pos'] = pos
        # kwargs['scene'] = self
        entity = ent_class(*args, **kwargs)

        self.game.log(
            f'spawning entity {type(entity).__name__} @ '
            f'({pos[0]}, {pos[1]}) '
            f'with {len(entity.components)} components'
        )

        self.entities.append(entity)
        entity.onSpawn()

        return entity

    def destroyEntity(self, entity: Entity):
        """Remove an entity and all its components from this scene."""
        print(
            f'destroying entity {type(entity).__name__} '
            f'({len(entity.components)} components)'
        )
        self.entities.remove(entity)

    @property
    def component_count(self) -> int:
        """Return the total amount of components being rendered."""
        num = 0
        for entity in self.entities:
            num += len(entity.components)
        return num + len(self.components)

    @property
    def entity_count(self) -> int:
        """Return the total amount of entities."""
        return len(self.entities)
