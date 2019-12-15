
"""Contains the base Component class."""

from __future__ import annotations

import inspect
from typing import List, Optional, Union, Type, TypeVar, TYPE_CHECKING

from engine.objects.base import BaseObject
from structs.vector import Vector

if TYPE_CHECKING:
    from engine.game.scene import Scene


class Component(BaseObject):
    """
    Component is the base class for an object that defines behavior of
    an Entity.

    Components can also have child Components.
    """
    def __init__(self, pos: tuple = (0, 0), parent: Component = None):
        """
        Initializes a Component.

        Args:
            pos (tuple, optional): the position of this component
            parent (Component, optional): [description]. Defaults to None.
            view (Camera, optional): [description]. Defaults to None.

        """
        super().__init__(pos=pos)

        self.parent: Optional[Component] = parent
        self.children: List[Component] = []

    def add_component(self, *components: Component):
        """
        Add a child component to this component.

        Args:
            components (Component): the components to add

        """
        self.children.append(*components)

    def remove_component(self, *components: Component):
        """
        Remove a child component from this component.

        Args:
            components (Component): the components to remove
        """
        self.children.remove(*components)

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @BaseObject.position.setter  # type: ignore
    def position(self, position: tuple):
        """
        Overrides `BaseObject.position` setter method

        Args:
            position (tuple): the new position of this component
        """

        a: Vector = self.position
        b: Vector = Vector(position)

        self._pos = b
        for child in self.children:
            child.position += (b.x - a.x, b.y - a.y)

        self.on_position_change()

    @property
    def local_position(self) -> Vector:
        """
        Get or set the position of this component with respect to the parent.

        If this component is the top-most in hierarchy (the parent), the
        position retrieved will be with respect to world-space.
        Otherwise, it will be with respect to the parent of this component
        (local).
        """
        if self.parent is None:
            return self.position
        else:
            a = self.position
            b = self.root.position
            return Vector(a.x - b.x, a.y - b.y)

    @property
    def root(self) -> Component:
        """
        Retrieve the top-most parent in the component heirarchy.
        """
        if self.parent is None:
            return self
        else:
            return self.parent.root

    # -------------------------------------------------------------------------
    # Events (to be overridden by subclasses)
    # -------------------------------------------------------------------------

    def on_render(self, delta: float):
        """Render this component on every frame."""
        pass

    def on_update(self, delta: float):
        """Update this component on every tick."""
        pass


class SceneComponent(Component):
    """
    A SceneComponent is a Component that is rendered by a Scene.
    """

    def __init__(self, scene: Scene,
                 pos: tuple = (0, 0), parent: Component = None):
        """
        Create a SceneComponent.

        Args:
            scene (Scene): the scene that renders this component
            pos (tuple, optional): the position of this component
            parent (Component, optional): the parent of this component
        """
        super().__init__(pos=pos, parent=parent)

        self.scene: Scene = scene

    def on_destroy(self):
        pass

    def spawn_component(self, comp_cls, pos: Union[tuple, Vector],
                        *args, **kwargs):
        """
        Instantiate a new SceneComponent and add it to this one.
        """
        return self.scene.spawn_component(comp_cls, pos, parent=self,
                                          *args, **kwargs)


def spawnable(old_init):
    """
    Implicitly adds parameters needed to call `SceneComponent.__init__()`
    and implicitly calls `super().__init__()`.

    When using this decorator, it is recommended to create instances
    of this component using `Scene.spawn_component()`.

        class ExampleComponent(SceneComponent):
            @spawnable
            def __init__(self):
                pass

        game = Game()
        scene = game.newScene()

        scene.spawn_component(ExampleComponent)
    """

    def component_super(self, *args, pos: tuple, scene: Scene,
                        parent: Component, **kwargs):
        SceneComponent.__init__(self, scene=scene, pos=pos, parent=parent)

        old_init(self, *args, **kwargs)

    sig_old = inspect.signature(old_init)

    # old parameter list
    params_a = list(sig_old.parameters.values())
    # new parameter list
    params_b = list(inspect.signature(component_super).parameters.values())

    # insert old parameter list into new
    new_params = (params_a[0:1] + params_b[2:5] + params_a[1:]
                  + params_b[1:2] + params_b[5:6])

    # component_super.__signature__ = sig_old.replace(
    #     parameters=tuple(new_params))

    return component_super
