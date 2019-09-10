
import math
import pyglet
import typing

from engine.component import Component, SceneComponent
from structs.color import Color, WHITE
from structs.vector import Transform

if typing.TYPE_CHECKING:
    from engine.game.scene import Scene


class Box(SceneComponent):
    """A box that is a part of a scene."""

    @SceneComponent.implicit_super
    def __init__(self, size: tuple, color=None):

        if color is None:
            color = WHITE

        self.width, self.height = size
        r, g, b = color.r, color.g, color.b
        x, y, w, h = self.pos.x, self.pos.y, self.width, self.height

        self.vertex_list = self.scene.batch.add(
            4, pyglet.gl.GL_QUADS, None, 'v2f',
            ('c3B', (r, g, b) * 4)
        )

        self.onPositionChange()

    def onDestroy(self):
        self.vertex_list.delete()

    def onPositionChange(self):
        x, y, w, h = self.pos.x, self.pos.y, self.width, self.height
        self.vertex_list.vertices = [
            x + 0, y + 0,
            x + w, y + 0,
            x + w, y + h,
            x + 0, y + h
        ]


class BoxTestComponent(SceneComponent):
    """A graphics test using boxes."""

    @SceneComponent.implicit_super
    def __init__(self):

        self.boxes = []
        self.ticks = 0

        for i in range(0, 1500):

            if i < 750:
                # blue to cyan
                color = Color(0, int(255 * (i / 750)), 255)
            else:
                # cyan to green
                color = Color(0, 255, int(255 * (1 - ((i - 750) / 750))))

            box = self.spawnComponent(
                Box, ((i - 750) * 0.8, 0),
                size=(10, 10), color=color
            )
            self.boxes.append(box)

    def onUpdate(self, delta: float):

        for i in range(0, len(self.boxes)):
            box = self.boxes[i]
            box.pos = (
                box.pos.x,
                math.sin(self.ticks * 0.01 + (i * 0.1)) *
                math.cos(self.ticks * 0.01 + (i * 0.01)) * 200
            )

        self.ticks += 1


class BoxBatch(Component):
    """A batch of quads."""

    def __init__(self):
        super().__init__()

        self.batch = pyglet.graphics.Batch()
        self.elements = []

    def addSquare(self, pos: tuple, dims: tuple, color=None):
        quad = Box(pos, dims, self.batch, color)
        self.elements.append(quad)
        return quad

    def onUpdate(self, delta: float):
        pass

    def onRender(self, delta: float):
        self.batch.draw()
