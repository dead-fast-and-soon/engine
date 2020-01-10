import pyglet
import typing
import time

from konkyo.objects.entity import Entity
from konkyo.input import InputHandler
from konkyo.state import GameState
from konkyo.scene import Scene
from konkyo.camera import Camera, PixelCamera, ScreenPixelCamera
from konkyo.components.debug import FpsDisplay
from konkyo.components.console import Console
from konkyo.graphics import BatchRenderer
from konkyo.utils.gl import *


class _FrameTimer:
    def __init__(self):

        # initial time
        self._ti = time.perf_counter()

        # final time
        self._tf = self._ti

        # delta time
        self._delta = self._tf - self._ti

    def tick(self):

        self._tf = time.perf_counter()

        self._delta = self._tf - self._ti

        self._ti = self._tf

    @property
    def delta(self):
        return self._delta


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
        self.input: InputHandler = InputHandler()

        # the time elapsed since the last frame
        self.last_delta: float = 0

        self.window = pyglet.window.Window(width=width,
                                           height=height,
                                           vsync=False)

        self._closed = False

        self._on_update = lambda x: None

    def log(self, message):
        """
        Logs a message into an internal console.
        """
        self.console.log(message)

    def create_scene(self,
                   scene_class: typing.Type[Scene] = None,
                   name: str = None) -> Scene:
        """[summary]

        Args:
            scene_class (typing.Type[Scene]): the scene to load

        Returns:
            Scene: the scene that was loaded

        """
        scene_class = scene_class or Scene
        scene = scene_class(self, name)
        scene.on_load()
        self.scenes.insert(0, scene)
        return scene

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

        pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
        pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

        print('starting game...')

        # manually bind WindowBlock buffer to 0
        GLUniformBuffer(1).set_binding_point(0)

        # add fps and console objects
        hud_scene: Scene = self.create_scene(name='HUD')
        hud_scene.use_camera(ScreenPixelCamera(zoom=1.0))
        self.fps_disp = hud_scene.spawn_component(FpsDisplay, (0, 0))
        self.console: Console = hud_scene.spawn_component(Console, (0, 20))

        @self.window.event
        def on_key_press(symbol, modifiers):

            if symbol is pyglet.window.key.ESCAPE:
                self._closed = True
                self.window.close()

            self.input.set_key(symbol, True)

            [[
                entity.on_key_press(symbol, modifiers)
                for entity in scene.entities
            ] for scene in self.scenes]

        @self.window.event
        def on_key_release(symbol, modifiers):

            self.input.set_key(symbol, False)

            [[
                entity.on_key_release(symbol, modifiers)
                for entity in scene.entities
            ] for scene in self.scenes]

        print('rendering %d scenes:' % len(self.scenes))
        for scene in self.scenes:
            print(' - "{}" ({} components)'.format(scene.name,
                                                   len(scene.components)))

        timer = _FrameTimer()

        # from game.graphics.shaders import program

        # class Group(pyglet.graphics.Group):
        #     def set_state(self):
        #         super().set_state()
        #         self.program['projection'] = pyglet.matrix.create_orthogonal(0, 100, 0, 100, 0, 1)

        # batch = pyglet.graphics.Batch()
        # group = Group(program)
        # batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, group, [0, 1, 2, 0, 2, 3],
        #         ("vertices2f", (0, 0, 0, 600, 100, 600, 100, 0)),
        #         ("colors3f", (1.0, 1.0, 1.0) * 4))

        while not self._closed:

            timer.tick()

            # fire any pyglet events
            pyglet.clock.tick()
            self.window.switch_to()
            self.window.dispatch_events()

            self.window.clear()

            # update and render scenes
            self.update_all_scenes(timer.delta)
            self.render_all_scenes()
            self._on_update(timer.delta)
            # batch.draw()

            self.window.flip()

    def event_listener(self, fn):
        self._on_update = fn
        return fn
