
import pyglet
from engine.component import Component, Element
from structs.color import Color, WHITE
from structs.point import Transform


class BoxElement(Element):
    """A box that is a part of a batch."""

    def __init__(self, pos: tuple, dims: tuple, batch, color=None):
        super().__init__(pos)

        if color is None:
            color = WHITE

        self.width, self.height = dims
        r, g, b = color.r, color.g, color.b
        x, y, w, h = self.pos.x, self.pos.y, self.width, self.height

        self.vertex_list = batch.add(
            4, pyglet.gl.GL_QUADS, None, 'v2i',
            ('c3B', (r, g, b) * 4)
        )

        self.onPositionChange()

    def onPositionChange(self):
        x, y, w, h = self.pos.x, self.pos.y, self.width, self.height
        self.vertex_list.vertices = [
            x + 0, y + 0,
            x + w, y + 0,
            x + w, y + h,
            x + 0, y + h
        ]


class BoxBatch(Component):
    """A batch of quads."""

    def __init__(self):
        super().__init__()

        self.batch = pyglet.graphics.Batch()
        self.elements = []

    def addSquare(self, pos: tuple, dims: tuple, color=None):
        quad = BoxElement(pos, dims, self.batch, color)
        self.elements.append(quad)
        return quad

    def onUpdate(self, delta: float):
        pass

    def onRender(self, delta: float):
        self.batch.draw()
