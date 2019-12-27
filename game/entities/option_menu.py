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
            labels=[
                ((2, 1), 'CANCEL'),
                ((2, 3), 'FRAME'),
                ((2, 5), 'MENU ACCOUNT'),
                ((2, 7), 'PRINT'),
                ((2, 9), 'SOUND'),
                ((2, 11), 'BATTLE STYLE'),
                ((2, 13), 'BATTLE SCENE'),
                ((2, 15), 'TEXT SPEED'),

                ((10, 2), ':TYPE 1'),
                ((10, 4), ':ON'),
                ((10, 6), ':NORMAL'),
                ((10, 8), ':MONO'),
                ((10, 10), ':SHIFT'),
                ((10, 12), ':ON'),
                ((10, 14), ':MID')
            ],
            # options_list = [
            #     [':MID', ':FAST', ':SLOW'],
            #     [':ON', ':OFF'],
            #     [':SHIFT', ':SET'],
            #     [':MONO', ':STEREO'],
            #     [':NORMAL', ':DARKER', ':DARKEST', ':LIGHTEST', ':LIGHTER'],
            #     [':ON', ':OFF'],
            #     [':1', ':2', ':3', ':4', ':5', ':6', ':7', ':8'],
            #     []
            # ],
            panels=[
                ((0, 0), (20, 18))
            ],
            arrows=[
                (1, 1),
                (1, 3),
                (1, 5),
                (1, 7),
                (1, 9),
                (1, 11),
                (1, 13),
                (1, 15)
            ]
        )

        self.OPT_IDX_OFFSET = 9
        self._options = [
            [':TYPE 1', ':TYPE 2', ':TYPE 3', ':TYPE 4',
             ':TYPE 5', ':TYPE 6', ':TYPE 7', ':TYPE 8'],
            [':ON', ':OFF'],
            [':NORMAL', ':DARKER', ':DARKEST', ':LIGHTEST', ':LIGHTER'],
            [':MONO', ':STEREO'],
            [':SHIFT', ':SET'],
            [':ON', ':OFF'],
            [':MID', ':FAST', ':SLOW']
        ]

        self._options_selected = [
            0, 0, 0, 0, 0, 0, 0
        ]

        self._update_options()

    def _update_options(self):
        for i, label in enumerate(self._labels[self.OPT_IDX_OFFSET - 1:]):
            selection_idx = self._options_selected[i]
            text = self._options[i][selection_idx]
            label.component.text = text

    def _get_selected_option(self, i: int):
        return self._options_selected[i]

    def next_option(self):
        option_idx = self._state - 1
        self.set_option(option_idx,
                        self._get_selected_option(option_idx) + 1)

    def prev_option(self):
        option_idx = self._state - 1
        self.set_option(option_idx,
                        self._get_selected_option(option_idx) - 1)

    def set_option(self, option_idx, i: int):
        self._options_selected[option_idx] = i % len(self._options[option_idx])
        self._update_options()

    def on_key_press(self, symbol, modifier):
        super().on_key_press(symbol, modifier)

        if self._state is not 0:
            if symbol is key.RIGHT:
                self.next_option()

            if symbol is key.LEFT:
                self.prev_option()

    def on_hit_enter(self, state: int):
        print('selected option {} ({})'.format(option_idx, label_idx))

    @Entity.limit_rate(10)
    def on_update(self, delta: float):
        super().on_update(delta)
        self.console_set(3, f'options: { self._options_selected }')


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
