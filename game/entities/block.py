
from engine.components.debug import BoxComponent
from engine.components.shapes import BoxBatch, Box
from engine.component import Component, spawnable
from engine.entity import Entity
from structs.color import Color


# class Block(Component):

#     def __init__(self, x=0, y=0, view=None):
#         super().__init__(x, y, view=view)

#         color = Color(0, 255, 150)
#         darker = color.brightness(0.7)

#         self.addComponent(
#             BoxComponent(0, 0, 32, 32, color.r, color.g, color.b),
#             BoxComponent(2, 2, 28, 28, 
#               int(darker.r), int(darker.g), int(darker.b))
#         )


class Block(Entity):

    @spawnable
    def __init__(self, color, size: tuple):
        color_1 = Color(255, 255, 0)
        color_2 = color.brightness(0.7)

        self.box_1: Box = self.spawnComponent(Box, self.pos, size, color_1)
        self.box_2: Box = self.spawnComponent(
            Box, self.pos + (1, 1),
            (size[0] - 2, size[1] - 2), color_2
        )

    @property
    def color(self):
        return self.box_1.color

    @color.setter
    def color(self, color: Color):
        self.box_1.color = color
        self.box_2.color = color.brightness(0.7)


class BlockGrid(Entity):

    def __init__(self, pos):
        super().__init__(pos=pos)

        self.i = 0
        self.j = 0
        self.ticks = 0

        self.n = 0  # number of blocks rendering

        self.batch = BoxBatch()
        self.addComponent(self.batch)

    def addBlock(self, x, y):
        color = Color(0, 255, 150)
        darker = color.brightness(0.7)

        self.batch.addSquare((x, y), (32, 32), color)
        self.batch.addSquare((x + 2, y + 2), (28, 28), darker)

    def onUpdate(self, delta):
        i, j = self.i, self.j
        self.ticks += 1

        if self.ticks > 10 and self.n < 50:
            self.ticks -= 10

            self.addBlock(i * 32, j * 32)
            self.n += 1
            self.i += 1

            if self.i > 10:
                self.i = 0
                self.j += 1
