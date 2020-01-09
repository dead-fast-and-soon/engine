
from __future__ import annotations
import pyglet

from typing import TYPE_CHECKING, Optional

from konkyo.utils.gl import *
from konkyo.objects.component import BatchComponent
from pyglet.graphics.shader import Shader, ShaderProgram
from konkyo.structs.vector import Vector

if TYPE_CHECKING:
    from konkyo.asset.image import ImageAsset


vert = Shader("""#version 420 core
    in vec4 position;
    in vec4 color;
    in vec2 uv;

    out vec4 frag_color;
    out vec2 frag_uv;

    layout(binding = 0) uniform WindowBlock
    {
        mat4 projection;
        mat4 view;
    } window;

    void main()
    {
        gl_Position = window.projection * window.view * position;
        //gl_Position = projection * view * position;

        frag_color = color;
        frag_uv = uv;
    }
""", 'vertex')

frag = Shader("""#version 420 core
    in vec4 frag_color;
    in vec2 frag_uv;

    uniform sampler2D tex;

    out vec4 out_color;

    void main()
    {
        out_color = texture(tex, frag_uv) * frag_color;
    }
""", 'fragment')

program = ShaderProgram(vert, frag)


class SpriteGroup(pyglet.graphics.Group):
    def __init__(self, image: ImageAsset):
        super().__init__(program)
        self.image = image

    def set_state(self):
        self.program.use_program()

        # self.program['projection'] = pyglet.matrix.create_orthogonal(0, 160 * 4, 0, 144 * 4, 0, 1)
        # self.program['view'] = pyglet.matrix.Mat4()

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.image.pyglet_image.get_texture().id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def unset_state(self):
        glDisable(GL_BLEND)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.program.stop_program()


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
        self._group = SpriteGroup(image)

        self.vertex_list = self.scene.batch.pyglet_batch.add_indexed(
            4, pyglet.gl.GL_TRIANGLES, self._group, [0, 1, 2, 0, 2, 3],
            'position3f',
            # FIXME: 'color3B' (255, 255, 255) higher than (1.0, 1.0, 1.0)?
            ('color3f', (1.0, 1.0, 1.0) * 4),
            'uv2f'
        )

        self._scale = scale

        # offset of position due to inverse scaling
        self._offset = Vector(0, 0)

        self.is_flipped_x = False
        self.is_flipped_y = False

        self._scale_x, self._scale_y = 1, 1

        self._width, self._height = self.orig_width, self.orig_height

        # texture coordinates
        self._s, self._t = (0, 1), (0, 1)

        self.update_vertex_data()

    def update_vertex_data(self):
        """
        Update the vertex data for this sprite.
        Call this when changing any property of the sprite.
        """
        adj_pos = self.position + self.offset
        sc_x, sc_y = self._scale_x, self._scale_y
        x, y = adj_pos.x, adj_pos.y
        w, h = self._width * sc_x * self._scale, self._height * sc_y * self._scale
        s, t = self._s, self._t

        self.vertex_list.position[:] = [
            x,         y, 0,
            x + w,     y, 0,
            x + w, y + h, 0,
            x,     y + h, 0,
        ]

        self.vertex_list.uv[:] = [
            s[0], t[0],
            s[1], t[0],
            s[1], t[1],
            s[0], t[1]
        ]

    @property
    def image(self) -> ImageAsset:
        return self._image

    @image.setter
    def image(self, image: ImageAsset):
        self._image = image
        self.pyglet_group.tex = (image.pyglet_image
                                 .get_image_data()
                                 .create_texture(pyglet.image.Texture))

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width: int):
        self._width = width
        self.update_vertex_data()

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, height: int):
        self._height = height
        self.update_vertex_data()

    def set_tex_coords(self, s: tuple, t: tuple):
        assert (isinstance(s, tuple)
                and isinstance(t, tuple))
        self._s = s
        self._t = t
        self.update_vertex_data()

    @property
    def orig_width(self) -> int:
        return self.image.pyglet_image.width

    @property
    def orig_height(self) -> int:
        return self.image.pyglet_image.height

    def flip_x(self, flipped: Optional[bool] = None):

        flipped = not self.is_flipped_x if flipped is None else flipped

        if flipped is not self.is_flipped_x:
            self.set_scale_x(self._scale_x * -1)
            self.is_flipped_x = flipped
            self.on_position_change()

    def flip_y(self, flipped: Optional[bool] = None):

        flipped = not self.is_flipped_y if flipped is None else flipped

        if flipped is not self.is_flipped_y:
            self.set_scale_y(self._scale_y * -1)
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
        self.update_vertex_data()

    def set_scale(self, n: float):
        """
        Sets the scale of the sprite.
        """
        self._scale_x = n
        self._scale_y = n
        self.update_vertex_data()

    def set_scale_x(self, n: float):
        """
        Sets the scale of the sprite.
        """
        self._scale_x = n
        self.update_vertex_data()

    def set_scale_y(self, n: float):
        """
        Sets the scale of the sprite.
        """
        self._scale_y = n
        self.update_vertex_data()

    def on_position_change(self):

        self.update_vertex_data()
        # self.pyglet_sprite.draw()

    def on_set_visible(self):

        self.update_vertex_data()

    def on_set_hidden(self):

        self.update_vertex_data()
