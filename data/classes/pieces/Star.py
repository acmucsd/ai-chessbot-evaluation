# /* Kinght.py

from data.classes.Piece import Piece


class Star(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)

        self.notation = "N"

    def get_possible_moves(self, board):
        output = []
        moves = [(1, 1), (-1, 1), (1, -1), (-1, -1), (2, 0), (-2, 0), (0, 2), (0, -2)]
        for move in moves:
            new_pos = (self.x + move[0], self.y + move[1])
            if (
                new_pos[0] < 6
                and new_pos[0] >= 0
                and new_pos[1] < 6
                and new_pos[1] >= 0
            ):
                output.append([board.get_square_from_pos(new_pos)])
        return output
