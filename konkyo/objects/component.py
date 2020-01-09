
"""Contains the base Component class."""

from __future__ import annotations

import inspect
from typing import (List, Optional, Union,
                    Type, TypeVar, Callable, TYPE_CHECKING)

from konkyo.objects.base import GameObject, ScriptableObject
from konkyo.mixins.nameable import Nameable
from konkyo.mixins.renderable import Renderable, BatchRenderable
from konkyo.structs.vector import Vector
import konkyo

if TYPE_CHECKING:
    from konkyo.scene import Scene


class Component(ScriptableObject, Nameable):
    """
    Component is the base class for an object that defines behavior of
    an Entity.

    Components can also have child Components.
    """
    def __init__(self, *args, pos: tuple, name: str, parent: Component = None,
                 **kwargs):
        """
        Create a Component.

        Args:
            pos (tuple): [description]
            name (str): [description]
            parent (Component, optional): [description]. Defaults to None.
        """
        super().__init__(*args, pos=pos, name=name, **kwargs)
        self._parent: Optional[Component] = parent
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

    def create_component(self, cmp_class: Type[konkyo.T],
                         pos: tuple = (0, 0), *args, **kwargs) -> konkyo.T:
        return konkyo.create_component(cmp_class, pos=pos, parent=self,
                                       *args, **kwargs)

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def parent(self) -> Optional[Component]:
        """
        Get the parent Component of this Component.

        Returns:
            Component: the parent Component or None
        """
        return self._parent

    @parent.setter
    def parent(self, parent: Component):
        """
        Set the parent Component of this Component.

        Args:
            parent (Component): the new parent Component
        """
        if parent is not self._parent:  # run only if the parents are different
            if self._parent is not None and self in self._parent.children:
                parent.children.remove(self)  # remove self from old parent
            self._parent = parent
            if self not in parent.children:
                parent.children.append(self)  # add self to new parent

    @property
    def position(self) -> Vector:
        """
        Overrides `GameObject.position` getter method.

        Returns:
            Vector: the world position of this component
        """

        return GameObject.position.fget(self)  # type: ignore

    @position.setter  # type: ignore
    def position(self, position: tuple):
        """
        Overrides `GameObject.position` setter method

        Args:
            position (tuple): the new position of this component
        """

        a: Vector = self.position
        b: Vector = Vector(position)

        diff = b - a

        GameObject.position.fset(self, b)  # type: ignore
        for child in self.children:
            child.position += diff

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

    def on_destroy(self):
        """
        Called when this Component needs to be deleted.
        """
        pass


class GameComponent(Component):
    """
    A GameComponent is a Component that has an in-game
    visual representation

    Args:
        Component ([type]): [description]
    """
    def __init__(self, pos: tuple, name: str, parent: Component,
                 *args, **kwargs):

        super().__init__(*args, **kwargs, pos=pos, name=name, parent=parent)

        self._is_visible = True

    @property
    def is_visible(self) -> bool:
        return self._is_visible

    @is_visible.setter
    def is_visible(self, visible: bool):
        if visible != self._is_visible:
            self._is_visible = visible
            if visible:
                self.on_set_visible()
            else:
                self.on_set_hidden()

            for child in self.children:
                child.is_visible = visible

    def on_set_visible(self):
        """
        Called when this component has become visible.
        """
        raise NotImplementedError('this method was not implemented by {}'
                                  .format(type(self).__name__))

    def on_set_hidden(self):
        """
        Called when this component has become hidden.
        """
        raise NotImplementedError('this method was not implemented by {}'
                                  .format(type(self).__name__))


class RenderedComponent(GameComponent, Renderable):
    """
    A RenderedComponent is a Component that is rendered
    using a render call.
    """
    def __init__(self, pos: tuple, name: str, parent: Component,
                 *args, **kwargs):
        """
        Create a RenderedComponent.

        Args:
            pos (tuple, optional): [description].
            name (str):
            parent (Component, optional): [description].
        """
        super().__init__(*args, **kwargs, pos=pos, name=name, parent=parent)


class BatchComponent(GameComponent, BatchRenderable):
    """
    A BatchComponent is a Component that is rendered using
    a batched render call from a Scene.
    """
    def __init__(self, *args, pos: tuple, name: str = None,
                 parent: Component = None, scene: Scene, **kwargs):
        """
        Create a BatchComponent.

        Args:
            pos (tuple): [description]
            name (str): [description]
            parent (Component): [description]
            scene (Scene): [description]
        """
        super(BatchComponent, self).__init__(
            pos=pos, name=name, parent=parent, scene=scene
        )

    def create_component(self, cmp_class: Type[konkyo.T], pos: tuple, *args,
                         name: str = None,
                         **kwargs) -> konkyo.T:
        comp = konkyo.create_component(cmp_class, pos, *args, name=name,
                                       parent=self, scene=self.scene, **kwargs)
        self.scene._register_components([comp])
        return comp

    def destroy_component(self, component) -> konkyo.T:
        self.scene.destroy_component(component)
        if component in self.children:
            self.children.remove(component)
