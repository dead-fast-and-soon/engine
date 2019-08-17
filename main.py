
from engine.game import Game

from game.entities.block import BlockGrid

# construct game window
game = Game(width=1280, height=720)

# spawn entities
game.scene.spawnEntity(BlockGrid(view=game.view, scene=game.scene))

# start game
print('starting game')
game.start()
