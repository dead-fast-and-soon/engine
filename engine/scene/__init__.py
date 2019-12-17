"""Contains scene-related classes."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Type, TypeVar, Union
import pyglet

from engine.camera import PixelCamera
from engine.graphics import BatchRenderer
from structs.vector import Vector
from engine.objects.component import (Component, BatchComponent,
                                      RenderedComponent)
import engine

if TYPE_CHECKING:
    from engine.camera import Camera
    from engine.game import Game
    from engine.objects.entity import Entity


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
        self.batch: BatchRenderer = BatchRenderer(10)  # 10 layers

        # the camera to use to render this scene
        self.camera: Camera = PixelCamera(self)

        # a list of entities
        self.entities: List[Entity] = []

        # a list of all components in the scene
        self.components: List[Component] = []

        # a list of components that need draw calls
        self.rendered_components: List[RenderedComponent] = []

    def use_camera(self, camera_class: Type[Camera], *args, **kwargs):
        """
        Creates a Camera that will be used to render this scene.
        All other arguments will be forwarded to the constructor of the
        Camera class provided.

        Args:
            camera_class (Type[Camera]): the class of the camera
        """
        self.camera = camera_class(self, *args, **kwargs)  # type: ignore

    def render(self):
        """Render this scene.

        This method will call this scene's batch draw, as well as
        every component's on_render() methods.

        Args:
            delta (float): the time (in seconds) that passed since
                           the last frame

        """
        self.camera.arm()  # set openGL coordinates
        self.batch.render()  # render everything in the batch

        for component in self.rendered_components:  # render everything else
            component.render()

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
            component.update(delta)

    def spawn_component(self, cmp_class: Type[engine.T], pos: tuple,
                        *args, **kwargs):
        """
        Spawn a component into this Scene.

        Args:
            component: a component or list of components
        """
        kwargs['scene'] = self

        component = engine.create_component(cmp_class, pos, *args, **kwargs)
        self.components += engine.collect_components(component)

    def destroy_component(self, components: Union[List[Component], Component]):
        """
        Remove an entity and all its components from this Scene.

        Args:
            components: a component or list of components
        """
        if isinstance(components, Component): components = [components]

        for component in components:
            print('destroying entity {} ({} components)'
                  .format(type(component).__name__, len(component.children)))
            component.on_destroy()

            for child in component.children:
                self.destroy_component(child)

    def spawn_entity(self, ent_class: Type[Entity], pos: tuple = (0, 0),
                     *args, **kwargs):
        """
        Spawn an Entity into this Scene.

        Args:
            ent_class (Type[Entity]): the class of the entity
            pos (tuple, optional): the world position of the entity
        """
        entity = engine.create_entity(ent_class, pos, *args,
                                      scene=self, **kwargs)
        components = engine.collect_components(entity)

        self.entities.append(entity)
        self._register_components(components)

        print('spawned entity ({} components)'.format(len(components)))
        for comp in components:
            print(' - "{}" ({})'.format(comp.name, type(comp).__name__))

    def destroy_entity(self, entity: Entity):
        """
        Delete an Entity from the Scene.

        Args:
            entity (Entity): the entity to delete
        """
        self.entities.remove(entity)
        components = engine.collect_components(entity)
        for component in components:
            self.destroy_component(component)
        self._unregister_components(components)

    def _register_components(self, components: List[Component]):
        """
        Register components as part of this scene.

        Args:
            components (List[Component]): a list of components
        """
        for component in components:
            self.components.append(component)
            if isinstance(component, RenderedComponent):
                self.rendered_components.append(component)

    def _unregister_components(self, components: List[Component]):
        """
        Unregister components from this scene.

        Args:
            components (List[Component]): a list of components
        """
        for component in components:
            self.components.remove(component)
            if isinstance(component, RenderedComponent):
                self.rendered_components.remove(component)

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
