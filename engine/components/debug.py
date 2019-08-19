import pyglet
from pyglet import graphics

import math

from engine.component import Component
from structs.point import Transform


class DotComponent(Component):

    def onRender(self):
        pyglet.graphics.draw(
            1,
            pyglet.gl.GL_POINTS,
            ('v2i', (int(self.x), int(self.y))),
            ('c3B', (255, 0, 0))  # red
        )


class BoxComponent(Component):
    """
    A simple box.
    """

    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 r=255,
                 g=255,
                 b=255,
                 parent=None,
                 view=None):
        super().__init__(pos=(x, y), parent=parent, view=view)

        self.w = w
        self.h = h
        self.r, self.g, self.b = r, g, b

        self.vertices = pyglet.graphics.vertex_list(
            4, 'v2i', ('c3B', (r, g, b) * 4)
        )

    def onUpdate(self, delta):
        pass

    def onRender(self, delta):
        wpos = self.wpos
        t = self.view.transform(Transform(wpos.x, wpos.y, self.w, self.h))

        x, y, w, h = int(t.x), int(t.y), int(t.w), int(t.h)

        self.vertices.vertices =\
            [x, y] + [x + w, y] + [x + w, y + h] + [x, y + h]

        self.vertices.draw(pyglet.gl.GL_QUADS)


# class CircleComponent(Component):
#     def __init__(self, radius: float = 5, n: int = 6, x=0, y=0, parent=None):
#         super().__init__(pos=(x, y), parent=parent, view=view)

#         self.radius = radius
#         self.n = n

#     def onRender(self, delta):

#         pos = self.spos

#         verts = []
#         colors = []

#         for i in range(0, self.n):

#             verts.extend([
#                 (math.sin((i / self.n) * 2 * math.pi) * self.radius) + pos.x,
#                 (math.cos((i / self.n) * 2 * math.pi) * self.radius) + pos.y
#             ])

#             colors.extend([255, 0, 0])  # red

#         print(f'rendering circle at ({ pos.x }, { pos.y }))')
#         pyglet.graphics.draw(self.n, pyglet.gl.GL_LINE_LOOP,
#                              ('v2f', tuple(verts)), ('c3B', tuple(colors)))


class Text(Component):

    def __init__(self, text: str = '', x=0, y=0, parent=None, view=None):
        super().__init__(pos=(x, y), parent=parent, view=view)

        self.handle = pyglet.text.Label(
            text,
            font_name='Consolas',
            font_size=12,
            x=0, y=0
        )
        self.text = text

    @property
    def text(self):
        return self.handle.text

    @text.setter
    def text(self, text: str):
        self.handle.text = text

    def onRender(self, delta):
        self.handle.x = self.pos.x
        self.handle.y = self.pos.y

        self.handle.draw()


class FpsDisplay(Component):

    def __init__(self, game, x=0, y=0, *, parent=None, view=None):
        super().__init__(pos=(x, y), parent=parent, view=view)

        self.text = Text()
        self.addComponent(self.text)
        self.game = game

        self.deltas = []

    def onRender(self, delta):

        if delta > 0:
            self.deltas.append(delta)

        if len(self.deltas) > 60:
            del self.deltas[0]

        if len(self.deltas) == 0:
            avg_delta = 0
            min_delta = 0
            max_delta = 0
        else:
            avg_delta = float(sum(self.deltas) / len(self.deltas))
            min_delta = min(self.deltas)
            max_delta = max(self.deltas)

        if avg_delta == 0:
            fps = 0
        else:
            fps = 1.0 / avg_delta

        if max_delta == 0:
            fps_l = str(0)
        else:
            fps_l = str(round(1.0 / max_delta, 2))

        if min_delta == 0:
            fps_h = str(0)
        else:
            fps_h = str(round(1.0 / min_delta, 2))

        self.text.text =\
            'FPS: ' + str(round(fps, 2)) +\
            f'(min: { fps_l }, max: { fps_h } )\n' +\
            'cmps: ' + str(self.game.scene.component_count) + '\n' +\
            'ents: ' + str(self.game.scene.entity_count) + '\n'


class Console(Component):
    def __init__(self, game, view=None):
        super().__init__(pos=(20, 20), parent=None, view=view)

        self.document = pyglet.text.document.FormattedDocument()

        self.layout = pyglet.text.layout.TextLayout(
            self.document, width=80, height=720,
            multiline=True, wrap_lines=False
        )
        self.layout.x = 20
        self.layout.y = game.height - 20
        self.layout.anchor_y = 'top'

        self.lines = []

    def log(self, message):
        print(message)
        self.lines.append(message)
        self.document.text = '\n'.join(self.lines)
        self.document.set_style(
            0, len(self.document.text),
            dict(
                font_name='Consolas', font_size=8,
                color=(0, 255, 0, 255), background_color=(0, 0, 0, 200)
            )
        )

    def onRender(self, delta):
        self.layout.draw()
