from engine.game import Game
from engine.asset.tileset import TilesetAsset
from engine.components.sprite import Sprite
from engine.camera import ScreenPixelCamera
from engine.objects.component import BatchComponent
from engine.components.shapes import Box2D
from structs.vector import Vector


# spawn sprites
class Panel(BatchComponent):
    def on_spawn(self, frame_width, frame_height, borders: bool = True,
                 layer: int = 0):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame = TilesetAsset(
            'assets/frame1.png', tile_width=8, tile_height=8
        )
        self.borders = borders
        TILE_SIZE = 8

        TILE_TL = self.frame.get_tile(0)
        TILE_BL = self.frame.get_tile(4)
        TILE_TR = self.frame.get_tile(2)
        TILE_BR = self.frame.get_tile(5)
        TILE_V = self.frame.get_tile(3)
        TILE_H = self.frame.get_tile(1)

        ox, oy = self.position.x, self.position.y
        height, width = self.frame_height, self.frame_width

        border_offset = (8, 8)

        if self.borders is True:
            # draw corners
            # Top Left

            for x in range(0, width):
                for y in range(0, height):
                    adj_pos = self.position + (Vector(x, y) * TILE_SIZE)

                    if (x, y) == (0, 0):
                        tile = TILE_BL

                    elif (x, y) == (0, height - 1):
                        tile = TILE_TL

                    elif (x, y) == (width - 1, height - 1):
                        tile = TILE_TR

                    elif (x, y) == (width - 1, 0):
                        tile = TILE_BR

                    elif x == 0 or x == width - 1:
                        tile = TILE_V

                    elif y == 0 or y == height - 1:
                        tile = TILE_H

                    else:
                        tile = None

                    if tile:
                        self.create_component(Sprite, adj_pos,
                                              tile, layer=layer)

        # draw inner fill
        if borders:
            self.create_component(
                Box2D, self.position + border_offset,
                ((width - 2) * TILE_SIZE, (height - 2) * TILE_SIZE),
                (255, 255, 255), layer=layer
            )
        else:
            self.create_component(
                Box2D, self.position,
                (width * TILE_SIZE, height * TILE_SIZE),
                (255, 255, 255), layer=layer
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

    scene.spawn_component(Panel, (0, 0), 4, 4, True, layer=0)
    scene.spawn_component(Panel, (16, 16), 4, 4, True, layer=1)
    game.start()
