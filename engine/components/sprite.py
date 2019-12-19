
from __future__ import annotations

import pyglet
from typing import List, TYPE_CHECKING

from engine.objects.component import BatchComponent
from engine.asset.image import ImageAsset
from structs.vector import Vector

if TYPE_CHECKING:
    from engine.asset.tileset import TilesetAsset


class Sprite(BatchComponent):

    def on_spawn(self, image: ImageAsset, scale: float = 1, layer: int = 0):
        """
        A sprite object. These are loaded from an image.

        Args:
            img ([type]): the image to use
            batch ([type], optional): the pyglet batch to render this sprite.
                                      Defaults to None.
        """
        self._image = image

        self.pyglet_sprite = pyglet.sprite.Sprite(
            self._image.pyglet_image,
            x=self.position.x, y=self.position.y,
            batch=self.scene.batch.pyglet_batch,
            group=self.scene.batch.groups[layer]
        )

        if scale != 1:
            self.pyglet_sprite.scale = scale

        # offset of position due to inverse scaling
        self._offset = (0, 0)

        self.is_flipped_x = False
        self.is_flipped_y = False

    @property
    def image(self) -> ImageAsset:
        return self._image

    @image.setter
    def image(self, image: ImageAsset):
        self._image = image
        self.pyglet_sprite.image = image.pyglet_image

    @property
    def width(self) -> int:
        return self.pyglet_sprite.width

    @property
    def height(self) -> int:
        return self.pyglet_sprite.height

    def flip_x(self):
        self.pyglet_sprite.scale_x *= -1
        self.is_flipped_x = not self.is_flipped_x
        self.on_position_change()

    def flip_y(self):
        self.pyglet_sprite.scale_y *= -1
        self.is_flipped_y = not self.is_flipped_y
        self.on_position_change()

    @property
    def offset(self) -> list:
        offset = list(self._offset[::])
        if self.is_flipped_x: offset[0] *= -1
        if self.is_flipped_y: offset[1] *= -1
        return offset

    @offset.setter
    def offset(self, offset: tuple):
        self._offset = offset
        self.on_position_change()

    def set_scale(self, n: float):
        """
        Sets the scale of the sprite.

            :param float n: The scale factor
        """
        self.pyglet_sprite.scale = n

    def on_position_change(self):

        offset = self.offset
        self.pyglet_sprite.x = self.position.x + offset[0]
        self.pyglet_sprite.y = self.position.y + offset[1]
        # self.pyglet_sprite.draw()


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

        '>': 109  # solid right arrow
    }

    def on_spawn(self, tileset: TilesetAsset, text: str = '', scale: int = 1,
                 layer: int = 0):
        """
        Creates text (using a sprite sheet) to be rendered.
        """
        # the spacing between each sprite
        self.charSpacing: int = 0

        # the spacing between each line
        self.lineHeight: int = 4

        # the scaling of the text (as int to keep pixel perfect)
        self.scale: int = scale

        # location marker representing current line and column
        self.loc: Vector = Vector(0, 0)

        # the sprite sheet currently in use
        self.sheet: TilesetAsset = tileset

        # the layer to draw this text
        self.layer: int = layer

        if text != '':
            self.loadText(text)

    def loadText(self, text: str):
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

                self.create_component(Sprite, (x, y), tile,
                                      scale=self.scale, layer=self.layer,
                                      name='Sprite {}'.format(char))
                col += 1

        # shift all sprites up to align (0, 0) at bottom left
        self.position += (0, (self.sheet.width + self.lineHeight) * -line)


class AnimatedSprite(BatchComponent):

    def on_spawn(self, frames: List[ImageAsset], frame_duration: float):
        """
        An animated sprite.

        Args:
            frames (List[ImageAsset]): a list of frames to use in this
                                       animation
            frame_duration (float): the duration of each frame of the
                                    animation
        """
        self.frames = frames
        self.sprite = self.create_component(Sprite, self.position,
                                            self.frames[0])
        self.sprite.offset = (-8, -8)  # center image
        self.frame_duration = frame_duration
        self._timer = 0

        self.current_frame = 0

    def next_frame(self) -> ImageAsset:
        """
        Return the next frame in the animation.

        Returns:
            ImageAsset: the next frame in the animation
        """
        next_frame = self.current_frame + 1
        if next_frame >= len(self.frames):
            next_frame = 0
            self.sprite.flip_x()
        self.current_frame = next_frame
        return self.frames[next_frame]

    def on_update(self, delta: float):

        self._timer += delta

        while self._timer >= self.frame_duration:
            self.sprite.image = self.next_frame()
            self._timer -= self.frame_duration
