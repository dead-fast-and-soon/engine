
import math

from engine.game import Game
from engine.asset.tileset import TilesetAsset
from engine.objects.entity import Entity
from engine.objects.component import fixed_rate
from engine.components.shapes import Box2D
from engine.components.sprite import SpriteText
from engine.camera import PixelCamera
from structs.vector import Vector


class ExampleEntity(Entity):

    @Entity.spawnable
    def __init__(self, text: str, speed: float):

        tileset = TilesetAsset('assets/font.png', tile_height=8, tile_width=8)

        sprite = self.create_component(SpriteText, (0, 8),
                                       tileset, text)
        box = self.create_component(Box2D, (0, 0),
                                    size=(8, 8), color=(0, 0, 255))
        sprite.parent = self.root_component
        box.parent = self.root_component

        self.time: float = 0
        self.speed = speed

    @fixed_rate(60)
    def on_update(self, delta: float):
        self.position = Vector((math.cos(self.time * self.speed) * 10,
                                math.sin(self.time * self.speed) * 10))
        self.time += delta

    def on_key_press(self, symbol, modifier):
        print(symbol)


game = Game(width=1280, height=720)

scene = game.create_scene()
scene.use_camera(PixelCamera, zoom=4.0)
scene.spawn_entity(ExampleEntity, (0, 0), 'hello there', 2)
# scene.spawn_entity(ExampleEntity, (10, -5), 'what', 3)

game.start()
