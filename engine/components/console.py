
import pyglet

from engine.objects.component import BatchComponent


class Console(BatchComponent):
    """
    A console used for debugging.
    """
    def on_spawn(self, width=400, height=720):
        """
        Create a new console.

        Args:
            width (int, optional): the width of the console. Defaults to 400.
            height (int, optional): the height of the console. Defaults to 720.
        """
        print(f'placing console @({self.position.x},{self.position.y})')
        self.document = pyglet.text.document.FormattedDocument()

        self.layout: pyglet.text.layout.TextLayout =\
            pyglet.text.layout.TextLayout(
                self.document, width=None, height=None,
                multiline=True, wrap_lines=False,
                batch=self.scene.batch.pyglet_batch
            )
        self.layout.x = self.position.x
        self.layout.y = self.position.y
        self.layout.anchor_x = 'left'
        self.layout.anchor_y = 'bottom'

        self.lines = []

    def line(self, n, message):
        while n >= len(self.lines):
            self.lines.append('')

        self.lines[n] = message
        self.updateText()

    def log(self, message):
        # print(message)
        self.lines.append(message)
        self.updateText()

    def updateText(self):
        self.document.text = '\n'.join(self.lines)
        self.document.set_style(
            0, len(self.document.text),
            dict(
                font_name='Consolas', font_size=8,
                color=(0, 255, 0, 255), background_color=(0, 0, 0, 200)
            )
        )

    def on_position_change(self):
        self.layout.x = self.position.x
        self.layout.y = self.position.y

    def on_render(self):
        # print("rendering console")
        # self.layout.draw()
        pass
