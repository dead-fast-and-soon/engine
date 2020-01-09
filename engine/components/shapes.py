
import math
import pyglet
from typing import TYPE_CHECKING, List

from engine.objects.component import Component, BatchComponent
from engine.structs.color import Color, WHITE
from engine.structs.vector import Transform

if TYPE_CHECKING:
    from engine.scene import Scene


class Shape2D(BatchComponent):
    """
    A geometric shape that is created using points.
    """
    def on_spawn(self, points: List[tuple], color: tuple = (255, 255, 255),
                 is_filled: bool = True, is_looped: bool = True,
                 layer: int = 0):
        """
        Create a primitive shape.

        Args:
            points (List[tuple]): the points to create the shape
            color (tuple, optional): the color of the shape.
            is_filled (bool, optional): if this is a filled or outlined shape.
        """
        assert len(points) > 0, 'must provide at least one point'

        if len(points) == 1:
            mode = pyglet.gl.GL_POINTS
        elif len(points) == 2:
            mode = pyglet.gl.GL_LINES
        elif not is_filled:
            if is_looped:
                mode = pyglet.gl.GL_LINE_LOOP
            else:
                mode = pyglet.gl.GL_LINE_STRIP
        elif len(points) == 3:
            mode = pyglet.gl.GL_TRIANGLES
        elif len(points) == 4:
            mode = pyglet.gl.GL_TRIANGLES
            # mode = pyglet.gl.GL_TRIANGLE_FAN  # maybe more effecient?
        else:
            mode = pyglet.gl.GL_POLYGON
            # mode = pyglet.gl.GL_TRIANGLE_FAN

        self.points = points
        self.num_points = len(points)

        group = self.scene.batch.group(layer)
        batch = self.scene.batch.pyglet_batch

        if self.num_points is 4:  # use indexed list
            self.vertex_list = self.scene.batch.add_indexed(
                self.num_points, mode,
                [0, 1, 2, 0, 2, 3], 'vertices2f', 'colors3B'
            )

        else:
            self.vertex_list = self.scene.batch.add(
                self.num_points, mode, 'vertices2f', 'colors3B'
            )

        self.color = color
        self.update_points()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color: tuple):
        self._color = tuple(color)
        self.vertex_list.colors[:] = tuple(color) * self.num_points

    @property
    def translated_points(self) -> list:
        """
        Get points of this shape translated by this component's position.

        Returns:
            list: a list of translated points
        """
        new_points = []
        for point in self.points:
            x = point[0] + self.position.x
            y = point[1] + self.position.y
            new_points.append((x, y))
        return new_points

    @property
    def translated_flat_points(self) -> list:
        """
        Get points of this shape translated by this component's position.

        Returns:
            list: a flat list of translated points
        """
        new_points = []
        for point in self.points:
            new_points.append(point[0] + self.position.x)
            new_points.append(point[1] + self.position.y)
        return new_points

    def flatten_points(self, points: list) -> list:
        """
        Get points of this shape as a flat list.

        Returns:
            list: a list of numbers
        """
        return [n for point in points for n in point]

    def update_points(self):
        """
        Update the points of this shape.
        """
        # points = self.translated_flat_points
        # print(points)
        # self.vertex_list.set_attribute_data(0, points)
        self.vertex_list.vertices[:] = self.translated_flat_points

    def on_position_change(self):
        self.update_points()

    def on_destroy(self):
        self.vertex_list.delete()


class Box2D(Shape2D):
    """
    A 2D box.
    """
    def on_spawn(self, size: tuple, color: tuple = (255, 255, 255),
                 is_filled: bool = True, layer: int = 0):
        """
        Create a 2D box.

        Args:
            size (tuple): the width and height of the box (in pixels)
            color (tuple): the color of the box [defaults to (255, 255, 255)]
            is_filled (bool): if true, fill the box, otherwise draw an
                              outline
        """
        self._size = size
        points = self._get_points()
        super().on_spawn(color=color, points=points, is_filled=is_filled,
                         layer=layer)

    @property
    def size(self):

        return self._size

    @size.setter
    def size(self, size: tuple):

        self._size = size
        self.points = self._get_points()
        self.update_points()

    def _get_points(self):

        width, height = self.size
        return [
            (0, 0), (0, height),
            (width, height), (width, 0)
        ]


class Circle2D(Shape2D):
    """
    A 2D circle.
    """
    def on_spawn(self, radius: float = 5, n: int = 6, *args, **kwargs):
        points = []
        for i in range(n):
            points.append((
                (math.sin((i / n) * 2 * math.pi) * radius),
                (math.cos((i / n) * 2 * math.pi) * radius)
            ))
        super().on_spawn(*args, points=points, **kwargs)
