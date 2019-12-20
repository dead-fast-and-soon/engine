from engine.game import Game
from engine.camera import ScreenPixelCamera
from engine.objects.entity import Entity
from game.components.panel import Panel
from game.components.elements import Element, MoveElement
import pyglet.window.key as key


class Menu(Entity):
    def on_spawn(self):
        self.create_component(Panel, (80, 0), 9, 17, True)
        self.create_component(Panel, (0, 0), 10, 5, False)
        self.create_component(Element, (96, 120), 'POK^DEX')
        self.create_component(Element, (96, 104), 'POK^MON')
        self.create_component(Element, (96, 88), 'PACK')
        self.create_component(Element, (96, 72), r'#%GEAR')
        self.create_component(Element, (96, 56), 'SILVER')
        self.create_component(Element, (96, 40), 'SAVE')
        self.create_component(Element, (96, 24), 'OPTION')
        self.create_component(Element, (96, 8), 'EXIT')
        self.move_element: MoveElement = self.create_component(
            MoveElement, (88, 104), '>', -8, 136, 0, 0, 16, 0, 128
        )

    def on_key_press(self, symbol, modifier):
        if symbol == key.UP:
            self.move_element.move_up()
        if symbol == key.DOWN:
            self.move_element.move_down()
        if symbol == key.RIGHT:
            self.move_element.move_right()
        if symbol == key.LEFT:
            self.move_element.move_left()
        if symbol == key.ENTER:
            self.move_element.on_key_press()

    def on_key_release(self, symbol, modifier):
        pass

    def on_update(self, delta: float):
        # Pack description
        if self.move_element.position == (88, 88):
            self.create_component(Element, (0, 24), 'Contains\n items', 8)

        # PokeGEAR description
        if self.move_element.position == (88, 72):
            self.create_component(Element, (0, 24), 'Trainer\'s')
            self.create_component(Element, (0, 8), 'key device')

        # Trainer name description
        if self.move_element.position == (88, 56):
            self.create_component(Element, (0, 24), 'Your own')
            self.create_component(Element, (0, 8), 'status')

        # Save description
        if self.move_element.position == (88, 40):
            self.create_component(Element, (0, 24), 'Save your')
            self.create_component(Element, (0, 8), 'progress')

        # Options description
        if self.move_element.position == (88, 24):
            self.create_component(Element, (0, 24), 'Change')
            self.create_component(Element, (0, 8), 'settings')

        # Exit description
        if self.move_element.position == (88, 8):
            self.create_component(Element, (0, 24), 'Close this')
            self.create_component(Element, (0, 8), 'menu')


if __name__ == '__main__':
    # create window
    screen_width = 160
    screen_height = 144
    game = Game(width=screen_width * 4, height=screen_height * 4)

    # start new scene
    scene = game.create_scene()

    # use a zoomed in camera
    scene.use_camera(ScreenPixelCamera, zoom=4)
    scene.spawn_entity(Menu)
    game.start()
