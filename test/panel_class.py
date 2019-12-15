from engine.game import Game
from engine.asset.tileset import TilesetAsset
from engine.components.sprite import Sprite
from engine.camera import ScreenPixelCamera

# load assets
frame = TilesetAsset('assets/frame1.png', tile_width=8, tile_height=8)
white_block = TilesetAsset('assets/white_block.png', tile_width=8, tile_height=8)

# create window
screen_width = 160
screen_height = 144
game = Game(width=screen_width * 4, height=screen_height * 4)

# start new scene
scene = game.create_scene()

# use a zoomed in camera
scene.use_camera(ScreenPixelCamera, zoom=4)


TILE_SIZE = 8

TILE_TL = frame.get_tile(0)
TILE_BL = frame.get_tile(4)
TILE_TR = frame.get_tile(2)
TILE_BR = frame.get_tile(5)
TILE_V = frame.get_tile(3)
TILE_H = frame.get_tile(1)


# spawn sprites
class Panel():

    def __init__(self, position: tuple, frame_width, frame_height):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.x = position[0]
        self.y = position[1]

    def draw_frame(self):

        x, y = self.x, self.y
        height, width = self.frame_height, self.frame_width

        # draw corners
        # Top Left
        scene.spawn_component(Sprite, (x, y + height * TILE_SIZE), TILE_TL)

        # Bottom Left
        scene.spawn_component(Sprite, (x, y), TILE_BL)

        # Top Right
        scene.spawn_component(Sprite, (x + width * TILE_SIZE,
                                       y + height * TILE_SIZE), TILE_TR)
        # Bottom Right
        scene.spawn_component(Sprite, (x + width * TILE_SIZE, y), TILE_BR)

        # draw horizontal outlines
        for idx in range(self.frame_width):
            scene.spawn_component(Sprite, (idx * TILE_SIZE + x + TILE_SIZE,
                                           height * TILE_SIZE + y), TILE_H)

            scene.spawn_component(Sprite, (idx * TILE_SIZE + x + TILE_SIZE,
                                           0 + y), TILE_H)

        # draw vertical outlines
        for idx in range(self.frame_height):
            scene.spawn_component(Sprite, (x, idx * TILE_SIZE
                                           + y + TILE_SIZE), TILE_V)

            scene.spawn_component(Sprite, (x + width * TILE_SIZE,
                                           idx * TILE_SIZE + self.y), TILE_V)

        # draw inner fill
        for idx in range(self.frame_width - 1):
            for idy in range(self.frame_height - 1):
                scene.spawn_component(Sprite,
                                      (idx * TILE_SIZE + x + TILE_SIZE,
                                       idy * TILE_SIZE + y + TILE_SIZE),
                                      white_block.get_tile(0))

# start game
window = Panel((80, 0), 9, 17)
window.draw_frame()
window2 = Panel((-8, -8), 11, 6)
window2.draw_frame()
game.start()
