
from engine.game import Game
from engine.components.shapes import Box2D, Circle2D


game = Game(width=160, height=160)

scene = game.create_scene()

scene.spawn_component(Box2D, (10, 10), size=(50, 50), color=(0, 255, 0))
scene.spawn_component(Box2D, (10, -60), size=(50, 50), color=(0, 0, 255), is_filled=False)
scene.spawn_component(Circle2D, (-35, -35), n=10, radius=25, color=(0, 255, 255))
scene.spawn_component(Circle2D, (-35, 35), n=7, radius=25, color=(255, 255, 0), is_filled=False)

game.start()
