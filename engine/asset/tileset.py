
from __future__ import annotations

import pyglet
from engine.asset.image import ImageAsset
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.scene import Scene


class TilesetAsset(ImageAsset):

    def __init__(self, path: str, tile_width: int, tile_height: int = None):
        """
        Loads an image as a sprite sheet.

            :param str path: The path to the image
            :param int w:    The width of each sprite
            :param int h:    The height of each sprite
        """
        super().__init__(path)

        # the list of subimages
        self.tiles: List[ImageAsset] = []

        # if height is not given, use same value as width
        tile_height = tile_width if tile_height is None else tile_height

        self._height, self._width = tile_height, tile_width
        width, height = self.pyglet_image.width, self.pyglet_image.height

        for j in range(height // tile_height - 1, -1, -1):
            for i in range(0, width // tile_width):

                tile = self.pyglet_image.get_region(
                    i * tile_width, j * tile_height,  # position of tile
                    tile_width, tile_height           # size of tile
                )

                # set texture parameter to use "nearest" filter
                tile.get_texture()
                pyglet.gl.glTexParameteri(
                    pyglet.gl.GL_TEXTURE_2D,
                    pyglet.gl.GL_TEXTURE_MAG_FILTER,
                    pyglet.gl.GL_NEAREST
                )

                self.tiles.append(ImageAsset(tile))

    @property
    def length(self):
        """
        Return the amount of tiles in this tileset.
        """
        return len(self.tiles)

    @property
    def height(self):
        """ The height of the sprites in this sprite sheet. """
        return self._height

    @property
    def width(self):
        """ The width of the sprites in this sprite sheet. """
        return self._width

    def get_tile(self, key) -> ImageAsset:
        """ Retrieves an image from this sheet by index. """
        return self.tiles[key]

    def __getitem__(self, key) -> ImageAsset:
        """ Retrieves a sprite from this sprite sheet by index. """
        return self.get_tile(key)

    def __iter__(self) -> List[ImageAsset]:
        """
        Convert this tileset into a list of images.

        Returns:
            List[ImageAsset]: a list of images
        """
        yield from self.tiles
