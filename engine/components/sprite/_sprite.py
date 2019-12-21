
from __future__ import annotations
import pyglet

from typing import TYPE_CHECKING, Optional

from engine.objects.component import BatchComponent
from structs.vector import Vector

if TYPE_CHECKING:
    from engine.asset.image import ImageAsset

PygletSprite = pyglet.sprite.Sprite


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

        self.pyglet_sprite = PygletSprite(
            img=self._image.pyglet_image,
            x=self.position.x, y=self.position.y,
            batch=self.scene.batch.pyglet_batch,
            group=self.scene.batch.groups[layer]
        )

        if scale != 1:
            self.pyglet_sprite.scale = scale

        # offset of position due to inverse scaling
        self._offset = Vector(0, 0)

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

    def flip_x(self, flipped: Optional[bool] = None):

        flipped = not self.is_flipped_x if flipped is None else flipped

        if flipped is not self.is_flipped_x:
            self.pyglet_sprite.scale_x *= -1
            self.is_flipped_x = flipped
            self.on_position_change()

    def flip_y(self, flipped: Optional[bool] = None):

        flipped = not self.is_flipped_y if flipped is None else flipped

        if flipped is not self.is_flipped_y:
            self.pyglet_sprite.scale_y *= -1
            self.is_flipped_y = flipped
            self.on_position_change()

    @property
    def offset(self) -> Vector:
        x, y = tuple(self._offset)
        if self.is_flipped_x: x *= -1
        if self.is_flipped_y: y *= -1
        return Vector(x, y)

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

        adj_pos = self.position + self.offset
        self.pyglet_sprite.update(x=adj_pos.x, y=adj_pos.y)
        # self.pyglet_sprite.draw()

    def on_set_visible(self):

        self.pyglet_sprite.visible = True

    def on_set_hidden(self):

        self.pyglet_sprite.visible = False
