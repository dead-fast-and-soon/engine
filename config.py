from structs.point import Point

# sprite pixel width and height
SPRITE_SIZE = 8

# gameboy color screen resolution
GBC_W = 160
GBC_H = 144

# gbc screen *4
WIDTH = GBC_W * 4
HEIGHT = GBC_H * 4


BOT_LEFT = Point(0, 0)
BOT_CENTER = Point(WIDTH // 2, 0)
BOT_RIGHT = Point(WIDTH, 0)
CEN_LEFT = Point(0, HEIGHT // 2)
CENTER = Point(WIDTH // 2, HEIGHT // 2)
CEN_RIGHT = Point(WIDTH, HEIGHT // 2)
TOP_LEFT = Point(0, HEIGHT)
TOP_CENTER = Point(WIDTH // 2, HEIGHT)
TOP_RIGHT = Point(WIDTH, HEIGHT)

