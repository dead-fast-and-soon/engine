
from __future__ import annotations

import config
import typing
from abc import ABC, abstractmethod
from pyglet import gl

from structs.vector import Vector, Transform

if typing.TYPE_CHECKING:
    from engine.game import Game
    from engine.game.scene import Scene


class Camera:
    """A camera defining the perspective of which to render scenes."""

    def __init__(self, game: Game):
        """Initializes a Camera

        Args:
            game (Game): the Game managing the window where rendering
                         takes place

        """
        self.game: Game = game
        self.scene: typing.Optional[Scene] = None

    def assignScene(self, scene: Scene):
        """Assign a scene to be rendered using this camera.

        When calling `renderScene()`, the scene will be rendered from the
        perspective of this camera.

        Args:
            scene (Scene): the scene to assign

        """
        self.scene = scene

    def renderScene(self, delta: float):
        """Render the scenes from this camera's perspective.

        If no Scene is assigned to this Camera, this method is a no-op.

        Args:
            delta (float): the time (in seconds) that passed since
                           the last frame

        """
        if self.scene is not None:
            self.arm()
            self.scene.render(delta)

    def arm(self):
        """Arm this camera.

        This method will modify the coordinate system used by OpenGL.
        Any future draw calls will be rendered from the perspective of this
        new coordinate system.

        """
        pass


class PixelCamera(Camera):
    """An orthographic camera using pixels as units.

    This camera is recommended for world-space 2D rendering.

    The focus point (defaulting to [0, 0]) are the coordinates corresponding
    to the center of the screen.

    The zoom factor (defaulting to 1) is the amount to zoom the camera in.
    Providing integer values for the zoom factor ensures pixel-perfect
    rendering.

    """

    def __init__(self, game: Game, focus: tuple = (0, 0), zoom: float = 1.0):
        super().__init__(game)

        self.zoom: float = zoom
        self.focus: Vector = Vector(focus)

    @property
    def focus(self) -> Vector:
        return self._focus

    @focus.setter
    def focus(self, pos):
        self._focus = Vector(pos)

        w, h = self.game.width, self.game.height

        x_range = (
            ((-w / 2.0) + self.focus.x) / self.zoom,
            ((+w / 2.0) + self.focus.x) / self.zoom
        )

        y_range = (
            ((-h / 2.0) + self.focus.y) / self.zoom,
            ((+h / 2.0) + self.focus.y) / self.zoom
        )

        # precalculate ranges
        self.ranges = x_range + y_range + (0.0, 1.0)  # z-range

    def arm(self):
        r = self.ranges

        if self.ranges is not None:
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            gl.glOrtho(r[0], r[1], r[2], r[3], r[4], r[5])


class ScreenPixelCamera(PixelCamera):
    """An orthographic camera using pixels as units.

    This camera sets coordinates to behave like Pyglet's default coordinates.
    The point [0, 0] corresponds to the bottom-left of the screen.

    The zoom factor (defaulting to 1) is the amount to zoom the camera in.
    Providing integer values for the zoom factor ensures pixel-perfect
    rendering.

    """

    def __init__(self, game: Game, zoom: float = 1.0):
        focus = (game.width // 2, game.height // 2)  # center of screen
        super().__init__(game, focus, zoom)
