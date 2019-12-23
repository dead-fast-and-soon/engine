from engine.game import Game
from engine.camera import ScreenPixelCamera
from engine.objects.entity import Entity
from game.components.panel import Panel
from game.components.elements import Element, MoveElement
from game.entities.menu import Menu
import pyglet.window.key as key


class StartMenu(Menu):
    def on_spawn(self):
        super().on_spawn(
            labels_pos = (96, 8),
            arrow_pos = (88, 8),
            options_pos = (0, 8),
            label_line_height = 8,
            options_line_height = 0,
            options_label_line_height = 8,
            labels = [
                'POK^DEX',
                'POK^MON',
                'PACK',
                '#%GEAR',
                'SILVER',
                'SAVE',
                'OPTION',
                'EXIT'
            ],
            options_list = [
                ['Pok^mon \ndatabase'],
                ['Party #% \nstatus'],
                ['Contains \nitems'],
                ['Trainer\'s \nkey device'],
                ['Your own \nstatus'],
                ['Save your \nprogress'],
                ['Change \nsettings'],
                ['Exit this \nmenu']
            ],
            options_only_show_selected = True,
            panels = [
                    (80, 0, 9, 17, True),
                    (0, 0, 10, 5, False)
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
    scene.spawn_entity(StartMenu)
    game.start()
