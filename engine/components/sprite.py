import pyglet
from pyglet import image, gl
from engine.component import Component
from engine.components.debug import CircleComponent
from structs.vector import Vector

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.spritesheet import SpriteSheet


class SpriteComponent(Component):

    def __init__(
        self, img, x: float = 0.0, y: float = 0.0,
        *, batch=None, parent=None
    ):
        """ Creates a sprite. """
        super().__init__(x, y, parent)

        if batch is None:
            self.handle = pyglet.sprite.Sprite(img, x, y)
        else:
            self.handle = pyglet.sprite.Sprite(img, x, y, batch=batch)

        # self.addComponent(CircleComponent())

    def setScale(self, n: float):
        """
        Sets the scale of the sprite.

            :param float n: The scale factor
        """
        self.scale = n

    def onRender(self):

        self.handle.x = self.spos.x
        self.handle.y = self.spos.y

        self.handle.scale = self.view.zoom

        self.handle.draw()


class SpriteTextComponent(Component):
    """
    A string of text that is rendered using sprites.
    """

    MAP = {
        'A': 0,  'B': 1,  'C': 2,  'D': 3,  'E': 4,  'F': 5,  'G': 6,
        'H': 7,  'I': 8,  'J': 9,  'K': 10, 'L': 11, 'M': 12, 'N': 13,
        'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20,
        'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25,

        '(': 26, ')': 27, ':': 28, ';': 29, '[': 30, ']': 31,

        'a': 32, 'b': 33, 'c': 34, 'd': 35, 'e': 36, 'f': 37, 'g': 38,
        'h': 39, 'i': 40, 'j': 41, 'k': 42, 'l': 43, 'm': 44, 'n': 45,
        'o': 46, 'p': 47, 'q': 48, 'r': 49, 's': 50, 't': 51, 'u': 52,
        'v': 53, 'w': 54, 'x': 55, 'y': 56, 'z': 57,

        '0': 118, '1': 119, '2': 120, '3': 121, '4': 122, '5': 123, '6': 124,
        '7': 125, '8': 126, '9': 127,

        '#': 97, '%': 98,  # mini PK/MN symbols

        '^': 106,  # accented 'e'

        '>': 109  # solid right arrow
    }

    def __init__(self, sheet: SpriteSheet, x: float = 0.0, y: float = 0.0,
                 text: str = '', scale: int = 1, parent=None, view=None):
        """
        Creates text (using a sprite sheet) to be rendered.
        """
        super().__init__(x, y, parent, view)

        # the spacing between each sprite
        self.charSpacing: int = 0

        # the spacing between each line
        self.lineHeight: int = 4

        # the scaling of the text (as int to keep pixel perfect)
        self.scale: int = scale

        # location marker representing current line and column
        self.loc: Vector = Vector(0, 0)

        # the sprite sheet currently in use
        self.sheet: SpriteSheet = sheet

        if text != '':
            self.loadText(text)

    def loadText(self, text: str):
        """
        Reads text then loads and positions the respective sprite
        for each character.

        If text was previously loaded, it will be deleted first.
        """

        self.deleteChildren()

        line, col = 0, 0

        for char in list(str(text)):  # convert text to str first for safety

            if char == '\n':  # newline
                line -= 1  # shift position down
                col = 0  # reset position to original x coordinate

            elif char == ' ':
                col += 1

            else:
                i = self.MAP.get(char, 0)

                spr = self.sheet[i]
                spr.setScale(self.scale)

                spr.x = ((self.sheet.width + self.charSpacing) * col *
                         self.scale)

                spr.y = ((self.sheet.width + self.lineHeight) * line *
                         self.scale)

                self.addComponent(spr)
                col += 1

        # shift all sprites up to align (0, 0) at bottom left
        self.translateChildren(0, (self.sheet.width + self.lineHeight) * -line)

        print(f'rendering text at ({ self.x }, { self.y })')
