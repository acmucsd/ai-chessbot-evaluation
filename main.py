import time

from collections import Counter
from data.classes.Board import Board
from data.classes.Bot import Bot
from tiebreakers import tiebreaker

import importlib.util
import os


def generate_round_robin(bot_names):
    for i in range(len(bot_names)):
        for j in range(i + 1, len(bot_names)):
            yield bot_names[i], bot_names[j]
    
if __name__ == "__main__":
    # get all bot files from bots folder
    bots = os.listdir("bots")
    bots = [bot for bot in bots if bot.endswith(".py")]

    bot_modules = []
    name_to_module = {}
    for bot in bots:
        spec = importlib.util.spec_from_file_location(bot[:-3], f"bots/{bot}")
        bot_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bot_module)
        bot_modules.append(bot_module)
        name_to_module[bot[:-3]] = bot_module

    bot_names = list(name_to_module.keys())
    scorecard = {bot: 0 for bot in bot_names}
    match_results = {bot: {} for bot in bot_names}
    # play the round robin
    for bot1, bot2 in generate_round_robin(bot_names):
        bot1_module = name_to_module[bot1]
        bot2_module = name_to_module[bot2]

        board = Board()
        bot1_instance = bot1_module.Bot()
        bot2_instance = bot2_module.Bot()
        running = True

        while running:
            if board.turn == "black":
                m = bot1_instance.move("black", board)
                board.handle_move(m[0], m[1])
            else:
                m = bot2_instance.move("white", board)
                board.handle_move(m[0], m[1])

            if board.is_in_checkmate("black"):
                print(f"{bot2} wins!")
                running = False
                scorecard[bot2] += 3
                match_results[bot1][bot2] = "L"
                match_results[bot2][bot1] = "W"
            elif board.is_in_checkmate("white"):
                print(f"{bot1} wins!")
                running = False
                scorecard[bot1] += 3
                match_results[bot1][bot2] = "W"
                match_results[bot2][bot1] = "L"
            # add draw condition later
    scorecard = tiebreaker(scorecard, match_results)
    print(scorecard)
    print(match_results)
