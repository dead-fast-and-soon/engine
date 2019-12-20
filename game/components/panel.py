from engine.game import Game
from engine.asset.tileset import TilesetAsset
from engine.components.sprite import Sprite
from engine.camera import ScreenPixelCamera
from engine.objects.component import BatchComponent
from engine.components.shapes import Box2D


# spawn sprites
class Panel(BatchComponent):
    def on_spawn(self, frame_width, frame_height, borders: bool):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame = TilesetAsset('assets/frame1.png', tile_width=8, tile_height=8)
        self.borders = borders
        TILE_SIZE = 8

        TILE_TL = self.frame.get_tile(0)
        TILE_BL = self.frame.get_tile(4)
        TILE_TR = self.frame.get_tile(2)
        TILE_BR = self.frame.get_tile(5)
        TILE_V = self.frame.get_tile(3)
        TILE_H = self.frame.get_tile(1)

        x, y = self.position.x, self.position.y
        height, width = self.frame_height, self.frame_width

        if self.borders is True:
            # draw corners
            # Top Left
            self.create_component(
                Sprite, (x, y + height * TILE_SIZE), TILE_TL, layer=1
            )

            # Bottom Left
            self.create_component(Sprite, (x, y), TILE_BL, layer=1)

            # Top Right
            self.create_component(
                Sprite, (x + width * TILE_SIZE, y + height * TILE_SIZE), TILE_TR, 
                layer=1
            )
            # Bottom Right
            self.create_component(
                Sprite, (x + width * TILE_SIZE, y), TILE_BR, layer=1
            )

            # draw horizontal outlines
            for idx in range(self.frame_width):
                self.create_component(Sprite, (idx * TILE_SIZE + x + TILE_SIZE,
                                            height * TILE_SIZE + y), TILE_H)

                self.create_component(Sprite, (idx * TILE_SIZE + x + TILE_SIZE,
                                            0 + y), TILE_H)

            # draw vertical outlines
            for idx in range(self.frame_height):
                self.create_component(Sprite, (x, idx * TILE_SIZE
                                            + y + TILE_SIZE), TILE_V)

                self.create_component(Sprite, (x + width * TILE_SIZE,
                                            idx * TILE_SIZE + y), TILE_V)

        # draw inner fill
        self.create_component(
            Box2D, (x, y),
            (width * TILE_SIZE, height * TILE_SIZE), 
            (255, 255, 255)
        )

# start game
if __name__ == '__main__':
    # create window
    screen_width = 160
    screen_height = 144
    game = Game(width=screen_width * 4, height=screen_height * 4)

    # start new scene
    scene = game.create_scene()

    # use a zoomed in camera
    scene.use_camera(ScreenPixelCamera, zoom=4)

    scene.spawn_component(Panel, (0, 0), 2, 2)
    game.start()
