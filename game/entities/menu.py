
from collections import namedtuple
from typing import List
from engine.objects.entity import Entity
from structs.vector import Vector
from game.components.elements import Element, MoveElement
from game.components.panel import Panel

import pyglet.window.key as key


PanelOptions = namedtuple('PanelOptions', 'x y width height borders')


class Menu(Entity):

    def on_spawn(self,
                 labels_pos: tuple = (0, 0), arrow_pos: tuple = (0, 0),
                 options_pos: tuple = (0, 0), label_line_height: int = 0,
                 options_line_height: int = 0,
                 options_only_show_selected: bool = False,
                 options_label_line_height: int = 0,
                 panels: List[tuple] = [],
                 labels: List[str] = [],
                 options_list: List[List[str]] = []):

        self.options_only_show_selected = options_only_show_selected

        # element offsets
        self.labels_pos = labels_pos
        self.arrows_pos = arrow_pos
        self.options_pos = options_pos

        # formatting
        self.line_height = label_line_height
        self.options_label_line_height = options_label_line_height

        # panels
        self.panels = [PanelOptions(*tup) for tup in panels]

        # create panels
        for panel in self.panels:
            self.create_component(Panel, (panel.x, panel.y),
                                  panel.width, panel.height,
                                  panel.borders)

        # create labels
        glued_labels = '\n'.join(labels)
        self.create_component(Element, labels_pos,
                              text=glued_labels, line_height=label_line_height)

        # create selector arrow
        self.move_element = self.create_component(
            MoveElement, arrow_pos, '>',
            0, len(options_list),  # vertical bounds
            0, 0,  # horizontal bounds
            16, 0,  # x/y movement amount
            0
        )

        # create option labels
        self.options = []
        for i, options in enumerate(reversed(options_list)):
            options_offset = Vector(options_pos) + (0, i * options_line_height)
            self.options.append([self.add_text(options_offset, label,
                                               options_label_line_height)
                                for label in options])

        # list containing selected option for each options
        self.options_selection = [0 for options in options_list]

        self.show_options()  # update options
        
    def hide_element(self, element):
        element.component.is_visible = False

    def hide_all_elements(self, options):
        [self.hide_element(dsc) for dsc in options]

    def show_element(self, options, idx):
        self.hide_all_elements(options)
        options[idx].component.is_visible = True

    @property
    def current_option_idx(self) -> int:
        """
        Return the index of the currently selected option.
        
        Returns:
            int: an index of the currently selected option
        """
        return self.move_element.grid_position.y

    @property
    def current_selection_idx(self) -> int:
        """
        Return the index of the currently selected label for the
        currently selected option.
        
        Returns:
            int: an index of the currently selected label
        """
        return self.get_selected_option(self.current_option_idx)

    def change_options(self, is_next: bool):
        # select prev option if is_next is false
        delta = 1 if is_next else -1

        self.options_selection[self.current_option_idx] += delta

    def get_selected_option(self, idx: int):
        if len(self.options[idx]) is 0:
            return 0
        else:
            return self.options_selection[idx] % len(self.options[idx])

    def show_options(self):
        for i in range(len(self.options)):
            if len(self.options[i]) > 0:
                if (
                    not self.options_only_show_selected
                    or self.current_option_idx is i
                ):
                    self.show_element(self.options[i],
                                      self.get_selected_option(i))
                else:
                    self.hide_all_elements(self.options[i])

    def on_key_press(self, symbol, modifier):
        if symbol == key.UP:
            self.move_element.move_up()
        if symbol == key.DOWN:
            self.move_element.move_down()
        if symbol == key.RIGHT:
            self.change_options(True)
            self.move_element.move_right()
        if symbol == key.LEFT:
            self.change_options(False)
            self.move_element.move_left()
        if symbol == key.ENTER:
            self.move_element.on_key_press()
            self.on_option_enter(self.current_option_idx,
                                 self.current_selection_idx)

        self.show_options()

    def on_key_release(self, symbol, modifier):
        pass

    def add_text(self, position: tuple,
                 text: str, line_height: int) -> Element:
        return self.create_component(Element, position, text, line_height)

    def on_option_enter(self, option_idx: int, label_idx: int):
        pass
