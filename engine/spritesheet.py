
import pyglet
from engine.components.sprite import SpriteComponent
from typing import List


class SpriteSheet:

    def __init__(self, path: str, w: int, h: int = None):
        """
        Loads an image as a sprite sheet.

            :param str path: The path to the image
            :param int w:    The width of the sprite
            :param int h:    The height of the sprite
        """
        self.handle = pyglet.image.load(path)
        self.images: List[pyglet.image.AbstractImage] = []

        # if height is not given, use same value as width
        h = w if h is None else h

        self._height = h
        self._width = w

        for j in range(self.handle.height // h - 1, -1, -1):
            for i in range(0, self.handle.width // w):

                subimg = self.handle.get_region(i * w, j * h, w, h)

                # set texture parameter to use "nearest" filter
                subimg.get_texture()
                pyglet.gl.glTexParameteri(
                    pyglet.gl.GL_TEXTURE_2D,
                    pyglet.gl.GL_TEXTURE_MAG_FILTER,
                    pyglet.gl.GL_NEAREST
                )

                self.images.append(subimg)

    @property
    def height(self):
        """ The height of the sprites in this sprite sheet. """
        return self._height

    @property
    def width(self):
        """ The width of the sprites in this sprite sheet. """
        return self._width

    def getSprite(self, key):
        """ Retrieves a sprite from this sheet by index. """
        return SpriteComponent(self.images[key])

    def getImage(self, key):
        """ Retrieves an image from this sheet by index. """
        return self.images[key]

    def __getitem__(self, key):
        """ Retrieves a sprite from this sprite sheet by index. """
        return self.getSprite(key)
