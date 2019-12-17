
import pyglet
import pyglet.window.key as key
import typing
import time

from engine.objects.entity import Entity
from engine.input import Input
from engine.state import GameState
from engine.scene import Scene
from engine.camera import Camera, PixelCamera, ScreenPixelCamera
from engine.components.debug import FpsDisplay
from engine.components.console import Console


class Game:
    """
    Manages the main game loop and gamestates.
    """

    def __init__(self, *, width, height):
        # the currently loaded gamestate
        self.state: GameState = GameState(self)

        # a list of scenes
        self.scenes: typing.List[Scene] = []

        # width and height of the window
        self.width: float = width
        self.height: float = height

        # the keyboard input object
        self.input: Input = Input()

        self.hud_scene: Scene = self.create_scene()
        self.hud_scene.use_camera(ScreenPixelCamera)
        self.hud_scene.spawn_component(FpsDisplay, (0, 0))

        self.console: Console = self.hud_scene.spawn_component(Console, (0, 0))

        # the time elapsed since the last frame
        self.last_delta: float = 0

    def log(self, message):
        """
        Logs a message into an internal console.
        """
        self.console.log(message)

    def load_scene(self, scene_class: typing.Type[Scene]) -> Scene:
        """[summary]

        Args:
            scene_class (typing.Type[Scene]): the scene to load

        Returns:
            Scene: the scene that was loaded

        """
        scene = scene_class(self)
        scene.use_camera(PixelCamera)
        scene.on_load()
        self.scenes.insert(0, scene)
        return scene

    def create_scene(self) -> Scene:
        """Create and return an empty Scene."""
        return self.load_scene(Scene)

    def render_all_scenes(self):
        """Render all scenes.

        Args:
            delta (float): change in time from the last frame
        """
        for scene in self.scenes:
            scene.render()

    def update_all_scenes(self, delta: float):
        """Update all scenes.

        Args:
            delta (float): change in time from the last tick
        """
        for scene in self.scenes:
            scene.update(delta)

    def start(self):
        """Open the main window and start the main game loop."""

        print('starting game...')

        for scene in self.scenes:
            print(' > rendering scene ({} components)'
                  .format(len(scene.components)))
        window = pyglet.window.Window(width=self.width, height=self.height,
                                      vsync=False)

        # schedule updateScenes() at fixed rate
        # pyglet.clock.schedule_interval(self.update_all_scenes, SPT)

        closed = False

        @window.event
        def on_key_press(symbol, modifiers):
            nonlocal closed
            if symbol is key.ESCAPE:
                closed = True
                window.close()

            self.input[symbol] = True

            for scene in self.scenes:
                for entity in scene.entities:
                    entity.on_key_press(symbol, modifiers)

        @window.event
        def on_key_release(symbol, modifiers):
            self.input[symbol] = False

            for scene in self.scenes:
                for entity in scene.entities:
                    entity.on_key_release(symbol, modifiers)

        last_time = time.perf_counter()
        # accum_time = 0

        # ----------------------------------------------------------------------
        #  Game Loop
        # ----------------------------------------------------------------------

        while not closed:

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

            self.update_all_scenes(delta)

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

            self.last_delta = delta
            self.render_all_scenes()

            if not closed:
                window.flip()
