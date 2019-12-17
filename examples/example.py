
from engine.game import Game
from engine.asset.tileset import TilesetAsset
from engine.components.sprite import Sprite
from engine.camera import PixelCamera

# load assets
tileset = TilesetAsset('assets/frame1.png', tile_width=8, tile_height=8)

# create window
game = Game(width=1280, height=720)

# start new scene
scene = game.create_scene()

# use a zoomed in camera
scene.use_camera(PixelCamera, zoom=4)

# spawn sprites
scene.spawn_component(Sprite, (0, 0), tileset.get_tile(0))
scene.spawn_component(Sprite, (16, 0), tileset.get_tile(1))
scene.spawn_component(Sprite, (32, 0), tileset.get_tile(2))
scene.spawn_component(Sprite, (48, 0), tileset.get_tile(3))
scene.spawn_component(Sprite, (64, 0), tileset.get_tile(4))
scene.spawn_component(Sprite, (80, 0), tileset.get_tile(5))

# start game
game.start()
