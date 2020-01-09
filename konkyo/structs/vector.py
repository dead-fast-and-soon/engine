
from __future__ import annotations
from typing import Union, Optional, cast
from dataclasses import dataclass
from numbers import Number

import math
import konkyo.utils.math


@dataclass(init=False, order=False, frozen=True)
class Vector:
    """
    Represents a 2D point in space.
    """
    x: Number
    y: Number = 0

    def __init__(self, x: Union[Vector, Number, tuple], y: Number = 0):
        """
        Create a 2D vector.

        Args:
            x (Union[Vector, Number, tuple]):
            y (Number, optional): the y component. Defaults to 0.
        """
        if isinstance(x, Number) and isinstance(y, Number):

            super().__setattr__('x', x)
            super().__setattr__('y', y)

        elif isinstance(x, tuple):

            vec_x, vec_y = x
            assert isinstance(vec_x, Number) and isinstance(vec_y, Number), (
                'values in tuple are not numbers')

            super().__setattr__('x', vec_x)
            super().__setattr__('y', vec_y)

        elif isinstance(x, Vector):

            super().__setattr__('x', x.x)
            super().__setattr__('y', x.y)

        else:

            raise ValueError('unable to construct point from value: {}'
                             .format(x))

    @property
    def is_zero(self) -> bool:
        """
        Return True if all components of this vector are 0.
        """
        return self.x is 0 and self.y is 0

    def lerp(self, other: Vector, t: float) -> Vector:
        """
        Lerp between this vector and another vector.

        Args:
            other (Vector): the other vector
            t (float): the time variable (between 0 and 1)

        Returns:
            Vector: the resultant vector
        """
        x = konkyo.utils.math.lerp(self.x, other.x, t)
        y = konkyo.utils.math.lerp(self.y, other.y, t)
        return Vector(x, y)

    def ceil(self) -> Vector:
        """
        Perform ceil rounding on this vector's components and
        return a new vector.

        Returns:
            Vector: the resultant vector
        """
        return Vector(math.ceil(self.x), math.ceil(self.y))

    def __iadd__(self, other):
        """ += operator """
        x, y = self.x, self.y

        if type(other) is tuple:
            return Vector(x + other[0], y + other[1])
        elif type(other) is Vector:
            return Vector(x + other.x, y + other.y)

        raise ValueError(f'unable to add 2D point to value { other }')

    def __add__(self, other):
        """ + operator """
        x, y = self.x, self.y

        if type(other) is tuple:
            return Vector(x + other[0], y + other[1])
        elif type(other) is Vector:
            return Vector(x + other.x, y + other.y)

        raise ValueError(f'unable to add 2D point to value { other }')

    def __sub__(self, other):
        """ - operator """
        x, y = self.x, self.y

        if type(other) is tuple:
            return Vector(x - other[0], y - other[1])
        elif type(other) is Vector:
            return Vector(x - other.x, y - other.y)

        raise ValueError(f'unable to subtract 2D point to value { other }')

    def __mul__(self, other):
        """
        * operator
        """
        assert isinstance(other, (int, float)), ('unable to multiply value'
                                                 'by {}'.format(other))

        return Vector(self.x * other, self.y * other)

    def __floordiv__(self, other):
        """
        // operator
        """
        assert isinstance(other, (int, float)), ('unable to multiply value'
                                                 'by {}'.format(other))

        return Vector(self.x // other, self.y // other)

    def __iter__(self):
        """Convert this Vector into an Iterable."""
        yield self.x
        yield self.y

    def __repr__(self):
        """
        Represent this vector as a string.
        """
        return '(X={},Y={})'.format(self.x, self.y)


class Transform(Vector):
    """
    Represents a 2D box in space.
    """

    def __init__(self, x: float, y: float, w: float, h: float):

        super().__init__(x, y)
        self.w = w
        self.h = h

    @property
    def point(self):
        """ Retrieves this transform as a point. """
        return Vector(self.x, self.y)
