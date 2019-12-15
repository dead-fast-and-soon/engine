
import math
import pyglet
import typing

from engine.objects.component import Component, BatchComponent
from structs.color import Color, WHITE
from structs.vector import Transform

if typing.TYPE_CHECKING:
    from engine.game.scene import Scene


class Box(BatchComponent):
    """A box that is a part of a scene."""

    @BatchComponent.spawnable
    def __init__(self, size: tuple, color=None):

        if color is None:
            color = WHITE

        self.width, self.height = size
        self._color = color
        x, y, w, h = self.position.x, self.position.y, self.width, self.height

        self.vertex_list = self.scene.pyglet_batch.add(
            4, pyglet.gl.GL_QUADS, None, 'v2f',
            ('c3B', tuple(color) * 4)
        )

        self.on_position_change()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color: Color):
        self._color = color
        self.vertex_list.colors = tuple(color) * 4

    def on_destroy(self):
        self.vertex_list.delete()

    def on_position_change(self):
        x, y, w, h = self.position.x, self.position.y, self.width, self.height
        self.vertex_list.vertices = [
            x + 0, y + 0,
            x + w, y + 0,
            x + w, y + h,
            x + 0, y + h
        ]


class BoxTestComponent(BatchComponent):
    """A graphics test using boxes."""

    @BatchComponent.spawnable
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

            box = self.spawn_component(
                Box, ((i - 750) * 0.8, 0),
                size=(10, 10), color=color
            )
            self.boxes.append(box)

    def on_update(self, delta: float):

        for i in range(0, len(self.boxes)):
            box = self.boxes[i]
            box.pos = (
                box.pos.x,
                math.sin(self.ticks * 0.01 + (i * 0.1))
                * math.cos(self.ticks * 0.01 + (i * 0.01)) * 200
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

    def on_update(self, delta: float):
        pass

    def on_render(self, delta: float):
        self.batch.draw()
