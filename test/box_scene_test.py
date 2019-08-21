"""
A graphics test using multiple boxes in order to test performance.
"""

import math

from engine.component import SceneComponent
from engine.components.shapes import Box
from engine.game import Game

from structs.color import Color


class BoxGeneratorComponent(SceneComponent):
    """An example component."""

    @SceneComponent.implicit_super  # skips need to manually call super()
    def __init__(self):
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

    # overridden from SceneComponent
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
scene = game.newScene()
scene.spawnComponent(BoxGeneratorComponent, (0, 0))

# create new camera
camera = game.addCamera()
camera.assignScene(scene)

# start game
print('starting game')
game.start()
