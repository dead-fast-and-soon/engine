
"""Contains the base Component class."""

from __future__ import annotations
from structs.point import Point
from typing import List, Optional, Union, Type, TypeVar


class Element:
    """Represents any object that has a position."""

    def __init__(self, pos: tuple = (0, 0)):
        """Initializes the position of an object.

        Args:
            pos (tuple, optional): [description]. Defaults to (0, 0).
        """
        self._pos: Point = Point.createFrom(pos)

    @property
    def pos(self) -> Point:
        return self._pos

    @pos.setter
    def pos(self, pos: Point):
        self._pos = pos
        self.onPositionChange()

    def onPositionChange(self):
        """Called when this object's position changes."""
        pass


class Component(Element):
    """A renderable object."""

    def __init__(self, pos: tuple = (0, 0), parent: Component = None,
                 *args, **kwargs):
        """Initializes a renderable component.

        Args:
            pos (tuple, optional): the position of this component
            parent (Component, optional): [description]. Defaults to None.
            view (Camera, optional): [description]. Defaults to None.

        """
        super().__init__(pos)

        # the parent component; if none, this is the parent
        self.parent: Optional[Component] = parent

        # a list of child components
        self.children: List[Component] = []

    @staticmethod
    def construct(cmp_class: Type[Component], pos: tuple = (0, 0),
                  parent: Component = None,
                  *args, **kwargs) -> Component:
        """Create a component from its class."""
        kwargs['pos'] = pos
        kwargs['parent'] = parent

        return cmp_class(*args, **kwargs)

    def addComponent(self, cmp_class: Type[Component], pos: tuple = (0, 0),
                     *args, **kwargs) -> Component:
        """Add a component to this group.

        Args:
            cmp_class (Type[Component]): the classtype of the component
            pos (tuple, optional): the position of the component

        """
        component = Component.construct(cmp_class, pos, self, *args, **kwargs)
        self.children.append(component)
        return component

    def translateChildren(self, x: float, y: float):
        """Translate the position of all child components."""
        if len(self.children) > 0:
            for component in self.children:
                component.pos += (x, y)

    def render(self, delta: float):
        """Render this component.

        This method will run on every frame.
        """
        self.onRender(delta)

        for child in self.children:
            child.render(delta)

    def update(self, delta: float):
        """Update this component.

        This method will run on every tick.
        """
        self.onUpdate(delta)

        for child in self.children:
            child.render(delta)

    def deleteChildren(self):
        """Clear this component's list of children."""
        self.children = []

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------

    @property
    def lpos(self) -> Point:
        """Get or set the position of this component with respect to the parent.

        If this component is the top-most in hierarchy (the parent), the
        position retrieved will be with respect to world-space.
        Otherwise, it will be with respect to the parent of this component
        (local).
        """
        if self.parent is None:
            return self.pos
        else:
            a = self.pos
            b = self.master.pos
            return Point(a.x - b.x, a.y - b.y)

    @property
    def master(self) -> Component:
        """Retrieve the top-most parent in the component heirarchy."""
        if self.parent is None:
            return self
        else:
            return self.parent.master

    # --------------------------------------------------------------------------
    # Events (to be overridden by subclasses)
    # --------------------------------------------------------------------------

    def onRender(self, delta: float):
        """Render this component on every frame."""
        pass

    def onUpdate(self, delta: float):
        """Update this component on every tick."""
        pass


class SceneComponent(Component):
    """A component that is rendered by a scene."""

    def __init__(self, scene: Scene, pos: tuple = (0, 0),
                 parent: Component = None):
        """Create a SceneComponent.

        Args:
            scene (Scene): the scene that renders this component
            pos (tuple, optional): the position of this component
            parent (Component, optional): the parent of this component
        """
        super().__init__(pos=pos, parent=parent)

        self.scene = scene

    def onDestroy(self):
        pass

    @staticmethod
    def implicit_super(old_init):
        """Implicitly adds parameters needed to call `SceneComponent.__init__()`
           and implicitly calls `super().__init__()`.
        """

        def _super(self, pos: tuple, scene: Scene, parent: Component,
                   *args, **kwargs):
            print('args: ' + str(args) + str(kwargs))
            super().__init__(pos=pos, scene=scene, parent=parent)

            old_init(self, *args, **kwargs)

        sig_old = inspect.signature(old_init)

        # old parameter list
        params_a = list(sig_old.parameters.values())
        # new parameter list
        params_b = list(inspect.signature(new_init).parameters.values())

        # insert old parameter list into new
        new_params = (
            params_a[0:1] + params_b[1:4] +
            params_a[1:] + params_b[4:]
        )

        _super.__signature__ = sig_old.replace(parameters=tuple(new_params))

        return _super
