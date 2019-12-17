import pyglet
from pyglet import graphics

import math

from engine.objects.component import RenderedComponent, BatchComponent
from structs.vector import Transform


class DotComponent(RenderedComponent):

    def on_render(self):
        pyglet.graphics.draw(
            1,
            pyglet.gl.GL_POINTS,
            ('v2i', (int(self.position.x), int(self.position.y))),
            ('c3B', (255, 0, 0))  # red
        )


class Quad(RenderedComponent):
    """
    A simple box.
    """

    @RenderedComponent.spawnable
    def __init__(self, width: float, height: float,
                 r=255, g=255, b=255):

        self.w = width
        self.h = height
        self.r, self.g, self.b = r, g, b

        self.vertices = pyglet.graphics.vertex_list(
            4, 'v2i', ('c3B', (r, g, b) * 4)
        )

    def on_render(self):
        pos = self.position

        x, y, w, h = int(pos.x), int(pos.y), int(self.w), int(self.h)

        self.vertices.vertices =\
            [x, y] + [x + w, y] + [x + w, y + h] + [x, y + h]

        self.vertices.draw(pyglet.gl.GL_QUADS)


class Text(BatchComponent):

    @BatchComponent.spawnable
    def __init__(self, text: str = ''):

        self.pyglet_text = pyglet.text.Label(
            text,
            font_name='Consolas',
            font_size=12,
            x=self.position.x, y=self.position.y,
            batch=self.scene.batch.pyglet_batch
        )
        self.text = text

    @property
    def text(self):
        return self.pyglet_text.text

    @text.setter
    def text(self, text: str):
        self.pyglet_text.text = text

    def on_position_change(self):
        self.pyglet_text.x = self.position.x
        self.pyglet_text.y = self.position.y


class FpsDisplay(BatchComponent):

    @BatchComponent.spawnable
    def __init__(self):

        self.text: Text = self.create_component(Text, self.position)

        self.deltas = []

    def on_update(self, delta):

        frametime = self.scene.game.last_delta

        if frametime > 0:
            fps = str(round(1.0 / frametime, 2))
        else:
            fps = str(0.0)

        self.text.text = 'FPS: ' + fps
