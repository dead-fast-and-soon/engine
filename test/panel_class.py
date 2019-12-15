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


# spawn sprites
class Panel():
    def __init__(self, frame_width, frame_height, frame_offset_x, frame_offset_y):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_offset_x = frame_offset_x
        self.frame_offset_y = frame_offset_y


    def width_length(self):
        # Top Left
        scene.spawn_component(Sprite, (self.frame_offset_x,
                                       self.frame_offset_y + self.frame_height
                                       * 8), frame.get_tile(0))

        # Bottom Left
        scene.spawn_component(Sprite, (self.frame_offset_x,
                              self.frame_offset_y), frame.get_tile(4))

        # Top Right
        scene.spawn_component(Sprite, (self.frame_offset_x + self.frame_width
                                       * 8, self.frame_offset_y
                                       + self.frame_height * 8),
                                       frame.get_tile(2))

        # Bottom Right
        scene.spawn_component(Sprite, (self.frame_offset_x + self.frame_width
                                       * 8, self.frame_offset_y),
                                       frame.get_tile(5))

        for idx in range(self.frame_width):
            scene.spawn_component(Sprite, (idx * 8 + self.frame_offset_x + 8,
                                           self.frame_height * 8
                                           + self.frame_offset_y),
                                           frame.get_tile(1))

            scene.spawn_component(Sprite, (idx * 8 + self.frame_offset_x + 8,
                                           0 + self.frame_offset_y),
                                           frame.get_tile(1))


    def height_length(self):
        for idx in range(self.frame_height):
            scene.spawn_component(Sprite, (self.frame_offset_x, idx * 8
                                           + self.frame_offset_y + 8),
                                           frame.get_tile(3))

            scene.spawn_component(Sprite, (self.frame_offset_x
                                           + self.frame_width * 8, idx * 8
                                           + self.frame_offset_y),
                                           frame.get_tile(3))


    def fill_frame(self):
        for idx in range(self.frame_width - 1):
            for idy in range(self.frame_height - 1):
                scene.spawn_component(Sprite, (idx * 8 + self.frame_offset_x
                                               + 8, idy * 8
                                               + self.frame_offset_y + 8),
                                               white_block.get_tile(0))


# start game
window = Panel(9, 17, 80, 0)
window.width_length()
window.height_length()
window.fill_frame()
window2 = Panel(11, 6, -8, -8)
window2.fill_frame()
game.start()
