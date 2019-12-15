"""Contains scene-related classes."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Type
import pyglet

from engine.camera import PixelCamera
from structs.vector import Vector

if TYPE_CHECKING:
    from engine.camera import Camera
    from engine.game import Game
    from engine.objects.entity import Entity
    from engine.objects.component import Component, SceneComponent


class Scene:
    """
    Represents a scene containing components.

    A Scene manages a list of components and is responsible for rendering them.
    Internally, this uses a Batch provided by Pyglet. This reduces the amount
    of draw calls for all components in this Scene to one.
    """

    def __init__(self, game: Game):
        """Construct a scene.

        A scene consists of a list of components.
        """
        self.game: Game = game

        # the batch to use to minimize draw calls
        self.pyglet_batch = pyglet.graphics.Batch()

        # the camera to use to render this scene
        self.camera: Camera = PixelCamera(self)

        # a list of entities
        self.entities: List[Entity] = []

        # a list of extra raw components to render (debug)
        self.components: List[Component] = []

    def use_camera(self, camera_class: Type[Camera], *args, **kwargs):
        """
        Creates a Camera that will be used to render this scene.
        All other arguments will be forwarded to the constructor of the
        Camera class provided.

        Args:
            camera_class (Type[Camera]): the class of the camera
        """
        self.camera = camera_class(self, *args, **kwargs)  # type: ignore

    def render(self, delta: float):
        """Render this scene.

        This method will call this scene's batch draw, as well as
        every component's on_render() methods.

        Args:
            delta (float): the time (in seconds) that passed since
                           the last frame

        """
        self.camera.arm()  # set openGL coordinates
        self.pyglet_batch.draw()  # render everything in the batch

        for entity in self.entities:
            entity.root_component.on_render(delta)

        for component in self.components:
            component.on_render(delta)

    def update(self, delta: float):
        """Update this scene.

        This method will call every component's on_update() methods.

        Args:
            delta (float): the time (in seconds) that passed since
                           the last tick
        """
        self.on_update(delta)

        for entity in self.entities:
            entity.update(delta)

        for component in self.components:
            component.on_update(delta)

    def spawn_entity(self, ent_class: Type[Entity], pos: tuple = (0, 0),
                     *args, **kwargs):
        """
        Spawn an Entity into this Scene.

        Args:
            ent_class (Type[Entity]): the class of the entity
            pos (tuple, optional): the world position of the entity
        """
        kwargs['pos'] = pos
        kwargs['scene'] = self

        entity = ent_class(*args, **kwargs)

        self.entities.append(entity)

    def spawn_component(self, cmp_class: Type[SceneComponent],
                        pos: tuple = (0, 0), *args, parent: Component = None,
                        **kwargs) -> SceneComponent:
        """
        Create a component from its class.

        Args:
            cmp_class (Type[SceneComponent]): the class of the component
            pos (tuple, optional): the position to spawn the component
            parent (Object, optional): the parent of this component

        Returns:
            SceneComponent: the component that was spawned
        """
        kwargs['pos'] = pos
        kwargs['scene'] = self
        kwargs['parent'] = parent

        # print('args: ' + str(args) + str(kwargs))
        # if hasattr(self.game, 'console'):
        # self.game.console.log('spawned component ' + str(cmp_class))

        component = cmp_class(*args, **kwargs)

        if parent is not None:  # add it to the parent's children
            parent.children.append(component)

        self.components.append(component)
        return component

    def destroy_component(self, *components: Component):
        """Remove an entity and all its components from this scene."""
        self.components.remove(*components)
        for component in components:
            print(
                f'destroying entity {type(component).__name__} '
                f'({len(component.children)} components)'
            )
            component.on_destroy()

            for child in component.children:
                if isinstance(child, Component):
                    self.destroy_component(child)

    def destroy_entity(self, entity: Entity):
        """
        Delete an Entity from the Scene.

        Args:
            entity (Entity): the entity to delete
        """
        self.entities.remove(entity)
        self.destroy_component(entity.root_component)

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

    def on_update(self, delta: float):
        """This method is called on every tick."""
        pass
