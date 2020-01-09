
from __future__ import annotations

import typing as t

from konkyo.objects.component import BatchComponent
from konkyo.components.sprite import Sprite
from konkyo.structs.vector import Vector

if t.TYPE_CHECKING:
    from konkyo.asset.image import ImageAsset
    from konkyo.asset.tileset import TilesetAsset


class SpriteText(BatchComponent):
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

        '>': 109,  # solid right arrow

        '\'': 96  # apostrophe
    }

    def on_spawn(self, tileset: TilesetAsset, text: str = '', scale: int = 1,
                 layer: int = 0, line_height: int = 4):
        """
        Creates text (using a sprite sheet) to be rendered.
        """
        # the spacing between each sprite
        self.charSpacing: int = 0

        # the spacing between each line
        self.lineHeight: int = line_height

        # the scaling of the text (as int to keep pixel perfect)
        self.scale: int = scale

        # location marker representing current line and column
        self.loc: Vector = Vector(0, 0)

        # the sprite sheet currently in use
        self.sheet: TilesetAsset = tileset

        # the layer to draw this text
        self.layer: int = layer

        self.sprites: t.List[Sprite] = []

        self._text = text
        if self._text != '':
            self.load_text(self._text)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        for sprite in self.sprites:
            self.destroy_component(sprite)
        self.sprites = []

        if text != '':
            self.load_text(text)

        self._text = text

    def load_text(self, text: str):
        """
        Reads text then loads and positions the respective sprite
        for each character.

        If text was previously loaded, it will be deleted first.
        """
        self.children = []

        line, col = 0, 0

        for char in list(str(text)):  # convert text to str first for safety

            if char == '\n':  # newline
                line -= 1  # shift position down
                col = 0  # reset position to original x coordinate

            elif char == ' ':
                col += 1

            else:
                i = self.MAP.get(char, 0)

                tile: ImageAsset = self.sheet[i]

                x = ((self.sheet.width + self.charSpacing)
                     * col * self.scale + self.position.x)
                y = ((self.sheet.width + self.lineHeight)
                     * line * self.scale + self.position.y)

                sprite = self.create_component(
                    Sprite, (x, y), tile,
                    scale=self.scale, layer=self.layer,
                    name='Sprite {}'.format(char)
                )
                self.sprites.append(sprite)

                col += 1

        # shift all sprites up to align (0, 0) at bottom left
        self.position += (0, (self.sheet.width + self.lineHeight) * -line)

    def on_set_visible(self):

        for sprite in self.sprites:
            sprite.is_visible = True

    def on_set_hidden(self):

        for sprite in self.sprites:
            sprite.is_visible = False
