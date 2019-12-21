"""
Contains image-related assets.
"""

import pyglet


class ImageAsset():
    """
    A wrapper class for images loaded using Pyglet.
    """
    def __init__(self, path_or_image):
        """
        Loads an image asset.

        Args:
            path_or_image (str): the path to the image
        """
        if type(path_or_image) is str:
            self.pyglet_image = pyglet.image.load(path_or_image)
        elif isinstance(path_or_image, pyglet.image.AbstractImage):
            self.pyglet_image = path_or_image
        else:
            raise ValueError('image must be a path or a pyglet image')
