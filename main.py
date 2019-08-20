
from engine.game import Game

from game.entities.block import BlockGrid

# construct game window
game = Game(width=1280, height=720)

camera = game.addCamera()
scene = game.newScene()

# spawn entities
scene.spawnEntity(BlockGrid, (0, 0))
camera.assignScene(scene)

# start game
print('starting game')
game.start()
