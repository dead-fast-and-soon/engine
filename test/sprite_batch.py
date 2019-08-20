import pyglet

window = pyglet.window.Window(vsync=False)
batch = pyglet.graphics.Batch()

frame_image = pyglet.image.load('frame1.png')
frame_sprites = []
for i in range(100):
        x, y = i * 10, 50
        frame_sprites.append(pyglet.sprite.Sprite(frame_image, x, y, 
                                                  batch=batch))


def nonBatchSprites():
        pass

while True:
        window.switch_to()
        window.dispatch_events()
        window.clear()
        "Draw Logic Start"

        batch.draw()

        "Draw Logic End"
        window.flip()
