"""
Components used for the purpose of debugging.
"""

from engine.objects.component import BatchComponent
from engine.components.text import Text


class FpsDisplay(BatchComponent):

    def on_spawn(self):

        self.text: Text = self.create_component(Text, self.position)
        self.deltas = []

    def on_update(self, delta):

        frametime = self.scene.game.last_delta

        if frametime > 0:
            fps = str(round(1.0 / frametime, 2))
        else:
            fps = str(0.0)

        self.text.text = 'FPS: ' + fps
