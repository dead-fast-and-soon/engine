import pyglet
from pyglet import graphics

import math

from engine.component import Component, SceneComponent
from structs.vector import Transform


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


class Text(SceneComponent):

    @SceneComponent.implicit_super
    def __init__(self, text: str = ''):

        self.handle = pyglet.text.Label(
            text,
            font_name='Consolas',
            font_size=12,
            x=self.pos.x, y=self.pos.y,
            batch=self.scene.batch
        )
        self.text = text

    @property
    def text(self):
        return self.handle.text

    @text.setter
    def text(self, text: str):
        self.handle.text = text

    def onPositionChange(self):
        self.handle.x = self.pos.x
        self.handle.y = self.pos.y


class FpsDisplay(SceneComponent):

    @SceneComponent.implicit_super
    def __init__(self):

        self.text: Text = self.spawnComponent(Text, self.pos)

        self.deltas = []
        self.last_frametime = 0

    def onUpdate(self, delta):

        if self.last_frametime > 0:
            fps = str(round(1.0 / self.last_frametime, 2))
        else:
            fps = str(0.0)

        self.text.text = 'FPS: ' + fps

    def onRender(self, delta):

        # if delta > 0:
        #     self.deltas.append(delta)

        # if len(self.deltas) > 10:
        #     del self.deltas[0]

        self.last_frametime = delta


class Console(SceneComponent):

    @SceneComponent.implicit_super
    def __init__(self, width=400, height=720):

        print(f'placing console @({self.pos.x},{self.pos.y})')
        self.document = pyglet.text.document.FormattedDocument()

        self.layout: pyglet.text.layout.TextLayout =\
            pyglet.text.layout.TextLayout(
                self.document, width=None, height=None,
                multiline=True, wrap_lines=False,
                batch=self.scene.batch
            )
        self.layout.x = self.pos.x
        self.layout.y = self.pos.y
        self.layout.anchor_x = 'left'
        self.layout.anchor_y = 'bottom'

        self.lines = []

    def line(self, n, message):
        while n >= len(self.lines):
            self.lines.append('')

        self.lines[n] = message
        self.updateText()

    def log(self, message):
        # print(message)
        self.lines.append(message)
        self.updateText()

    def updateText(self):
        self.document.text = '\n'.join(self.lines)
        self.document.set_style(
            0, len(self.document.text),
            dict(
                font_name='Consolas', font_size=8,
                color=(0, 255, 0, 255), background_color=(0, 0, 0, 200)
            )
        )

    def onPositionChange(self):
        self.layout.x = self.pos.x
        self.layout.y = self.pos.y

    def onRender(self, delta):
        # print("rendering console")
        # self.layout.draw()
        pass
