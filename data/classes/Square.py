# /* Square.py


# Tile creator
class Square:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.abs_x = x * width
        self.abs_y = y * height
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (x, y)
        self.color = "light" if (x + y) % 2 == 0 else "dark"
        self.draw_color = (220, 208, 194) if self.color == "light" else (53, 53, 53)
        self.highlight_color = (100, 249, 83) if self.color == "light" else (0, 228, 10)
        self.occupying_piece = None
        self.coord = self.get_coord()
        self.highlight = False

    # get the formal notation of the tile
    def get_coord(self):
        columns = "abcdef"
        return columns[self.x] + str(self.y + 1)
