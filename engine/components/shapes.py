
import pyglet
from engine.component import Component
from structs.color import Color, WHITE
from structs.point import Transform


class Quad:

    def __init__(self, x, y, width, height, color=None, batch=None):
        if color is None:
            color = WHITE

        r, g, b = color.r, color.g, color.b

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        if batch is None:
            self.vertex_list = pyglet.graphics.vertex_list(
                4,
                (
                    'v2i',
                    (x, y) +
                    (x + width, y) +
                    (x + width, y + height) +
                    (x, y + height)
                ),
                ('c3B', (r, g, b) * 4)
            )
        else:
            self.vertex_list = batch.add(
                4, pyglet.gl.GL_QUADS, None,
                (
                    'v2i',
                    (x, y) +
                    (x + width, y) +
                    (x + width, y + height) +
                    (x, y + height)
                ),
                ('c3B', (r, g, b) * 4)
            )

    def updateVertices(self, vertices):
        self.vertex_list.vertices = vertices


class QuadBatch(Component):
    """
    A batch of quads.
    """

    def __init__(self):
        super().__init__()

        self.batch = pyglet.graphics.Batch()
        self.quads = []

    def addQuad(self, x, y, width, height, color=None):
        quad = Quad(x, y, width, height, color, self.batch)
        self.quads.append(quad)
        return quad

    def onUpdate(self, delta):
        for quad in self.quads:
            x = quad.x + self.x
            y = quad.y + self.y
            w, h = quad.width, quad.height

            # transform dimensions according to view
            t = self.view.transform(Transform(x, y, w, h))
            tx, ty, tw, th = int(t.x), int(t.y), int(t.w), int(t.h)

            quad.updateVertices(
                [tx, ty] + [tx + tw, ty] +
                [tx + tw, ty + th] + [tx, ty + th]
            )

    def onRender(self, delta):
        self.batch.draw()
