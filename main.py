
from engine.game import Game

from game.entities.block import BlockGrid

# construct game window
game = Game(width=1280, height=720)

# spawn entities
game.scene.spawnEntity(BlockGrid, (0, 0))

# start game
print('starting game')
game.start()
