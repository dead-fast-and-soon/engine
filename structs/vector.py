
from __future__ import annotations
from typing import Union, Optional, cast


class Vector:
    """
    Represents a 2D point in space.
    """

    def __init__(self, x_or_point_or_tuple: Union[Vector, float, tuple],
                 y: Optional[float] = None):
        """Create a 2D point.

        Args:
            x_or_point_or_tuple (Union[Vector, float, tuple]):
                the x component or the Vector to clone or a tuple
                containing two floats
            y (Optional[float], optional):
                the y component
        """
        if (
            type(x_or_point_or_tuple) is float
            or type(x_or_point_or_tuple) is int
        ):
            x: float = cast(float, x_or_point_or_tuple)
            if y is None:
                raise ValueError("must provide y component if first "
                                 + "argument is a number")
            self.x = x
            self.y = y

        elif type(x_or_point_or_tuple) is tuple:
            pos: tuple = cast(tuple, x_or_point_or_tuple)
            if len(pos) != 2:
                raise ValueError("tuple must contain exactly two numbers")
            if (
                type(pos[0]) is not float
                and type(pos[1]) is not int
            ) or (
                type(pos[1]) is not float
                and type(pos[1]) is not int
            ):
                raise ValueError("values in tuple are not numbers")
            self.x = pos[0]
            self.y = pos[1]

        elif type(x_or_point_or_tuple) is Vector:  # copy constructor
            other: Vector = cast(Vector, x_or_point_or_tuple)
            self.x = other.x
            self.y = other.y

        else:
            raise ValueError("unable to create Vector from value: "
                             + str(x_or_point_or_tuple))

    def __eq__(self, other):
        if type(other) is Vector:
            return self.x == other.x and self.y == other.y
        if type(other) is tuple:
            return self.x == other[0] and self.y == other[1]
        else:
            return self is other

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

    def __iter__(self):
        """Convert this Vector into an Iterable."""
        yield self.x
        yield self.y

    @staticmethod
    def createFrom(val) -> 'Vector':
        """
        Attempts to construct a point from an arbitrary value.
        """
        if type(val) is tuple:
            return Vector(val[0], val[1])
        elif type(val) is Vector:
            return val
        else:
            raise ValueError(f'unable to construct point from value: { val }')


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
