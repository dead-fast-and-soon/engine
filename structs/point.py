

class Point:
    """
    Represents a 2D point in space.
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

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
