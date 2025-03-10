import random
import time


class Bot:
    def __init__(self):
        pass

    def get_possible_moves(self, side, board):
        return board.get_all_valid_moves(side)

    def move(self, side, board):
        # pick a random move for now
        moves = self.get_possible_moves(side, board)
        move = random.choice(moves)
        move = moves[-1]
        time.sleep(5)
        return move
