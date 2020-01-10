
import curses
import math

import numpy as np
import pyglet

from konkyo.asset.image import ImageAsset
from konkyo.asset.tileset import TilesetAsset
from konkyo.camera import OrthoCamera, HUDCamera
from konkyo.components.shapes import Shape2D
from konkyo.components.sprite import Sprite
from konkyo.components.text import Text
from konkyo.game import Game
from konkyo.utils.gl import *
# from game.graphics.shaders import program
from game.entities.player import Player


WIDTH, HEIGHT = 160 * 4, 144 * 4

game = Game(width=WIDTH, height=HEIGHT)
image = ImageAsset('assets/kris.png')
tileset = TilesetAsset('assets/kris.png', 16, 16)

scene = game.create_scene()
scene.use_camera(OrthoCamera, zoom=4)

player = scene.spawn_entity(Player, (0, 0))
# scene.spawn_component(Shape2D, (100, 100), points=[
    # (0, 0), (40, 72), (80, 0), (0, 0)
# ])
sprite = scene.spawn_component(Sprite, (16, 16), tileset[0], 1)

# scene.spawn_component(Text, (0, 0), 'test')
# scene.batch.add_indexed(3, pyglet.gl.GL_TRIANGLES, [0, 1, 2],
            # ("vertices2f", (0, 0, 40, 72, 80, 0)),
            # ("colors3B", (255, 255, 255) * 3))

screen = None
# screen = curses.initscr()
@game.event_listener
def on_update(delta):
    if screen:
        screen.clear()

        print(game.fps_disp.text.__dict__)

        lines = [
            f'pos: { player.position.ceil()}',
            f'grid: { player.grid_pos }',
            f'fps: { round(1 / delta, 2) }',
            f'text pos: { game.fps_disp.position }',
        ]

        for i, line in enumerate(lines):
            screen.addstr(i, 0, line)

        screen.refresh()


glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

buffer_id = sprite._sprite.group.program.uniform_buffers['WindowBlock'].buffer.id
print(buffer_id)
# player_program = player.sprite.sprite._sprite.group.program
# print(player_program._uniform_blocks['WindowBlock'].index)
# glUniformBlockBinding(player_program.id, 0, 0)

# uni_buffer = GLUniformBuffer(buffer_id)
# uni_buffer.set_binding_point(0)

# proj = glm.ortho(
#     (-WIDTH / 2) / 4,
#     (+WIDTH / 2) / 4,
#     (-HEIGHT / 2) / 4,
#     (+HEIGHT / 2) / 4
# )
# view = glm.mat4(1.0)

# with uni_buffer:
#     uni_buffer.sub_data(0, proj)
#     uni_buffer.sub_data(glm.sizeof(glm.mat4), view)

# print(np.array(proj, ndmin=1))
# with program.uniform_buffers['MVP'] as mvp:
#     mvp.projection[:] = np.array(proj).flatten()
#     mvp.view[:] = np.array(view).flatten()

game.start()
