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
            arrow_layer=3,
            arrows=[
                (1, 9), (1, 7)
            ],
            labels=[
                ((5, 15), 'PLAYER SILVER', 1),
                ((5, 13), 'BADGES', 1),
                ((5, 9), 'TIME', 1),
                ((18, 13), '0', 1),
                ((15, 9), '0:08', 1),

                ((2, 9), 'YES', 3),
                ((2, 7), 'NO', 3),

                ((1, 1), 'Would you like to\nsave the game?', 1, 8)
            ],
            panels=[
                # Text Panel
                ((0, 0), (20, 6), 0),
                # Yes / No Panel
                ((0, 6), (6, 5), 2),
                # Player info Panel
                ((4, 8), (16, 10), 0)
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