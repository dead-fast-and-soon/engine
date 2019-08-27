"""
A test of the block-based combat game idea.
"""

import math
import pyglet
import pyglet.window.key as key

from typing import cast

from engine.components.debug import Console
from engine.components.shapes import Box
from engine.component import SceneComponent
from engine.entity import Entity
from engine.camera import PixelCamera
from engine.game import Game
from engine.game.scene import Scene

from structs.point import Point
from structs.color import Color

BLOCK_SIZE = 8  # in pixels


class BackgroundComponent(SceneComponent):

    @SceneComponent.implicit_super
    def __init__(self, size: tuple):

        color_1 = Color(20, 20, 20)
        color_2 = Color(40, 40, 40)

        ctr = Point((BLOCK_SIZE * size[0]) // -2, (BLOCK_SIZE * size[1]) // -2)

        color = color_1

        for i in range(0, size[0]):  # x-range
            for j in range(0, size[1]):  # y-range

                pos = ctr + Point(i * BLOCK_SIZE, j * BLOCK_SIZE)

                self.spawnComponent(
                    Box, tuple(pos),
                    size=(BLOCK_SIZE, BLOCK_SIZE), color=color
                )

                color = color_2 if color is color_1 else color_1


class BlockEntity(Entity):

    @Entity.implicit_super
    def __init__(self):

        color = Color(64, 163, 239)  # sky-blueish

        self.block = self.spawnComponent(
            Box, tuple(self.pos),
            size=(BLOCK_SIZE, BLOCK_SIZE), color=color
        )

        self.block.pos = self.pos - Point(BLOCK_SIZE // 2, BLOCK_SIZE // 2)

        self.dir_x = 0
        self.dir_y = 0

        # grid coordinates of block
        self.stun_ticks = 0

    def onUpdate(self, delta: float):

        # print(f'{self.dir_x}, {self.dir_y}')

        if self.stun_ticks == 0:
            self.pos += (self.dir_x * BLOCK_SIZE, self.dir_y * BLOCK_SIZE)
            self.stun_ticks = 8

        else:
            self.stun_ticks -= 1

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
        # self.block.pos = self.pos - Point(BLOCK_SIZE // 2, BLOCK_SIZE // 2)
        pass


class CombatScene(Scene):

    # overridden from Scene
    def onLoad(self):

        self.ticks = 0  # accumulate total ticks

        self.spawnComponent(BackgroundComponent, (0, 0), (15, 9))
        self.spawnComponent(BlockEntity, (0, 0))

    # overridden from Scene
    def onUpdate(self, delta: float):

        self.ticks += 1


# configure game window
game = Game(width=1280, height=720)

# spawn entities
# scene = game.loadScene(CombatScene)
scene = game.createScene()
console: Console = scene.spawnComponent(Console, (0, 0))

console.log('test')
game.log('test')

# create new camera
camera = game.createCamera(PixelCamera, zoom=4)
camera.assignScene(scene)

# ticks = 0


# def updateCamera(delta: float):
#     global ticks
#     camera.focus = Point(
#         math.sin(ticks * 0.1) * 100,
#         math.cos(ticks * 0.1) * 100
#     )
#     ticks += 1

# pyglet.clock.schedule_interval(updateCamera, 1.0 / 60.0)

# scene.render = profile(scene.render)
# game.start = profile(game.start)
# camera.renderScene = profile(camera.renderScene)

# start game
print('starting game')
game.start()
