
import pyglet
import typing
import time

from engine.game.state import GameState
from engine.game.scene import Scene
from engine.camera import Camera, ScreenCamera
from engine.components.debug import Console, FpsDisplay

SPT = 1.0 / 60.0  # 60 ticks per second


class Game:
    """
    Manages the main game loop and gamestates.
    """

    def __init__(self, *, width, height):
        # the currently loaded gamestate
        self.state: GameState = GameState(self)

        # a list of cameras
        self.cameras: typing.List[Camera] = []

        # a list of scenes
        self.scenes: typing.List[Scene] = []

        # width and height of the window
        self.width: float = width
        self.height: float = height

        # add an in-game debug console
        self.console = Console((20, 20), game=self)
        self.fps_display = FpsDisplay((0, 0))

        hud_scene = Scene(self)
        hud_scene.components.append(self.console)
        hud_scene.components.append(self.fps_display)

        hud_view = ScreenCamera(self)
        hud_view.assignScene(hud_scene)
        self.cameras.append(hud_view)

    def log(self, message):
        """
        Logs a message into an internal console.
        """
        self.console.log(message)

    def createScene(self):
        """Create and return an empty Scene."""
        scene = Scene(self)
        self.scenes.append(scene)
        return scene

    def createCamera(self, camera_class: typing.Type[Camera] = None):
        """Create and return a Camera object."""
        if camera_class is None:
            camera_class = Camera

        camera = camera_class(self)
        self.cameras.append(camera)
        return camera

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

            def on_key_press(symbol, modifier):
                active_ent = self.state.activeTextbox()
                if active_ent is not None:
                    active_ent.onKeyPress(symbol, modifier)

        window = Window()

        last_time = time.perf_counter()
        accum_time = 0

        while True:

            end_time = time.perf_counter()
            delta = end_time - last_time
            last_time = end_time

            # clear buffer
            # ------------

            window.switch_to()
            window.dispatch_events()
            window.clear()

            # update logic
            # ------------

            accum_time += delta

            # if accumulative dt goes above SPT, run a tick and decrement
            while accum_time >= SPT:
                for scene in game.scenes:
                    scene.update(SPT)
                accum_time -= SPT

            # rendering
            # ---------

            for camera in game.cameras:
                camera.renderScenes(delta)

            window.flip()
