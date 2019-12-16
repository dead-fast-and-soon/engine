"""
Contains classes relating to batch rendering using Pyglet.
"""

import pyglet
from typing import List


class BatchRenderer:
    """
    A wrapper for Pyglet's Batch and OrderedGroup classes.
    """
    def __init__(self, group_count: int = 10):
        """
        Initialize a BatchRenderer.
        """
        self.pyglet_batch: pyglet.graphics.Batch = pyglet.graphics.Batch()

        self.pyglet_groups: List[pyglet.graphics.OrderedGroup] = []

        for i in range(group_count):
            self.pyglet_groups.append(pyglet.graphics.OrderedGroup(i))

    def render(self):
        """
        Render this batch.
        """
        self.pyglet_batch.draw()

    @property
    def groups(self) -> List[pyglet.graphics.OrderedGroup]:
        """
        Get a list of groups.

        Returns:
            List[pyglet.graphics.OrderedGroup]: the list of groups
        """
        return self.pyglet_groups
