
from engine.game import Game
from engine.asset.tileset import TilesetAsset
from engine.components.sprite import SpriteText
from engine.camera import PixelCamera

# load assets
tileset = TilesetAsset('assets/font.png', tile_width=8, tile_height=8)

# create window
game = Game(width=1280, height=720)

# start new scene
scene = game.create_scene()

# use a zoomed in camera
scene.use_camera(PixelCamera, zoom=4)

# spawn sprites
scene.spawn_component(SpriteText, (0, 8), tileset, 'hello')

# start game
game.start()
