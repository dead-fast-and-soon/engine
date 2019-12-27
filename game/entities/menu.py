
from dataclasses import dataclass
from typing import List

import pyglet.window.key as key

from engine.objects.entity import Entity
from game.components.elements import Element, MoveElement
from game.components.panel import Panel
from structs.vector import Vector


@dataclass
class _PanelMeta:
    pos: tuple
    size: tuple
    layer: int = 0
    borders: bool = True


@dataclass
class _LabelMeta:
    pos: tuple
    text: tuple
    layer: int = 0
    line_height: int = 0
    states: tuple = None  # for which states should this label be visible


@dataclass
class _Panel:
    meta: _PanelMeta
    component: Element


@dataclass
class _Label:
    meta: _LabelMeta
    component: Element


class Menu(Entity):

    GRID_SIZE = 8

    def on_spawn(self, panels: List[tuple] = [], labels: List[tuple] = [],
                 arrows: List[tuple] = [], arrow_char: str = '>',
                 arrow_layer: int = 0):

        # menu state
        self._state = 0
        self._total_states = len(arrows)

        # panels
        panel_metas: List[_Panel] = [_PanelMeta(*tup) for tup in panels]

        # labels
        label_metas: List[_Label] = [_LabelMeta(*tup) for tup in labels]

        # arrow locations
        self._arrow_positions: List[Vector] = [Vector(tup) for tup in arrows]

        # create panels
        self._panels = []
        for meta in panel_metas:
            self._panels.append(
                _Panel(meta, self.create_component(
                    Panel,
                    Vector(meta.pos) * Menu.GRID_SIZE,
                    *meta.size, meta.borders, layer=meta.layer)))

        # create labels
        self._labels = []
        for meta in label_metas:
            self._labels.append(
                _Label(meta, self.create_component(
                    Element, Vector(meta.pos) * Menu.GRID_SIZE,
                    text=meta.text, line_height=meta.line_height,
                    layer=meta.layer)))

        self._update_labels()

        if self._arrow_positions:
            # create arrow at 1st position
            self._arrow = self.create_component(
                Element, self._arrow_positions[0], text=arrow_char,
                layer=arrow_layer
            )

            self._update_arrow()

    def _to_world(self, grid_pos: Vector) -> Vector:
        """
        Return grid position translated to world position

        Args:
            grid_pos (Vector): grid position

        Returns:
            Vector: world position
        """
        return grid_pos * self.GRID_SIZE

    def _update_all(self):
        self._update_arrow()
        self._update_labels()

    def _update_arrow(self):
        if self._arrow_positions:
            gpos = self._arrow_positions[self._state]
            self._arrow.position = self._to_world(gpos)

    def _update_labels(self):
        for label in self._labels:
            states = label.meta.states
            if states is not None and not isinstance(states, list):
                states = [states]

            if states is not None and self._state not in states:
                label.component.is_visible = False
            else:
                label.component.is_visible = True

    def goto_next_state(self):
        """
        Move the menu's state forward by one.
        """
        if self._total_states > 0:
            next_state = self._state + 1
            self._state = next_state % self._total_states  # autowrap
            self._update_all()

    def goto_prev_state(self):
        """
        Move the menu's state backward by one.
        """
        if self._total_states > 0:
            next_state = self._state - 1
            self._state = next_state % self._total_states  # autowrap
            self._update_all()

    def on_key_press(self, symbol, modifier):

        # simple vertical menu
        if symbol is key.UP:
            self.goto_next_state()

        if symbol == key.DOWN:
            self.goto_prev_state()

        if symbol == key.ENTER:
            self.on_hit_enter(self._state)

    def on_key_release(self, symbol, modifier):
        pass

    def on_hit_enter(self, state: int):
        pass

    @Entity.limit_rate(10)
    def on_update(self, delta: float):
        self.console_set(2, f'menu state: { self._state }')
