
import pyglet

from engine.objects.component import BatchComponent


class Text(BatchComponent):

    def on_spawn(self, text: str = ''):

        self.pyglet_text = pyglet.text.Label(
            text,
            font_name='Consolas',
            font_size=12,
            x=self.position.x, y=self.position.y,
            batch=self.scene.batch.pyglet_batch
        )
        self.text = text

    @property
    def text(self):

        return self.pyglet_text.text

    @text.setter
    def text(self, text: str):

        self.pyglet_text.text = text

    def on_position_change(self):

        self.pyglet_text.x = self.position.x
        self.pyglet_text.y = self.position.y
