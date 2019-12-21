
import pyglet.window.key as key
import math

from engine.asset.tileset import TilesetAsset
from engine.objects.entity import Entity
from engine.components.sprite import AnimatedSprite
from structs.vector import Vector
from game.structs.framedata import FrameData

from engine.utils.math import lerp

KEY_PRESSED = 1
KEY_HELD = 2
KEY_RELEASED = 0


class Player(Entity):

    MOVE_LENGTH = 0.25

    def on_spawn(self):

        self.frames = TilesetAsset("assets/kris.png",
                                   tile_width=16, tile_height=16)

        # TODO: move these animations to their own file

        self.ANI_DOWN = [
            (self.frames[0], 0.125, False, False, Vector(-8, -8)),
            (self.frames[3], 0.125, False, False, Vector(-8, -8)),
            (self.frames[0], 0.125, True, False, Vector(-8, -8)),
            (self.frames[3], 0.125, True, False, Vector(-8, -8))
        ]

        self.ANI_UP = [
            (self.frames[1], 0.125, False, False, Vector(-8, -8)),
            (self.frames[4], 0.125, False, False, Vector(-8, -8)),
            (self.frames[1], 0.125, True, False, Vector(-8, -8)),
            (self.frames[4], 0.125, True, False, Vector(-8, -8))
        ]

        self.ANI_LEFT = [
            (self.frames[2], 0.125, False, False, Vector(-8, -8)),
            (self.frames[5], 0.125, False, False, Vector(-8, -8))
        ]

        self.ANI_RIGHT = [
            (self.frames[2], 0.125, True, False, Vector(-8, -8)),
            (self.frames[5], 0.125, True, False, Vector(-8, -8))
        ]

        self.sprite: AnimatedSprite = self.create_component(
            AnimatedSprite, (0, 0),
            frames=self.ANI_DOWN
        )

        self.keys = self.scene.game.input

        self.last_pos: Vector = self.position
        self.grid_pos: Vector = Vector(0, 0)
        self.grid_size = 16

        self.move_fd: FrameData = FrameData([(Player.MOVE_LENGTH, 0)])
        self.move_state = self.move_fd.current_state

    def on_key_press(self, symbol, modifier):
        pass

    def on_key_release(self, symbol, modifier):
        pass

    def on_update(self, delta: float):

        # shortcut way of getting axes
        axis = Vector(self.keys[key.RIGHT] - self.keys[key.LEFT],
                      self.keys[key.UP] - self.keys[key.DOWN])

        if self.move_state is FrameData.NOT_ACTIVE:
            if not axis.is_zero:

                self.grid_pos += axis
                self.last_pos = self.position
                self.move_fd.start()

                # switch to appropriate animation

                if axis.y == 1:
                    self.sprite.set_animation(self.ANI_UP)
                elif axis.y == -1:
                    self.sprite.set_animation(self.ANI_DOWN)

                if axis.x == 1:
                    self.sprite.set_animation(self.ANI_RIGHT)
                elif axis.x == -1:
                    self.sprite.set_animation(self.ANI_LEFT)

                self.sprite.play()

            else:  # stop animations

                self.sprite.restart()
                self.sprite.stop()

        self.move_fd.update(delta)  # update movement frame data

        if self.move_state is 0:

            perc = self.move_fd.section_progress(0)
            self.position = self.last_pos.lerp(self.grid_pos * self.grid_size,
                                               perc)

        self.move_state = self.move_fd.current_state
