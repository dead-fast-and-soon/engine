
from konkyo.utils.gl import *

__all__ = ['ColorPalette']


def convert_colors(colors: list, bits: int):
    """
    Convert a list of bit formatted colors into a list of
    float-formatted colors.
    """
    max_val = (2 ** bits) - 1
    return [[i / max_val for i in color] for color in colors]


class ColorPalette:
    """
    A GL texture object representing a color table.
    """

    def __init__(self, pixels: list, bits: int = 0):

        if bits > 0:
            pixels = convert_colors(pixels, bits)

        [self._assert_pixel(pixel) for pixel in pixels]

        self.pixels = pixels
        """The colors in this palette"""

        width = len(self.pixels)

        self.id = GLuint()
        """The ID of the GL texture"""

        glGenTextures(1, self.id)

        # print('creating texture with width %d' % width)

        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                     width, 1,  # size of texture
                     0,
                     GL_RGBA, GL_FLOAT, self.get_data())
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

    def _assert_pixel(self, pixel):
        """
        Verify that the given pixel is valid.
        """
        assert len(pixel) == 4, (
            'invalid pixel %s: must have 4 items' % pixel
        )
        assert all(isinstance(i, float) for i in pixel), (
            'invalid pixel %s: all items must be floats' % pixel
        )

    def get_data(self):
        """
        Convert our list of pixels into a C array.
        """
        pixels = self.pixels
        return (c_float * (4 * len(pixels)))(*[i for pixel in pixels for i in pixel])

    def get_sub_data(self, i):
        """
        Convert one of our pixels into a C array.
        """
        pixel = self.pixels[i]
        return (c_float * 4)(*pixel)

    def __getitem__(self, idx):
        return self.pixels[idx]

    def __setitem__(self, idx, color):
        """
        Set one of the colors in this palette.

        Args:
            idx ([type]): the index of the color to set
            value ([type]): the color
        """
        self._assert_pixel(color)
        assert idx < len(self.pixels)

        self.pixels[idx] = color

        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexSubImage2D(GL_TEXTURE_2D, 0,
                        idx, 0,  # xy offset
                        1, 1,    # data width/height
                        GL_RGBA, GL_FLOAT, self.get_sub_data(idx))
        glBindTexture(GL_TEXTURE_2D, 0)
