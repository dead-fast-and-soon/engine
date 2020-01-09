
from numbers import Number


class Color:

    def __init__(self, r, g, b):
        assert (0 <= r <= 255
                and 0 <= b <= 255
                and 0 <= g <= 255), 'RGB values must be between 0 - 255'

        self.r, self.g, self.b = r, g, b

    def brightness(self, n):
        """
        Sets brightness of this color (from 0.0 to 1.0)
        """
        r = int(self.r * n)
        g = int(self.g * n)
        b = int(self.b * n)

        return Color(r, g, b)

    def __iter__(self):
        """Convert this Vector into an Iterable."""
        yield self.r
        yield self.g
        yield self.b

    def __mul__(self, other):
        """
        Multiply this color by a scalar.

        Args:
            other ([type]): [description]
        """
        assert isinstance(other, Number), f'cannot multiply color by { other }'

        return Color(self.r * other, self.g * other, self.b * other)


WHITE = Color(255, 255, 255)
