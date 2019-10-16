from structs.vector import Vector

# sprite pixel width and height
SPRITE_SIZE = 8

# gameboy color screen resolution
GBC_W = 160
GBC_H = 144

# gbc screen *4
WIDTH = GBC_W * 4
HEIGHT = GBC_H * 4


BOT_LEFT = Vector(0, 0)
BOT_CENTER = Vector(WIDTH // 2, 0)
BOT_RIGHT = Vector(WIDTH, 0)
CEN_LEFT = Vector(0, HEIGHT // 2)
CENTER = Vector(WIDTH // 2, HEIGHT // 2)
CEN_RIGHT = Vector(WIDTH, HEIGHT // 2)
TOP_LEFT = Vector(0, HEIGHT)
TOP_CENTER = Vector(WIDTH // 2, HEIGHT)
TOP_RIGHT = Vector(WIDTH, HEIGHT)

