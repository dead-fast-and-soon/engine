from engine.game import Game
from engine.asset.tileset import TilesetAsset
from engine.components.sprite import SpriteText
from engine.camera import ScreenPixelCamera
from test.panel import Panel
from engine.objects.entity import Entity
import pyglet.window.key as key

# load assets
tileset = TilesetAsset('assets/font.png', tile_width=8, tile_height=8)

# create window
screen_width = 160
screen_height = 144
game = Game(width=screen_width * 4, height=screen_height * 4)

# start new scene
scene = game.create_scene()

# use a zoomed in camera
scene.use_camera(ScreenPixelCamera, zoom=4)

# Create Panel
window = Panel((80, 0), 9, 17, scene)
window.draw_frame()


class Element(Entity):
    @Entity.spawnable
    def __init__(self, text: str):
        self.x = self.position.x
        self.y = self.position.y
        self.text = text
        self.component = self.scene.spawn_component(SpriteText,
                                              (self.x, self.y), 
                                              tileset, 
                                              self.text, layer=2)
        self.component.parent = self.root_component


class MoveElement(Entity):
    @Entity.spawnable
    def __init__(self, text: str):
        self.x = self.position.x
        self.y = self.position.y
        self.text = text
        self.component = self.scene.spawn_component(SpriteText,
                                              (self.x, self.y), 
                                              tileset, 
                                              self.text, layer=2)
        self.component.parent = self.root_component

    def on_key_press(self, symbol, modifier):
        if symbol == key.UP:
            self.position += (0, 8)
        if symbol == key.DOWN:
            self.position -= (0, 8)


# start game
scene.spawn_entity(Element, (96, 120), 'POK^DEX')
scene.spawn_entity(Element, (96, 104), 'POK^MON')
scene.spawn_entity(Element, (96, 88), 'PACK')
scene.spawn_entity(Element, (96, 72), r'#%GEAR')
scene.spawn_entity(Element, (96, 56), 'SILVER')
scene.spawn_entity(Element, (96, 40), 'SAVE')
scene.spawn_entity(Element, (96, 24), 'OPTION')
scene.spawn_entity(Element, (96, 8), 'EXIT')
scene.spawn_entity(MoveElement, (88, 104), '>')

game.start()
