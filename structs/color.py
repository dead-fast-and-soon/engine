
class Color:

    def __init__(self, r, g, b):
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


WHITE = Color(255, 255, 255)
