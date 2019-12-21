
from engine.game import Game
from engine.asset.tileset import TilesetAsset
from engine.camera import PixelCamera
from game.entities.player import Player

WIDTH, HEIGHT = 160, 144

game = Game(width=WIDTH * 4, height=HEIGHT * 4)

scene = game.create_scene()
scene.use_camera(PixelCamera, zoom=4)

scene.spawn_entity(Player)

game.start()
