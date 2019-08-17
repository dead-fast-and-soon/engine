
from __future__ import annotations
import config
from structs.point import Point, Transform
import typing

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


class HudView(View):
    """
    A HUD view is a 1:1 conversion of world-space to screen-space coordinates.
    Coordinates of components using this view will be passed as is as
    screen coordinates.
    """

    def __init__(self, zoom: float = 1.0):
        super().__init__(0, 0, zoom)

    def transformPoint(self, p: Point):
        x = int(p.x * self.zoom)
        y = int(p.y * self.zoom)

        return Point(x, y)
