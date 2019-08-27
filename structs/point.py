
from __future__ import annotations
from typing import Union, Optional, cast


class Point:
    """
    Represents a 2D point in space.
    """

    def __init__(self, x_or_point_or_tuple: Union[Point, float, tuple],
                 y: Optional[float] = None):
        """Create a 2D point.

        Args:
            x_or_point_or_tuple (Union[Point, float, tuple]):
                the x component or the Point to clone or a tuple
                containing two floats
            y (Optional[float], optional):
                the y component
        """
        if (
            type(x_or_point_or_tuple) is float or
            type(x_or_point_or_tuple) is int
        ):
            x: float = cast(float, x_or_point_or_tuple)
            if y is None:
                raise ValueError("must provide y component if first " +
                                 "argument is a number")
            self.x = x
            self.y = y

        elif type(x_or_point_or_tuple) is tuple:
            pos: tuple = cast(tuple, x_or_point_or_tuple)
            if len(pos) != 2:
                raise ValueError("tuple must contain exactly two numbers")
            if (
                type(pos[0]) is not float and
                type(pos[1]) is not int
            ) or (
                type(pos[1]) is not float and
                type(pos[1]) is not int
            ):
                raise ValueError("values in tuple are not numbers")
            self.x = pos[0]
            self.y = pos[1]

        elif type(x_or_point_or_tuple) is Point:  # copy constructor
            other: Point = cast(Point, x_or_point_or_tuple)
            self.x = other.x
            self.y = other.y

        else:
            raise ValueError("unable to create Point from value: " +
                             str(x_or_point_or_tuple))

    def __iadd__(self, other):
        """ += operator """
        x, y = self.x, self.y

        if type(other) is tuple:
            return Point(x + other[0], y + other[1])
        elif type(other) is Point:
            return Point(x + other.x, y + other.y)

        raise ValueError(f'unable to add 2D point to value { other }')

    def __add__(self, other):
        """ + operator """
        x, y = self.x, self.y

        if type(other) is tuple:
            return Point(x + other[0], y + other[1])
        elif type(other) is Point:
            return Point(x + other.x, y + other.y)

        raise ValueError(f'unable to add 2D point to value { other }')

    def __sub__(self, other):
        """ - operator """
        x, y = self.x, self.y

        if type(other) is tuple:
            return Point(x - other[0], y - other[1])
        elif type(other) is Point:
            return Point(x - other.x, y - other.y)

        raise ValueError(f'unable to subtract 2D point to value { other }')

    def __iter__(self):
        """Convert this Point into an Iterable."""
        yield self.x
        yield self.y

    @staticmethod
    def createFrom(val) -> 'Point':
        """
        Attempts to construct a point from an arbitrary value.
        """
        if type(val) is tuple:
            return Point(val[0], val[1])
        elif type(val) is Point:
            return val
        else:
            raise ValueError(f'unable to construct point from value: { val }')


class Transform(Point):
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
        return Point(self.x, self.y)
