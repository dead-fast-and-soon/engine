import pyglet

window = pyglet.window.Window(vsync=False)
batch = pyglet.graphics.Batch()


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
        batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None,
                          [0, 1, 2, 0, 2, 3],
                          ('v2i', (10 + x, 10 + x,
                                   15 + x, 10 + x,
                                   15 + x, 15 + x,
                                   10 + x, 15 + x))
                          )

while True:
        window.switch_to()
        window.dispatch_events()
        window.clear()
        batch.draw()
        '''
        for x in range(0, 100):
                squaresWithTriangles()
        '''
        window.flip()
pyglet.app.run()
