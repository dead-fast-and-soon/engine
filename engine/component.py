
"""Contains the base Component class."""

from __future__ import annotations

import inspect
from typing import List, Optional, Union, Type, TypeVar, TYPE_CHECKING

from structs.vector import Vector

if TYPE_CHECKING:
    from engine.game.scene import Scene


class Element:
    """Represents any object that has a position."""

    def __init__(self, pos: tuple = (0, 0), parent: Element = None):
        """Initializes the position of an object.

        Args:
            pos (tuple, optional): [description]. Defaults to (0, 0).
        """
        self._pos: Vector = Vector.createFrom(pos)

        self.parent: Optional[Element] = parent

        self.children: List[Element] = []

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def pos(self) -> Vector:
        return self._pos

    @pos.setter
    def pos(self, pos: Union[tuple, Vector]):
        """Set the position of this element. This will also set the position
        of any child elements.
        
        Args:
            pos (Union[tuple, Vector]): [description]
        """
        a = self._pos
        b = Vector.createFrom(pos)
        self._pos = b

        # translate children positions by difference
        for child in self.children:
            child.pos += (b.x - a.x, b.y - a.y)

        self.onPositionChange()

    @property
    def lpos(self) -> Vector:
        """
        Get or set the position of this component with respect to the parent.

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
            return Vector(a.x - b.x, a.y - b.y)

    @property
    def master(self) -> Element:
        """Retrieve the top-most parent in the component heirarchy."""
        if self.parent is None:
            return self
        else:
            return self.parent.master

    def onPositionChange(self):
        """Called when this object's position changes."""
        pass


class Component(Element):
    """A renderable object."""

    def __init__(self, pos: tuple = (0, 0), parent: Element = None):
        """Initializes a renderable component.

        Args:
            pos (tuple, optional): the position of this component
            parent (Component, optional): [description]. Defaults to None.
            view (Camera, optional): [description]. Defaults to None.

        """
        super().__init__(pos=pos, parent=parent)

    def addComponent(self, *components: Component):
        """Add a child component to this component.

        Args:
            component (Component): the component to add

        """
        self.children.append(*components)

    def removeComponent(self, *components: Component):
        """Remove a component from this component."""
        self.children.remove(*components)

    def translateChildren(self, x: float, y: float):
        """Translate the position of all child components."""
        if len(self.children) > 0:
            for component in self.children:
                component.pos += (x, y)

    def deleteChildren(self):
        """Clear this component's list of children."""
        self.children = []

    # -------------------------------------------------------------------------
    # Events (to be overridden by subclasses)
    # -------------------------------------------------------------------------

    def onRender(self, delta: float):
        """Render this component on every frame."""
        pass

    def onUpdate(self, delta: float):
        """Update this component on every tick."""
        pass


class SceneComponent(Component):
    """A component that is rendered by a scene."""

    def __init__(self, scene: Scene, pos: tuple = (0, 0),
                 parent: Element = None):
        """Create a SceneComponent.

        Args:
            scene (Scene): the scene that renders this component
            pos (tuple, optional): the position of this component
            parent (Component, optional): the parent of this component
        """
        super().__init__(pos=pos, parent=parent)

        self.scene: Scene = scene

    def onDestroy(self):
        pass

    def spawnComponent(
        self, comp_cls, pos: Union[tuple, Vector], *args, **kwargs
    ):
        """Instantiate a new SceneComponent and add it to this one."""
        return self.scene.spawnComponent(comp_cls, pos, parent=self,
                                         *args, **kwargs)


def spawnable(old_init):
    """
    Implicitly adds parameters needed to call `SceneComponent.__init__()`
    and implicitly calls `super().__init__()`.

    When using this decorator, it is recommended to create instances
    of this component using `Scene.spawnComponent()`.

        class ExampleComponent(SceneComponent):
            @spawnable
            def __init__(self):
                pass

        game = Game()
        scene = game.newScene()

        scene.spawnComponent(ExampleComponent)
    """

    def component_super(self, *args, pos: tuple, scene: Scene,
                        parent: Element, **kwargs):
        SceneComponent.__init__(self, scene=scene, pos=pos, parent=parent)

        old_init(self, *args, **kwargs)

    sig_old = inspect.signature(old_init)

    # old parameter list
    params_a = list(sig_old.parameters.values())
    # new parameter list
    params_b = list(inspect.signature(component_super).parameters.values())

    # insert old parameter list into new
    new_params = (
        params_a[0:1] + params_b[2:5] +
        params_a[1:] + params_b[1:2] + params_b[5:6]
    )

    # component_super.__signature__ = sig_old.replace(
    #     parameters=tuple(new_params))

    return component_super
