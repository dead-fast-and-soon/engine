from engine.game import Game
from engine.camera import ScreenPixelCamera
from engine.objects.entity import Entity
from game.components.panel import Panel
from game.components.elements import Element, MoveElement
from game.entities.menu import Menu
import pyglet.window.key as key


class SaveMenu(Menu):
    def on_spawn(self):
        super().on_spawn(
            labels_pos = (40, 120),
            arrow_pos = (8, 56),
            labels = [
                'PLAYER SILVER',
                'BADGES'
                'TIME'
                '0',
                '0:08',
                'YES',
                'NO'
            ],
            panels = [
                # Text Panel
                (0, 0, 19, 5, True),
                # Yes / No Panel
                (0, 48, 5, 5, True),
                # Player info Panel
                (32, 64, 15, 9, True)
            ]
        )


if __name__ == '__main__':
    # create window
    screen_width = 160
    screen_height = 144
    game = Game(width=screen_width * 4, height=screen_height * 4)

    # start new scene
    scene = game.create_scene()

    # use a zoomed in camera
    scene.use_camera(ScreenPixelCamera, zoom=4)
    scene.spawn_entity(SaveMenu)
    game.start()