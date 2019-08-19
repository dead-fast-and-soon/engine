from __future__ import annotations
from structs.point import Point
import typing

if typing.TYPE_CHECKING:
    from engine.game import Game
    from engine.entity import Entity
    from engine.component import Component


class Scene:
    """
    Stores assets for a game.
    """

    def __init__(self, game):
        self.game: Game = game

        # the list of entities currently spawned
        self.entities: typing.List[Entity] = []

        # a list of extra raw components to render (debug)
        self.components: typing.List[Component] = []

    def renderScene(self, delta: float):
        """
        Renders all entities in this scene.
        """
        for entity in self.entities:
            entity.renderEntity(delta)

        # also render debug components
        for component in self.components:
            component.render(delta)

    def spawnEntity(
        self,
        ent_class: typing.Type[Entity], pos=(0, 0), *args, **kwargs
    ) -> Entity:
        """
        Adds an entity and all its components to this state.
        """
        pos = Point.createFrom(pos)

        kwargs['pos'] = pos
        kwargs['view'] = self.game.view
        kwargs['scene'] = self
        entity = ent_class(*args, **kwargs)

        self.game.log(
            f'spawning entity {type(entity).__name__} @ '
            f'({pos.x}, {pos.y}) '
            f'with {len(entity.components)} components'
        )

        self.entities.append(entity)
        entity.onSpawn()

        return entity

    def destroyEntity(self, entity: Entity):
        """
        Removes an entity and all its components from this state.
        """
        print(
            f'destroying entity {type(entity).__name__} '
            f'({len(entity.components)} components)'
        )
        self.entities.remove(entity)

    @property
    def component_count(self) -> int:
        """
        Returns the total amount of components being rendered.
        """
        num = 0
        for entity in self.entities:
            num += len(entity.components)
        return num + len(self.components)

    @property
    def entity_count(self) -> int:
        """
        Returns the total amount of entities.
        """
        return len(self.entities)
