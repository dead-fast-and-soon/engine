
from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from engine.entity import Entity
    from engine.component import Component


class Scene:
    """
    Stores assets for a game.
    """

    def __init__(self, game):
        self.game = game

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

    def spawnEntity(self, entity: Entity):
        """
        Adds an entity and all its components to this state.
        """
        if entity is not None:
            self.game.log(f'spawning entity {type(entity).__name__} @ '
                          f'({entity.x}, {entity.y}) '
                          f'with {len(entity.components)} components')

            entity.scene = self  # set the entity's state if needed
            self.entities.append(entity)
            entity.onSpawn()

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
