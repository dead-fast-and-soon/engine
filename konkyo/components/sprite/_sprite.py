
from __future__ import annotations
import pyglet

from typing import TYPE_CHECKING, Optional

from konkyo.components.shapes import Box2D
from konkyo.objects.component import BatchComponent
from konkyo.structs.vector import Vector
import konkyo.utils.gl as gl
from konkyo.graphics.palette import ColorPalette
from konkyo.components.sprite._shaders import make_program

if TYPE_CHECKING:
    from konkyo.asset.image import ImageAsset
    from pyglet.graphics.shader import ShaderProgram


class _SpriteGroup(pyglet.sprite.SpriteGroup):
    def __init__(self, image: ImageAsset, palette):
        super().__init__(image.pyglet_image.get_texture(),
                         pyglet.gl.GL_SRC_ALPHA,
                         pyglet.gl.GL_ONE_MINUS_SRC_ALPHA,
                         make_program())
        self.palette = palette
        self.set_image(image)

    def set_image(self, image: ImageAsset):
        self.img_texture = image.pyglet_image.get_texture()

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.img_texture.id)
        gl.glTexParameteri(gl.GL_TEXTURE_2D,
                           gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D,
                           gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

    def set_state(self):
        self.program.use_program()

        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.img_texture.id)

        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.palette.id)

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def unset_state(self):
        gl.glDisable(gl.GL_BLEND)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

        self.program.stop_program()


class Sprite(BatchComponent):

    def on_spawn(self, image: ImageAsset, scale: float = 1, layer: int = 0,
                 color: tuple = (255, 255, 255), palette: ColorPalette = None,
                 anchor: tuple = None):
        """
        A sprite object. These are loaded from an image.

        Args:
            image (ImageAsset): the image to use
            palette_colors (tuple): a tuple of colors (in RGBA float) to use
                as a color table for this sprite
        """

        self._image = image.pyglet_image

        anchor = anchor or (0, 0)

        self._anchor_x = int(self._image.width * anchor[0])
        self._anchor_y = int(self._image.height * anchor[1])
        # self._image.anchor_x = self._anchor_x
        # self._image.anchor_y = self._anchor_y
        print('using anchor {}, {}'.format(self._anchor_x, self._anchor_y))

        self._layer = layer
        batch = self.scene.batch.pyglet_batch

        self.palette = palette
        if self.palette:
            self._group = _SpriteGroup(image, self.palette)
        else:
            self._group = None

        self._sprite = pyglet.sprite.Sprite(
            img=self._image,
            batch=batch,
            group=self._group
        )

        # force nearest filter
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._image.get_texture().id)
        self.color = color

        if scale != 1:
            self._sprite.scale = scale

        self.is_flipped_x = False
        self.is_flipped_y = False

        # texture coordinates
        self._s, self._t = (0, 1), (0, 1)

        self._wireframe = None

        self.update_position()

    @property
    def shaders(self) -> ShaderProgram:
        """
        Get the shader program used by this sprite.
        """
        return self._sprite._group.program

    @property
    def image(self) -> ImageAsset:
        return self._image

    @image.setter
    def image(self, image: ImageAsset):
        self._image = image
        # self._image.pyglet_image.anchor_x = self._anchor_x
        # self._image.pyglet_image.anchor_y = self._anchor_y
        if self._group:
            self._group.set_image(image)
        else:
            self._sprite.image = image.pyglet_image
        self.update_tex_coords()

    @property
    def width(self) -> int:
        return self._sprite.width

    @property
    def height(self) -> int:
        return self._sprite.height

    @property
    def color(self) -> tuple:
        return self._sprite.color

    @color.setter
    def color(self, color: tuple):
        self._sprite.color = color

    def toggle_wireframe(self):
        if self._wireframe is None:
            self._wireframe = self.create_component(Box2D, self.position,
                                                    (self.width, self.height),
                                                    is_filled=False,
                                                    layer=self._layer)
            self.is_visible = False
        else:
            self.destroy_component(self._wireframe)
            self._wireframe = None
            self.is_visible = True

    def set_tex_coords(self, s: tuple, t: tuple):
        assert isinstance(s, tuple) and isinstance(t, tuple)
        self._s = s
        self._t = t
        self.update_tex_coords()

    def update_tex_coords(self):
        s, t = self._s, self._t
        self._sprite._vertex_list.tex_coords[:] = [
            s[0], t[0], 0,
            s[1], t[0], 0,
            s[1], t[1], 0,
            s[0], t[1], 0,
        ]

    def flip_x(self, flipped: Optional[bool] = None):
        if flipped is None:
            flipped = not self.is_flipped_x

        if flipped:
            self._s = (1, 0)
        else:
            self._s = (0, 1)

        self.is_flipped_x = flipped
        self.update_tex_coords()

    def flip_y(self, flipped: Optional[bool] = None):
        if flipped is None:
            flipped = not self.is_flipped_y

        if flipped:
            self._t = (1, 0)
        else:
            self._t = (0, 1)

        self.is_flipped_y = flipped
        self.update_tex_coords()

    @property
    def _adjusted_position(self):
        # FIXME: position acting strangely with negative scales
        return self.position - (self._anchor_x * self._sprite.scale_x,
                                self._anchor_y * self._sprite.scale_y)

    def update_position(self):
        adj_pos = self._adjusted_position
        # adj_pos = self.position
        self._sprite.update(x=adj_pos.x, y=adj_pos.y)

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

