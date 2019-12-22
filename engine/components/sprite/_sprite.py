
from __future__ import annotations
import pyglet

from typing import TYPE_CHECKING, Optional

from engine.objects.component import BatchComponent
from structs.vector import Vector

if TYPE_CHECKING:
    from engine.asset.image import ImageAsset


class Sprite(BatchComponent):

    def on_spawn(self, image: ImageAsset, scale: float = 1, layer: int = 0):
        """
        A sprite object. These are loaded from an image.

        Args:
            img ([type]): the image to use
            batch ([type], optional): the pyglet batch to render this sprite.
                                      Defaults to None.
        """

        group = self.scene.batch.groups[layer]
        batch = self.scene.batch.pyglet_batch

        self._image = image.pyglet_image
        self._sprite = pyglet.sprite.Sprite(img=self._image,
                                            batch=batch,
                                            group=group)

        if scale != 1:
            self.pyglet_sprite.scale = scale

        # offset of position due to inverse scaling
        self._offset = Vector(0, 0)

        self.is_flipped_x = False
        self.is_flipped_y = False

        # texture coordinates
        self._s, self._t = (0, 1), (0, 1)

        self.update_position()

    @property
    def image(self) -> ImageAsset:
        return self._image

    @image.setter
    def image(self, image: ImageAsset):
        self._image = image
        self._sprite.image = image.pyglet_image
        self.update_tex_coords()

    @property
    def width(self) -> int:
        return self._sprite.width

    @property
    def height(self) -> int:
        return self._height

    def set_tex_coords(self, s: tuple, t: tuple):
        assert isinstance(s, tuple) and isinstance(t, tuple)
        self._s = s
        self._t = t
        self.update_tex_coords()

    def update_tex_coords(self):

        s, t = self._s, self._t

        self._sprite._vertex_list.tex_coords = [
            s[0], t[0], 0,
            s[1], t[0], 0,
            s[1], t[1], 0,
            s[0], t[1], 0,
        ]

    def flip_x(self, flipped: Optional[bool] = None):

        flipped = not self.is_flipped_x if flipped is None else flipped

        if flipped is not self.is_flipped_x:
            self._sprite.scale_x *= -1
            self.is_flipped_x = flipped
            self.on_position_change()

    def flip_y(self, flipped: Optional[bool] = None):

        flipped = not self.is_flipped_y if flipped is None else flipped

        if flipped is not self.is_flipped_y:
            self._sprite.scale_y *= -1
            self.is_flipped_y = flipped
            self.update_position()

    def update_position(self):

        adj_pos = self.position + self.offset
        self._sprite.update(x=adj_pos.x, y=adj_pos.y)

    @property
    def offset(self) -> Vector:
        x, y = tuple(self._offset)
        if self.is_flipped_x: x *= -1
        if self.is_flipped_y: y *= -1
        return Vector(x, y)

    @offset.setter
    def offset(self, offset: tuple):
        self._offset = offset
        self.update_position()

    def set_scale(self, n: float):
        """
        Sets the scale of the sprite.
        """
        self._sprite.scale_x = n
        self._sprite.scale_y = n
        self.update_position()

    def set_scale_x(self, n: float):
        """
        Sets the scale of the sprite.
        """
        self._sprite.scale_x = n
        self.update_position()

    def set_scale_y(self, n: float):
        """
        Sets the scale of the sprite.
        """
        self._sprite.scale_y = n
        self.update_position()

    def on_position_change(self):

        self.update_position()

    def on_set_visible(self):

        self._sprite.visible = True

    def on_set_hidden(self):

        self._sprite.visible = False

    def on_destroy(self):

        self._sprite.delete()
