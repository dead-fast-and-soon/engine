"""
A graphics test using multiple boxes in order to test performance.
"""

import math

from engine.components.shapes import Box
from engine.camera import PixelCamera
from engine.game import Game
from engine.game.scene import Scene

from structs.color import Color


class BoxTestScene(Scene):
    """An example component."""

    # overridden from Scene
    def onLoad(self):

        self.ticks = 0  # accumulate total ticks
        self.boxes = []

        for i in range(0, 1500):
            if i < 750:
                # blue to cyan
                color = Color(0, int(255 * (i / 750)), 255)
            else:
                # cyan to green
                color = Color(0, 255, int(255 * (1 - ((i - 750) / 750))))

            box = self.spawnComponent(
                Box, ((i - 750) * 0.8, 0),
                size=(10, 10), color=color
            )

            self.boxes.append(box)

    # overridden from Scene
    def onUpdate(self, delta: float):

        for i in range(len(self.boxes)):
            box = self.boxes[i]
            box.pos = (  # type: ignore
                box.pos.x,
                math.sin(self.ticks * 0.01 + (i * 0.1)) *
                math.cos(self.ticks * 0.01 + (i * 0.01)) * 200
            )

        self.ticks += 1

# configure game window
game = Game(width=1280, height=720)

# spawn entities
scene = game.loadScene(BoxTestScene)

# create new camera
camera = game.createCamera(PixelCamera)
camera.assignScene(scene)

# start game
print('starting game')
game.start()
