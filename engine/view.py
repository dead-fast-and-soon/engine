
from __future__ import annotations
import config
import typing
from pyglet import gl

from structs.point import Point, Transform
from engine.game.scene import Scene

if typing.TYPE_CHECKING:
    from game import Game


class View:
    """
    A view converts world-space coordinates (of components)
    to screen-space coordinates.

    For world-space coordinates, x and y have a range of (-inf, inf)
    and (0, 0) is the origin point.

    for screen-space coordinates,
    x has a range [0, WIDTH] and y has a range of [0, HEIGHT] where WIDTH and
    HEIGHT are the size of the game window,
    and (0, 0) is the bottom-left of the window.
    """

    def __init__(self, game: Game = None,
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

    def transformPoint(self, p: Point):
        if self.game is None:
            width, height = 0, 0
        else:
            width, height = self.game.width, self.game.height
        x = int(width // 2 + ((p.x - self.fx) * self.zoom))
        y = int(height // 2 + ((p.y - self.fy) * self.zoom))

        return Point(x, y)

    def transform(self, t: Transform):
        p = self.transformPoint(t.point)  # reuse point transformation
        w = t.w * self.zoom
        h = t.h * self.zoom

        return Transform(p.x, p.y, w, h)

    def assignScene(self, scene: Scene):
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
        # if these coordinates are already being used, skip running the method
        if current_view is not self:
            # width and height of game window
            w, h = self.game.width, self.game.height
            zoom = self.zoom

            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            gl.glOrtho(
                -w / 2.0 / zoom, w / 2.0 / zoom,  # x range
                -h / 2.0 / zoom, h / 2.0 / zoom,  # y range
                0.0, 1.0                          # z range
            )


class HudView(View):
    """
    A HUD view is a 1:1 conversion of world-space to screen-space coordinates.
    Coordinates of components using this view will be passed as is as
    screen coordinates.
    """

    def __init__(self, game, zoom: float = 1.0):
        super().__init__(game, 0, 0, zoom)

    def transformPoint(self, p: Point):
        x = int(p.x * self.zoom)
        y = int(p.y * self.zoom)

        return Point(x, y)

    def useViewport(self):
        """
        This remapping places (0,0) at the bottom left of the window.
        """
        # if these coordinates are already being used, skip running the method
        if current_view is not self:
            # width and height of game window
            w, h = self.game.width, self.game.height

            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            gl.glOrtho(0.0, w, 0.0, h, 0.0, 1.0)

# the last viewport remapping
current_view: typing.Optional[View] = None
