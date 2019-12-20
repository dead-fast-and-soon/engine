from engine.game import Game
from engine.asset.tileset import TilesetAsset
from engine.components.sprite import SpriteText
from engine.camera import ScreenPixelCamera
from game.components.panel import Panel
from engine.objects.component import BatchComponent
import pyglet.window.key as key
import sys

# load assets
tileset = TilesetAsset('assets/font.png', tile_width=8, tile_height=8)


class Element(BatchComponent):
    def on_spawn(self, text: str, line_height: int):
        self.x = self.position.x
        self.y = self.position.y
        self.text = text
        self.component = self.create_component(SpriteText,
                                               (self.x, self.y),
                                               tileset,
                                               self.text,
                                               line_height=line_height,
                                               layer=2)


class MoveElement(BatchComponent):
    def on_spawn(self, text: str, lower_bound, upper_bound, left_bound,
                 right_bound, move_pixal_vertical, move_pixal_horizontal,
                 wrap_around):
        self.x = self.position.x
        self.y = self.position.y
        self.text = text
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.move_pixal_vertical = move_pixal_vertical
        self.move_pixal_horizontal = move_pixal_horizontal
        self.wrap_around = wrap_around
        self.component = self.create_component(
            SpriteText, (self.x, self.y), tileset, self.text, layer=2
        )

    def move_up(self):
        if self.position.y < self.upper_bound:
            self.position += (0, self.move_pixal_vertical)

        if self.position.y == self.upper_bound:
            self.position -= (0, self.wrap_around)

    def move_down(self):
        if self.position.y > self.lower_bound:
            self.position -= (0, self.move_pixal_vertical)

        if self.position.y == self.lower_bound:
            self.position += (0, self.wrap_around)

    def move_right(self):
        if self.position.x < self.right_bound:
            self.position += (self.move_pixal_horizontal, 0)

    def move_left(self):
        if self.position.x > self.left_bound:
            self.position -= (self.move_pixal_horizontal, 0)

    def on_key_press(self):
        if self.position.y == self.lower_bound + 16:
            pass

        # Silly Menu stuff
        '''
        if symbol == key.RIGHT:
            self.position += (4, 0)
        if symbol == key.LEFT:
            self.position -= (4, 0)
        '''


# start game
if __name__ == '__main__':
        # create window
    screen_width = 160
    screen_height = 144
    game = Game(width=screen_width * 4, height=screen_height * 4)

    # start new scene
    scene = game.create_scene()

    # use a zoomed in camera
    scene.use_camera(ScreenPixelCamera, zoom=4)

    # Create Panel
    scene.spawn_component(Panel, (80, 0), 9, 17)

    scene.spawn_component(Element, (96, 120), 'POK^DEX')
    scene.spawn_component(Element, (96, 104), 'POK^MON')
    scene.spawn_component(Element, (96, 88), 'PACK')
    scene.spawn_component(Element, (96, 72), r'#%GEAR')
    scene.spawn_component(Element, (96, 56), 'SILVER')
    scene.spawn_component(Element, (96, 40), 'SAVE')
    scene.spawn_component(Element, (96, 24), 'OPTION')
    scene.spawn_component(Element, (96, 8), 'EXIT')
    scene.spawn_component(MoveElement, (88, 104), '>', -8, 136, 16, 0, 128)

    game.start()
