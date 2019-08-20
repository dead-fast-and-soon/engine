
from __future__ import annotations
from abc import ABC, abstractmethod
import config
import typing
from pyglet import gl

from structs.point import Point, Transform
from engine.game.scene import Scene

if typing.TYPE_CHECKING:
    from engine.game import Game


class Camera:
    """A camera defining the perspective of which to render scenes."""

    def __init__(self, game: Game,
                 fx: float = 0.0, fy: float = 0.0, zoom: float = 1.0):
        """
        (fx, fy) represents the focal point of the view (default is (0, 0)).
        """
        self.fx: float = fx
        self.fy: float = fy
        self.zoom: float = zoom

        self.game: Game = game

        # the scene this camera should render
        self.scene: typing.Optional[Scene] = None

        # precalculate ranges
        self.ranges = (
            -game.width / 2.0 / zoom, game.width / 2.0 / zoom,  # x range
            -game.height / 2.0 / zoom, game.height / 2.0 / zoom,  # y range
            0.0, 1.0  # z range
        )

    def assignScene(self, scene: Scene):
        """Assigns a scene to be rendered using this camera."""
        self.scene = scene

    def renderScenes(self, delta: float):
        """Render the scenes from this camera's perspective."""
        if self.scene is not None:
            self.useViewport()
            self.scene.renderScene(delta)

    def useViewport(self):
        """
        Remaps the OpenGL coordinates for future draw calls.
        By default, this remapping places (0,0) at the center of the window.
        """
        # width and height of game window
        r = self.ranges

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(r[0], r[1], r[2], r[3], r[4], r[5])


class ScreenCamera(Camera):
    """
    A HUD view is a 1:1 conversion of world-space to screen-space coordinates.
    Coordinates of components using this view will be passed as is as
    screen coordinates.
    """

    def __init__(self, game, zoom: float = 1.0):
        super().__init__(game, 0, 0, zoom)

    def useViewport(self):
        """
        This remapping places (0,0) at the bottom left of the window.
        """
        # width and height of game window
        w, h = self.game.width, self.game.height

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0.0, w, 0.0, h, 0.0, 1.0)
