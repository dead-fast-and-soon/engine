
import pyglet

from engine.game.state import GameState
from engine.game.scene import Scene
from engine.view import View
from engine.components.debug import Console, FpsDisplay

SPT = 1.0 / 60.0  # 60 ticks per second


class Game:
    """
    Manages the main game loop and gamestates.
    """

    def __init__(self, *, width, height):
        # the currently loaded gamestate
        self.state: GameState = GameState(self)

        # the current viewport
        self.view: View = View(self)

        # width and height of the window
        self.width, self.height = width, height

        # add an in-game debug console
        self.console = Console(self)
        self.fps_display = FpsDisplay(self, x=20, y=20)

        # load an empty scene
        self.loadScene(Scene(self))

    def log(self, message):
        """
        Logs a message into an internal console.
        """
        self.console.log(message)

    def loadScene(self, scene: Scene):
        """
        Loads a scene.
        """
        self.scene = scene

        # add debug components
        self.scene.components.append(self.console)
        self.scene.components.append(self.fps_display)

    def start(self):
        """
        Opens the window and starts the main game loop.
        """

        width, height = self.width, self.height
        game = self

        class Window(pyglet.window.Window):
            def __init__(self):
                super(Window, self).__init__(
                    width=width,
                    height=height,
                    vsync=False
                )

                pyglet.clock.schedule(self.on_draw)
                self.delta_counter = 0.0  # accumalates frametime

            def on_key_press(symbol, modifier):

                active_ent = self.state.activeTextbox()
                if active_ent is not None:
                    active_ent.onKeyPress(symbol, modifier)

            def on_draw(self, delta=0):

                # delta = pyglet.clock.tick()

                # clear buffer
                # ------------

                self.clear()

                # update logic
                # ------------

                self.delta_counter += delta

                # if accumulative dt goes above SPT, run a tick and decrement
                while self.delta_counter >= SPT:
                    if game.scene is not None:
                        for entity in game.scene.entities:
                            entity.updateEntity(SPT)

                    self.delta_counter -= SPT

                # rendering
                # ---------

                if game.scene is not None:
                    game.scene.renderScene(delta)

        window = Window()
        pyglet.app.run()
