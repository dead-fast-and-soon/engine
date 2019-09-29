"""
A test of the block-based combat game idea.
"""

import math
import pyglet
import pyglet.window.key as key

from typing import cast

from engine.components.debug import Console, Text
from engine.components.shapes import Box
from engine.component import SceneComponent
from engine.entity import Entity
from engine.camera import PixelCamera
from engine.game import Game
from engine.game.scene import Scene

from structs.vector import Vector
from structs.color import Color

BLOCK_SIZE = 8  # in pixels

SELECT_AREA = 5  # select phase area
SELECT_POS_L = Vector(-85, 0)
SELECT_POS_R = Vector(85, 0)


class BackgroundComponent(SceneComponent):

    @SceneComponent.implicit_super
    def __init__(self, size: tuple):

        color_1 = Color(20, 20, 20)
        color_2 = Color(40, 40, 40)

        ctr = Vector((BLOCK_SIZE * size[0]) // -2, (BLOCK_SIZE * size[1]) // -2)

        color = color_1

        for i in range(0, size[0]):  # x-range
            for j in range(0, size[1]):  # y-range

                pos = ctr + Vector(i * BLOCK_SIZE, j * BLOCK_SIZE) + self.pos

                self.spawnComponent(
                    Box, tuple(pos),
                    size=(BLOCK_SIZE, BLOCK_SIZE), color=color
                )

                color = color_2 if color is color_1 else color_1


class Cursor(Entity):

    @Entity.implicit_super
    def __init__(self):

        color = Color(64, 163, 239)  # sky-blueish

        self.origin = SELECT_POS_L
        self.block = self.spawnComponent(

            Box, tuple(self.origin + self.pos),
            size=(BLOCK_SIZE, BLOCK_SIZE), color=color
        )

        self.grid_pos = Vector(0, 0)

        self.selected_coords = [self.grid_pos]

        self.dir_x = 0
        self.dir_y = 0

        # grid coordinates of block
        self.stun_ticks = 0

    def update_position(self):
        """Update block position based on block_pos"""

        self.block.pos = self.origin + Vector(
            (self.grid_pos.x - (1 / 2)) * BLOCK_SIZE,
            (self.grid_pos.y - (1 / 2)) * BLOCK_SIZE
        )

    def onUpdate(self, delta: float):

        # print(f'{self.dir_x}, {self.dir_y}')
        global console

        if self.stun_ticks == 0:
            self.grid_pos += (self.dir_x, self.dir_y)
            self.selected_coords.append(self.grid_pos)
            self.stun_ticks = 8

            self.update_position()
        else:
            self.stun_ticks -= 1

        console.line(0, 'pos: ' + str(tuple(self.grid_pos)))
        console.line(1, 'select: ' + str(self.selected_coords))

    def onKeyPress(self, k: int, mod):
        if k is key.UP:
            if self.dir_y == -1:
                self.dir_y = 0
            else:
                self.dir_y = 1

        elif k is key.DOWN:
            if self.dir_y == 1:
                self.dir_y = 0
            else:
                self.dir_y = -1

        elif k is key.RIGHT:
            if self.dir_x == -1:
                self.dir_x = 0
            else:
                self.dir_x = 1

        elif k is key.LEFT:
            if self.dir_x == 1:
                self.dir_x = 0
            else:
                self.dir_x = -1

    def onKeyRelease(self, k: int, mod):
        if k is key.UP:
            if self.dir_y == 1:
                self.dir_y = 0
            else:
                self.dir_y = -1

        elif k is key.DOWN:
            if self.dir_y == -1:
                self.dir_y = 0
            else:
                self.dir_y = 1

        elif k is key.RIGHT:
            if self.dir_x == 1:
                self.dir_x = 0
            else:
                self.dir_x = -1

        elif k is key.LEFT:
            if self.dir_x == -1:
                self.dir_x = 0
            else:
                self.dir_x = 1

    def onPositionChange(self):
        # shift block position to be center on entity position
        # self.block.pos = self.pos - Vector(BLOCK_SIZE // 2, BLOCK_SIZE // 2)
        pass


class CombatScene(Scene):

    # overridden from Scene
    def onLoad(self):

        self.ticks = 0  # accumulate total ticks

        self.spawnComponent(BackgroundComponent, (0, 0), (15, 9))
        self.spawnComponent(BackgroundComponent, SELECT_POS_L, (5, 5))
        self.spawnComponent(Cursor, (0, 0))

    # overridden from Scene
    def onUpdate(self, delta: float):

        self.ticks += 1


# configure game window
game = Game(width=1280, height=720)

# spawn entities
scene = game.loadScene(CombatScene)
# scene = game.createScene()

# create new camera
camera = game.createCamera(PixelCamera, zoom=4)
camera.assignScene(scene)

hud_scene = game.createScene()
console = hud_scene.spawnComponent(Console, (-640, 320), 800, 320)

hud_cam = game.createCamera(PixelCamera)
hud_cam.assignScene(hud_scene)

# game.log("test")

# ticks = 0


# def updateCamera(delta: float):
#     global ticks
#     camera.focus = Vector(
#         math.sin(ticks * 0.1) * 100,
#         math.cos(ticks * 0.1) * 100
#     )
#     ticks += 1

# pyglet.clock.schedule_interval(updateCamera, 1.0 / 60.0)

# scene.render = profile(scene.render)
# game.start = profile(game.start)
# camera.renderScene = profile(camera.renderScene)

print('cameras:')
for camera in game.cameras:
    print('    ' + str(camera))

print('scenes: ')
for scene in game.scenes:
    print('    ' + str(scene))

# start game
print('starting game')
game.start()
