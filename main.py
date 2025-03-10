import random
import threading
import time

from collections import Counter
from data.classes.Board import Board
from data.classes.Bot import Bot
from tiebreakers import tiebreaker

import importlib.util
import os
import copy
import builtins
from contextlib import contextmanager
import signal
import multiprocessing


class TimeoutException(Exception):
    pass


@contextmanager
def override_builtins(name, new_value):
    """Temporarily override a built-in function and restore it after use."""
    original_value = getattr(builtins, name)  # Save original function
    setattr(builtins, name, new_value)  # Override with new function
    try:
        yield  # Allow execution
    finally:
        setattr(builtins, name, original_value)  # Restore original function


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


# def run_bot_move(bot, color, board, queue):
#     move = bot.move(color, board)
#     queue.put(move)


# def safe_bot_move(bot_instance, color, board_copy):
#     # start up the queue
#     queue = multiprocessing.Queue()

#     # run the bot move in a separate process
#     process = multiprocessing.Process(
#         target=lambda: run_bot_move(bot_instance, color, board_copy, queue)
#     )

#     # start the process, wait our time
#     process.start()
#     process.join(0.1)

#     # if its still alive, kill it
#     if process.is_alive():
#         process.terminate()
#         process.join()
#         move_result = random.choice(board.get_all_valid_moves(color))
#         print("Bot timed out, making random move")
#     else:
#         move_result = queue.get()

#     return move_result


def generate_round_robin(bot_names):
    for i in range(len(bot_names)):
        for j in range(i + 1, len(bot_names)):
            yield bot_names[i], bot_names[j]


DISALLOWED_MODULES = {"os", "sys", "shutil", "subprocess", "importlib", "builtins"}


def restricted_import(name, *args, **kwargs):
    if name in DISALLOWED_MODULES:
        raise ImportError(f"Importing {name} is not allowed")
    return original_import(name, *args, **kwargs)


original_import = builtins.__import__

if __name__ == "__main__":
    # get all bot files from bots folder
    bots = os.listdir("bots")
    bots = [bot for bot in bots if bot.endswith(".py")]

    # list of bot modules, and map the name of the bot to the module
    bot_modules = []
    name_to_module = {}
    for bot in bots:
        try:
            spec = importlib.util.spec_from_file_location(bot[:-3], f"bots/{bot}")
            bot_module = importlib.util.module_from_spec(spec)

            # overide import during execution of the bot

            with override_builtins("__import__", restricted_import):
                spec.loader.exec_module(bot_module)

            bot_modules.append(bot_module)
            name_to_module[bot[:-3]] = bot_module
        except ImportError as e:
            print(f"Failed to import {bot}: {e}")

    # setup bot scorecards

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
            # make a move as bot
            board_copy = copy.deepcopy(board)

            # TODO: replace the time limit with an env variable
            if board_copy.turn == "black":
                # m = safe_bot_move(bot1_instance, "black", board_copy)
                # board.handle_move(m[0], m[1])
                # try to make the move within the time limit
                try:
                    with time_limit(1):
                        m = bot1_instance.move("black", board_copy)
                        board.handle_move(m[0], m[1])
                except TimeoutException as e:
                    # if run out of time, make a random move
                    m = random.choice(board_copy.get_all_valid_moves("black"))
                    board.handle_move(m[0], m[1])
                    print(f"making a move for the bot {bot1}")
            else:
                # m = safe_bot_move(bot2_instance, "white", board_copy)
                # board.handle_move(m[0], m[1])
                try:
                    with time_limit(1):
                        m = bot2_instance.move("white", board_copy)
                        board.handle_move(m[0], m[1])
                except TimeoutException as e:
                    m = random.choice(board_copy.get_all_valid_moves("white"))
                    board.handle_move(m[0], m[1])
                    print(f"making a move for the bot {bot2}")

            # check if there is checkmate
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
