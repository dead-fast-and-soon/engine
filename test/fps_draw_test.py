import pyglet
import time

from engine.components.debug import FpsDisplay
from engine.components.shapes import QuadBatch
from engine.camera import Camera

window = pyglet.window.Window(vsync=False)

batch = pyglet.graphics.Batch()

quads = QuadBatch()

def squaresWithQuads():
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_QUADS,
                                     [0, 1, 2, 3],
                                     ('v2i', (100, 100,
                                              150, 100,
                                              150, 150,
                                              100, 150))
                                     )


def squaresWithTriangles():
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                     [0, 1, 2, 0, 2, 3],
                                     ('v2i', (100, 100,
                                              150, 100,
                                              150, 150,
                                              100, 150))
                                     )

for x in range(0, 100):
        # batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
        #                   [0, 1, 2, 0, 2, 3],
        #                   ('v2i', (10 + x, 10 + x,
        #                            15 + x, 10 + x,
        #                            15 + x, 15 + x,
        #                            10 + x, 15 + x))
        #                   )
        quads.addQuad(10 + x, 10 + x, 5, 5)

# fps_display = pyglet.window.FPSDisplay(window)
fps_display = FpsDisplay()
last_time = time.perf_counter()
accum_time = 0

while True:

        end_time = time.perf_counter()
        delta = end_time - last_time
        last_time = end_time

        window.switch_to()
        window.dispatch_events()
        window.clear()

        accum_time += delta
        while accum_time > 1.0:
                accum_time -= 1.0
                fps_display.update(1.0)

        # batch.draw()
        quads.render(delta)

        fps_display.render(delta)
        '''
        for x in range(0, 100):
                squaresWithTriangles()
        '''
        window.flip()
pyglet.app.run()
