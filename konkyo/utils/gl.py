
from __future__ import annotations
from pyglet.gl import *
from ctypes import *
import glm


def _get_uniform_location(id: int, name: str):
    """
    Get a uniform's location from its name.

    Args:
        id (int): the id of the shader program
        name (str): the name of the uniform
    """
    loc = glGetUniformLocation(id, create_string_buffer(name.encode('utf-8')))
    assert loc != -1, 'No uniform was found with name "%s"' % name
    return loc


def _set_uniform_mat4(id: int, value):
    """
    Set a uniform to a matrix.

    Args:
        id (int): [description]
        value ([type]): [description]
    """
    glUniformMatrix4fv(id, 1, GL_FALSE, glm.value_ptr(value))


def gl_set_uniform_mat4(program: int, name: str, value):
    loc = _get_uniform_location(program, name)
    _set_uniform_mat4(loc, value)


class GLDefinedBuffer:
    """
    This class references both a GL buffer object and a target,
    effectively forcing that buffer object to only be used with
    that given target.
    """

    def __init__(self, target: int, id: int = None):
        assert id is not None

        self.id = id
        self.target = target

    def bind(self):
        """
        Bind this buffer object to the target.
        """
        glBindBuffer(self.target, self.id)

    def unbind(self):
        """
        Bind nothing to the target, effectively unbinding our buffer.

        Args:
            target (int, optional): [description]. Defaults to None.
        """
        glBindBuffer(self.target, 0)


class GLUniformBuffer(GLDefinedBuffer):
    """
    A GL buffer object to be used with the GL_UNIFORM_BUFFER target.
    """

    def __init__(self, id: int = None):
        super().__init__(GL_UNIFORM_BUFFER, id)

    def sub_data(self, offset: int, data):
        """
        Set the data of a specific range in this buffer.

        Args:
            offset (int): the offset (in bytes) of where to start setting data
            size (int): the size (in bytes) of the data to set
            data ([type]): the data
        """
        glBufferSubData(self.target,
                        offset,
                        glm.sizeof(type(data)),
                        glm.value_ptr(data))

    def set_binding_point(self, binding_point: int):
        """
        Set the binding point that this buffer should use.

        Args:
            binding_point (int): [description]
        """
        glBindBufferBase(self.target, binding_point, self.id)

    def __enter__(self) -> GLUniformBuffer:
        self.bind()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unbind()


