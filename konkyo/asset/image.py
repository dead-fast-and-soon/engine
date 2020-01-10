"""
Contains image-related assets.
"""

from pyglet.image import AbstractImage, TileableTexture, load


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
        self.pyglet_image: AbstractImage = None
        if type(path_or_image) is str:
            self.pyglet_image = load(path_or_image)
        elif isinstance(path_or_image, AbstractImage):
            self.pyglet_image = path_or_image
        else:
            raise ValueError('image must be a path or a pyglet image')


class TileableImageAsset():
    """
    A wrapper class for images loaded using Pyglet.
    """

    def __init__(self, image_asset: ImageAsset):
        """
        Loads an image asset.

        Args:
            path_or_image (str): the path to the image
        """
        self.pyglet_image = (TileableTexture
                             .create_for_image(image_asset.pyglet_image))
