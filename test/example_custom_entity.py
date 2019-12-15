
import math

from engine.game import Game
from engine.asset.tileset import TilesetAsset
from engine.objects.entity import Entity
from engine.components.sprite import SpriteText
from engine.camera import PixelCamera


class ExampleEntity(Entity):

    @Entity.spawnable
    def __init__(self, text: str, speed: float):

        tileset = TilesetAsset('assets/font.png', tile_height=8, tile_width=8)

        sprite = self.scene.spawn_component(SpriteText, (0, 0),
                                            tileset, text)
        sprite.parent = self.root_component

        self.time: float = 0
        self.speed = speed

    def on_update(self, delta: float):

        self.position = (math.sin(self.time * self.speed) * 10,
                         math.cos(self.time * self.speed) * 10)
        self.time += delta


game = Game(width=1280, height=720)

scene = game.create_scene()
scene.use_camera(PixelCamera, zoom=4.0)
scene.spawn_entity(ExampleEntity, (-10, 5), 'hello there', 2)
scene.spawn_entity(ExampleEntity, (10, -5), 'what', 3)

game.start()
