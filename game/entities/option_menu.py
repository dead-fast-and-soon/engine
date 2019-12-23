from engine.game import Game
from engine.camera import ScreenPixelCamera
from engine.objects.entity import Entity
from game.components.panel import Panel
from game.components.elements import Element, MoveElement
from game.entities.menu import Menu
import pyglet.window.key as key

OPT_TEXT_SPEED = 0
OPT_BATTLE_SCENE = 1
OPT_BATTLE_STYLE = 2
OPT_SOUND = 3
OPT_PRINT = 4
OPT_MENU_ACCOUNT = 5
OPT_FRAME = 6
OPT_CANCEL = 7


class OptionsMenu(Menu):
    def on_spawn(self):
        super().on_spawn(
            labels_pos = (16, 8),
            arrow_pos = (8, 8),
            options_pos = (80, 0),
            label_line_height = 8,
            options_line_height = 16,
            labels = [
                'TEXT SPEED',
                'BATTLE SCENE',
                'BATTLE STYLE',
                'SOUND',
                'PRINT',
                'MENU ACCOUNT',
                'FRAME',
                'CANCEL'
            ],
            options_list = [
                [':MID', ':FAST', ':SLOW'],
                [':ON', ':OFF'],
                [':SHIFT', ':SET'],
                [':MONO', ':STEREO'],
                [':NORMAL', ':DARKER', ':DARKEST', ':LIGHTEST', ':LIGHTER'],
                [':ON', ':OFF'],
                [':1', ':2', ':3', ':4', ':5', ':6', ':7', ':8'],
                []
            ],
            panels = [
                    (0, 0, 19, 17, True)
            ]
        )

    def on_option_enter(self, option_idx, label_idx):
        print('selected option {} ({})'.format(option_idx, label_idx))


if __name__ == '__main__':
    # create window
    screen_width = 160
    screen_height = 144
    game = Game(width=screen_width * 4, height=screen_height * 4)

    # start new scene
    scene = game.create_scene()

    # use a zoomed in camera
    scene.use_camera(ScreenPixelCamera, zoom=4)
    scene.spawn_entity(OptionsMenu)
    game.start()
