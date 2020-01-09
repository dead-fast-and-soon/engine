
from __future__ import annotations
import typing
import konkyo.utils

if typing.TYPE_CHECKING:
    from konkyo.scene import Scene


class Renderable:
    """
    An object that requires a draw call to be rendered.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self):
        """
        Render this object.
        """
        self.on_render()

    def on_render(self):
        """
        Called when this object needs to be rendered.
        """
        pass


class BatchRenderable:
    """
    An object that requires a batched draw call from
    a Scene to be rendered.
    """
    def __init__(self, *args, scene: Scene, **kwargs):
        self.scene = scene
        super(BatchRenderable, self).__init__(*args, **kwargs)
