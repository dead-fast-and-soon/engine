
from __future__ import annotations
from structs.point import Point
from typing import List, Optional, Union
from engine.view import View, HudView


class Component:
    """
    A renderable object.
    """

    def __init__(
        self, x: float = 0.0, y: float = 0.0,
        *,
        pos: Optional[Union[Point, tuple]]=None,
        parent: Component = None, view: View
    ):
        # local position (world if this is the parent component)
        if pos is None:
            lpos = Point(x, y)
        else:
            lpos = Point.createFrom(pos)

        self._lpos: Point = lpos

        # parent component; if None then this is the parent
        self.parent: Optional[Component] = parent

        # child components
        self.children: List[Component] = []

        # if false, don't render this component
        self.enabled: bool = True

        if parent is not None and view is not None:
            print('warning: child component given a view - will be ignored')

        # currently used viewport
        self._view: Optional[View] = view

    def addComponent(self, *components):
        """
        Adds a component as a child to this component.
        """
        for component in components:
            self.children.append(component)
            component.parent = self

    def translateChildren(self, x: float, y: float):
        """
        Translates the position of all child components by a
        certain amount.
        """
        if len(self.children) > 0:
            for component in self.children:
                component.lpos += (x, y)

    def render(self, delta: float):
        """
        Internal render method.
        """
        if self.view is not None:
            self.view.useViewport()

        self.onRender(delta)

        for child in self.children:
            child.render(delta)

    def update(self, delta: float):
        """
        Internal update method.
        """
        self.onUpdate(delta)

        for child in self.children:
            child.render(delta)

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------

    @property
    def view(self) -> View:
        """
        The view currently used by this component.
        The view converts the coordinates of this component into
        screen-space coordinates.
        """
        if self.parent is not None:
            return self.parent.view  # recursively get the parent view
        else:
            if self._view is None:
                raise ValueError("this component does not have a view")
            return self._view  # return view at the topmost component

    @view.setter
    def view(self, view):
        self._view = view

    # @property
    # def x(self) -> float:
    #     """
    #     Gets or sets the X local coordinate of this component.
    #     """
    #     return self._x

    # @x.setter
    # def x(self, x: float):
    #     self._x = x

    # @property
    # def y(self) -> float:
    #     """
    #     Gets or sets the Y local coordinate of this component.
    #     """
    #     return self._y

    # @y.setter
    # def y(self, y: float):
    #     self._y = y

    @property
    def lpos(self) -> Point:
        """
        Gets or sets the position of this component.

        If this component is the top-most in hierarchy (the parent), the
        position retrieved will be with respect to world-space.
        Otherwise, it will be with respect to the parent of this component
        (local).
        """
        return self._lpos

    @lpos.setter
    def lpos(self, pos: Union[Point, tuple]):
        self._lpos = Point.createFrom(pos)

    @property
    def pos(self) -> Point:
        """
        Gets the position of this component with respect to world-space.
        """
        if self.parent is None:
            return self.lpos
        else:
            return self.parent.pos + self.lpos

    # @property
    # def spos(self) -> Point:
    #     """
    #     Gets the screen-space coordinates of this component.
    #     The conversion depends on the current view.

    #     This property is recommended when rendering the component.
    #     """
    #     pt = self.view.transformPoint(self.wpos)
    #     return pt

    # def deleteChildren(self):
    #     """
    #     Flags this component's children for deletion.
    #     """
    #     if len(self.children) > 0:
    #         for child in self.children:
    #             child.delete()

    #         self.children = []

    # def delete(self):
    #     """
    #     Flags this component (and children) for deletion.
    #     Deleted components won't be rendered.

    #     Use this method before removing this component from the
    #     main component list.
    #     """
    #     self.deleted = True
    #     print(f'deleting component { type(self).__name__ }')

    #     self.deleteChildren()

    # TODO switch _render() and render()

    # --------------------------------------------------------------------------
    # Events (to be overridden by subclasses)
    # --------------------------------------------------------------------------

    def onRender(self, delta: float):
        """
        Called on every frame.
        """
        pass

    def onUpdate(self, delta: float):
        """
        Called on every tick.
        """
        pass

    def onPositionChange(self, pos):
        """
        Called when this component's position changes.
        """
        pass

# def component(klass: type):
#     """
#     Automatically initializes the parent Component with the correct
#     parameters.
#     """
#     class DecoratedComponent(klass):

#         def __init__(self, *args, **kwargs):

#             super(klass, self).__init__(*args, **kwargs)
#             super().__init__(*args, **kwargs)

#     DecoratedComponent.__name__ = klass.__name__

#     return DecoratedComponent
