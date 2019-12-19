"""
Components used for the purpose of debugging.
"""

from engine.objects.component import BatchComponent
from engine.components.text import Text


class FpsDisplay(BatchComponent):

    def on_spawn(self):

        self.text: Text = self.create_component(Text, self.position)
        self.deltas = []
        self._timer = 0
        self.text.text = 'FPS: 0'

    def on_update(self, delta):

        self._timer += delta
        if self._timer >= 1:

            if delta > 0:
                fps = str(round(1.0 / delta, 2))
            else:
                fps = str(0.0)
            self.text.text = f'FPS: { fps }'

        while self._timer >= 1: self._timer -= 1
