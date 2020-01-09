"""
Contains classes relating to batch rendering using Pyglet.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, List

import pyglet

import glm
from engine.utils.gl import *
from engine.graphics.shaders import program

if TYPE_CHECKING:
    from engine.scene import Scene


IDENTITY_MAT = glm.mat4(1.0)


class ShaderGroup(pyglet.graphics.Group):

    def __init__(self, program, ortho: tuple):
        super().__init__(program)
        # self._ortho = ortho

    def set_state(self):
        super().set_state()
        # gl_set_uniform_mat4(self.program._id, 'view', IDENTITY_MAT)
        # gl_set_uniform_mat4(self.program._id, 'projection', glm.ortho(*self._ortho))


class SpriteShaderGroup(pyglet.sprite.SpriteGroup):

    def __init__(self, texture, program):
        super().__init__(texture,
                         GL_SRC_ALPHA,
                         GL_ONE_MINUS_SRC_ALPHA,
                         program)

class BatchRenderer:
    """
    A wrapper for Pyglet's Batch and OrderedGroup classes.
    """
    def __init__(self, scene: Scene = None, group_count: int = 10):
        """
        Initialize a BatchRenderer.
        """
        self.pyglet_batch: pyglet.graphics.Batch = pyglet.graphics.Batch()

        if scene is None:
            width, height = 100, 100
        else:
            width, height = scene.game.width, scene.game.height

        self._group = ShaderGroup(program, (0, width, 0, height))

        # self.pyglet_groups: List[pyglet.graphics.OrderedGroup] = []

        # for i in range(group_count):
            # self.pyglet_groups.append(pyglet.graphics.OrderedGroup(i))

    def render(self):
        """
        Render this batch.
        """
        self.pyglet_batch.draw()

    def add(self, count, mode, *data):
        return self.pyglet_batch.add(
            count, mode, self._group, *data)

    def add_indexed(self, count, mode, indices, *data):
        return self.pyglet_batch.add_indexed(
            count, mode, self._group, indices, *data)

    def group(self, order: int):
        return pyglet.graphics.Group(order=order)

    def get_sprite_group(self, image):
        return SpriteShaderGroup(image.get_texture(), program)

    # @property
    # def groups(self) -> List[pyglet.graphics.Group]:
    #     """
    #     Get a list of groups.

    #     Returns:
    #         List[pyglet.graphics.OrderedGroup]: the list of groups
    #     """
    #     return self.pyglet_groups
