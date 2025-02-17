import time

from data.classes.Board import Board
from data.classes.Bot import Bot


board = Board()


if __name__ == "__main__":
    running = True
    bot1 = Bot("black", board)
    bot2 = Bot("white", board)
    while running:

        if board.turn == "black":
            bot1.move()
            # time.sleep(1)
        else:
            bot2.move()
            # time.sleep(1)

        if board.is_in_checkmate("black"):  # If black is in checkmate
            print("White wins!")
            running = False
        elif board.is_in_checkmate("white"):  # If white is in checkmate
            print("Black wins!")
            running = False
