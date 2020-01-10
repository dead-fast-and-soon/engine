
from __future__ import annotations

import typing
from konkyo.utils.gl import *

from konkyo.structs.vector import Vector, Transform

if typing.TYPE_CHECKING:
    from konkyo.game import Game
    from konkyo.scene import Scene


class Camera:
    """
    A camera defining the perspective of which to render scenes.
    """

    def __init__(self):
        """
        Initializes a Camera.
        """
        self._scene = None

    def arm(self):
        """
        Arm this camera.

        This method will modify the projection used by OpenGL.
        Any future draw calls will be rendered using this camera's projection
        """
        try:
            proj = self.projection
            view = self.view
            buffer = GLUniformBuffer(1)

            with buffer:
                # overwrite first and second parts of buffer
                buffer.sub_data(0,                    proj)
                buffer.sub_data(glm.sizeof(glm.mat4), view)
        except AttributeError:
            raise AttributeError('must bind a scene first')

    @property
    def projection(self) -> glm.mat4:
        """
        Retrieve this camera's projection matrix.
        """
        raise NotImplementedError('not implemented')

    @property
    def view(self) -> glm.mat4:
        """
        Retrieve this camera's view matrix.
        """
        raise NotImplementedError('not implemented')

    def bind_scene(self, scene: Scene):
        """
        Bind a scene to this camera.
        All render calls from the given scene following this method will
        use this camera's projection and view matrices.

        Args:
            scene (Scene): the scene to bind
        """
        self._scene = scene


class OrthoCamera(Camera):
    """
    An orthographic camera using pixels as units.

    This camera is recommended for world-space 2D rendering.

    The focus point (defaulting to [0, 0]) are the coordinates corresponding
    to the center of the screen.

    The zoom factor (defaulting to 1) is the amount to zoom the camera in.
    Providing integer values for the zoom factor ensures pixel-perfect
    rendering.
    """

    def __init__(self, focus: tuple = (0, 0), zoom: float = 1.0):
        self.zoom: float = zoom
        self._focus: Vector = Vector(focus)

        self._projection = glm.mat4(1.0)
        self._view = glm.mat4(1.0)

    @property
    def focus(self) -> Vector:
        return self._focus

    @focus.setter
    def focus(self, pos):
        self._focus = Vector(pos)
        self.update_projection()

    def update_projection(self):
        w, h = self._scene.game.width, self._scene.game.height

        x_range = (
            ((-w / 2.0) + self._focus.x) / self.zoom,
            ((+w / 2.0) + self._focus.x) / self.zoom
        )

        y_range = (
            ((-h / 2.0) + self._focus.y) / self.zoom,
            ((+h / 2.0) + self._focus.y) / self.zoom
        )

        self._projection = glm.ortho(*x_range, *y_range, -1, 1)

    @property
    def projection(self):
        return self._projection

    @property
    def view(self):
        return self._view

    def bind_scene(self, scene: Scene):
        super().bind_scene(scene)
        self.update_projection()


class HUDCamera(Camera):
    """
    An orthographic camera using pixels as units.

    This camera sets coordinates to behave like Pyglet's default coordinates.
    The point [0, 0] corresponds to the bottom-left of the screen.

    The zoom factor (defaulting to 1) is the amount to zoom the camera in.
    Providing integer values for the zoom factor ensures pixel-perfect
    rendering.
    """

    def __init__(self, zoom: float = 1.0):
        self._zoom = zoom
        self._projection = glm.mat4(1.0)
        self._view = glm.mat4(1.0)

    def bind_scene(self, scene: Scene):
        super().bind_scene(scene)
        self._projection = glm.ortho(
            0, scene.game.width / self._zoom,
            0, scene.game.height / self._zoom,
            -1, 1
        )

    @property
    def projection(self):
        return self._projection

    @property
    def view(self):
        return self._view
