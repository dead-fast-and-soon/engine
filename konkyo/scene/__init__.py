"""Contains scene-related classes."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Type, TypeVar, Union
import pyglet

import konkyo
import konkyo.utils
from konkyo.camera import PixelCamera
from konkyo.graphics import BatchRenderer
from konkyo.structs.vector import Vector
from konkyo.mixins.nameable import Nameable
from konkyo.mixins.renderable import Renderable
from konkyo.mixins.scriptable import Scriptable
from konkyo.objects.component import (Component, BatchComponent,
                                      RenderedComponent)

if TYPE_CHECKING:
    from konkyo.camera import Camera
    from konkyo.game import Game
    from konkyo.objects.entity import Entity


class Scene(Nameable):
    """
    Represents a scene containing components.

    A Scene manages a list of components and is responsible for rendering them.
    Internally, this uses a Batch provided by Pyglet. This reduces the amount
    of draw calls for all components in this Scene to one.
    """

    def __init__(self, game: Game, name: str = None):
        """Construct a scene.

        A scene consists of a list of components.
        """
        super().__init__(name=name)

        self.game: Game = game

        # the batch to use to minimize draw calls
        self.batch: BatchRenderer = BatchRenderer(self, 10)  # 10 layers

        # the camera to use to render this scene
        self.camera: Camera = PixelCamera(self)

        # a list of entities
        self.entities: List[Entity] = []

        # a list of all components in the scene
        self.components: List[Component] = []

        # a list of objects that need draw calls
        self._renderable_components: List[Renderable] = []

        # a list of objects that need update calls
        self._updatable_objects: List[Scriptable] = []

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

        # render everything else
        [component.render() for component in self._renderable_components]
        # for component in self._renderable_components:
        #     component.render()

    def update(self, delta: float):
        """Update this scene.

        This method will call every component's on_update() methods.

        Args:
            delta (float): the time (in seconds) that passed since
                           the last tick
        """
        self.on_update(delta)

        for obj in self._updatable_objects:
            obj.on_update(delta)

    def spawn_component(self, cmp_class: Type[konkyo.T], pos: tuple, *args,
                        name: str = None, parent: Component = None,
                        **kwargs) -> konkyo.T:
        """
        Spawn a component into this Scene.

        Args:
            component: a component or list of components
        """
        if issubclass(cmp_class, BatchComponent):
            kwargs['scene'] = self

        component = konkyo.create_component(cmp_class, pos, name=name,
                                            parent=parent,
                                            *args, **kwargs)
        self._register_components(konkyo.collect_components(component))

        return component

    def destroy_component(self, component):
        """
        Remove an entity and all its components from this Scene.

        Args:
            components: a component or list of components
        """
        children = konkyo.collect_components(component, False)
        all_components = children + [component]

        for comp in set(all_components):
            try:
                comp.on_destroy()
            except AssertionError as e:
                print('failed to destroy: {}'.format(e))

        self._unregister_components(all_components)

    def spawn_entity(self, ent_class: Type[konkyo.E], pos: tuple = (0, 0),
                     *args, **kwargs) -> konkyo.E:
        """
        Spawn an Entity into this Scene.

        Args:
            ent_class (Type[Entity]): the class of the entity
            pos (tuple, optional): the world position of the entity
        """
        entity = konkyo.create_entity(ent_class, pos, *args, **kwargs,
                                      scene=self)
        components = konkyo.collect_components(entity)

        self.entities.append(entity)
        self._register_components(components)

        if konkyo.utils.is_function_defined(entity.on_update):
            self._updatable_objects.append(entity)

        print('spawned entity {} ({} components)'
              .format(entity.name, len(components)))

        for comp in components:
            print(' - "{}" ({})'.format(comp.name, type(comp).__name__))

        return entity

    def destroy_entity(self, entity: Entity):
        """
        Delete an Entity from the Scene.

        Args:
            entity (Entity): the entity to delete
        """
        self.entities.remove(entity)
        components = konkyo.collect_components(entity)
        for component in components:
            self.destroy_component(component)
        self._unregister_components(components)

        if konkyo.utils.is_function_defined(entity.on_update):
            self._updatable_objects.remove(entity)

    def _register_components(self, components: List[Component]):
        """
        Register components as part of this scene.

        Args:
            components (List[Component]): a list of components
        """
        for component in components:
            self.components.append(component)
            if isinstance(component, Renderable):
                self._renderable_components.append(component)
            if konkyo.utils.is_function_defined(component.on_update):
                self._updatable_objects.append(component)

    def _unregister_components(self, components: List[Component]):
        """
        Unregister components from this scene.

        Args:
            components (List[Component]): a list of components
        """
        for component in components:
            self.components.remove(component)
            if isinstance(component, Renderable):
                self._renderable_components.remove(component)
            if konkyo.utils.is_function_defined(component.on_update):
                self._updatable_objects.remove(component)

    @property
    def component_count(self) -> int:
        """Return the total amount of components being rendered."""
        return len(self.components)

    # --------------------------------------------------------------------------
    #  Event Methods
    # --------------------------------------------------------------------------

    def on_load(self):
        """This method is called when this scene is loaded.

        Overriding this method eliminates the need to override __init__().
        """
        pass

    def on_update(self, delta: float):
        """This method is called on every tick."""
        pass
