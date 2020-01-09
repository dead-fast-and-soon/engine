
from __future__ import annotations

import config
import typing
import glm
from abc import ABC, abstractmethod
from engine.utils.gl import *

from structs.vector import Vector, Transform

if typing.TYPE_CHECKING:
    from engine.game import Game
    from engine.scene import Scene


class Camera:
    """
    A camera defining the perspective of which to render scenes.
    """

    def __init__(self, scene: Scene):
        """
        Initializes a Camera

        Args:
            game (Game): the Scene that this camera will render
        """
        self.scene = scene

    def arm(self):
        """
        Arm this camera.

        This method will modify the coordinate system used by OpenGL.
        Any future draw calls will be rendered from the perspective of this
        new coordinate system.
        """
        pass


class PixelCamera(Camera):
    """
    An orthographic camera using pixels as units.

    This camera is recommended for world-space 2D rendering.

    The focus point (defaulting to [0, 0]) are the coordinates corresponding
    to the center of the screen.

    The zoom factor (defaulting to 1) is the amount to zoom the camera in.
    Providing integer values for the zoom factor ensures pixel-perfect
    rendering.
    """

    def __init__(self, scene: Scene, focus: tuple = (0, 0), zoom: float = 1.0):
        super().__init__(scene)

        self.zoom: float = zoom
        self.focus: Vector = Vector(focus)

    @property
    def focus(self) -> Vector:
        return self._focus

    @focus.setter
    def focus(self, pos):
        self._focus = Vector(pos)

        w, h = self.scene.game.width, self.scene.game.height

        x_range = (
            ((-w / 2.0) + self.focus.x) / self.zoom,
            ((+w / 2.0) + self.focus.x) / self.zoom
        )

        y_range = (
            ((-h / 2.0) + self.focus.y) / self.zoom,
            ((+h / 2.0) + self.focus.y) / self.zoom
        )

        # precalculate ranges
        self.ranges = x_range + y_range + (-1, 1) # z-range

    def arm(self):
        r = self.ranges

        if self.ranges is not None:

            proj = glm.ortho(*r)
            view = glm.mat4(1.0)
            buffer = GLUniformBuffer(1)

            with buffer:
                # overwrite first and second parts of buffer
                buffer.sub_data(0,                    proj)
                buffer.sub_data(glm.sizeof(glm.mat4), view)


class ScreenPixelCamera(PixelCamera):
    """
    An orthographic camera using pixels as units.

    This camera sets coordinates to behave like Pyglet's default coordinates.
    The point [0, 0] corresponds to the bottom-left of the screen.

    The zoom factor (defaulting to 1) is the amount to zoom the camera in.
    Providing integer values for the zoom factor ensures pixel-perfect
    rendering.
    """

    def __init__(self, scene: Scene, zoom: float = 1.0):
        # set (0, 0) to bottom right
        focus = (scene.game.width // 2, scene.game.height // 2)
        super().__init__(scene, focus, zoom)
