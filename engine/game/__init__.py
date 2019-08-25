
import pyglet
import pyglet.window.key as key
import typing
import time

from engine.entity import Entity
from engine.input import Input
from engine.game.state import GameState
from engine.game.scene import Scene
from engine.camera import Camera, ScreenPixelCamera
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

        # the keyboard input object
        self.input: Input = Input()

        # add an in-game debug console
        self.console = Console((20, 20), game=self)
        self.fps_display = FpsDisplay((0, 0))

        hud_scene = Scene(self)
        hud_scene.components.append(self.console)
        hud_scene.components.append(self.fps_display)

        hud_view = ScreenPixelCamera(self)
        hud_view.assignScene(hud_scene)
        self.cameras.append(hud_view)

    def log(self, message):
        """
        Logs a message into an internal console.
        """
        self.console.log(message)

    def loadScene(self, scene_class: typing.Type[Scene]) -> Scene:
        """[summary]

        Args:
            scene_class (typing.Type[Scene]): the scene to load

        Returns:
            Scene: the scene that was loaded

        """
        scene = scene_class(self)
        scene.onLoad()
        self.scenes.append(scene)
        return scene

    def createScene(self):
        """Create and return an empty Scene."""
        self.loadScene(Scene)

    def createCamera(self, camera_class: typing.Type[Camera] = None,
                     *args, **kwargs):
        """Create and return a Camera object."""
        if camera_class is None:
            camera_class = Camera

        camera = camera_class(self, *args, **kwargs)  # type: ignore
        self.cameras.append(camera)
        return camera

    def renderScenes(self, delta: float):
        """Render all scenes.

        Args:
            delta (float): change in time from the last frame
        """
        for camera in self.cameras:
            camera.renderScene(delta)

    def updateScenes(self, delta: float):
        """Update all scenes.

        Args:
            delta (float): change in time from the last tick
        """
        for scene in self.scenes:
            scene.update(delta)

    def start(self):
        """Open the main window and start the main game loop."""

        window = pyglet.window.Window(width=self.width, height=self.height,
                                      vsync=False)

        # schedule updateScenes() at fixed rate
        pyglet.clock.schedule_interval(self.updateScenes, SPT)

        @window.event
        def on_key_press(symbol, modifiers):
            if symbol is key.ESCAPE:
                window.close()

            self.input[symbol] = True

            for scene in self.scenes:
                for component in scene.components:
                    if isinstance(component, Entity):
                        component.onKeyPress(symbol, modifiers)

        @window.event
        def on_key_release(symbol, modifiers):
            self.input[symbol] = False

            for scene in self.scenes:
                for component in scene.components:
                    if isinstance(component, Entity):
                        component.onKeyRelease(symbol, modifiers)

        last_time = time.perf_counter()
        # accum_time = 0

        # update scenes at 0th tick
        self.updateScenes(SPT)

        # ----------------------------------------------------------------------
        #  Game Loop
        # ----------------------------------------------------------------------

        while True:

            pyglet.clock.tick()

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

            # accum_time += delta

            # # if accumulative dt goes above SPT, run a tick and decrement
            # # while accum_time >= SPT:
            # #     self.updateScenes(SPT)
            # #     accum_time -= SPT
            # if accum_time >= SPT:
            #     self.updateScenes(SPT)
            #     accum_time = 0

            # rendering
            # ---------

            self.renderScenes(delta)

            window.flip()
