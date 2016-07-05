#!/usr/bin/env python3
"""
Judge
"""

from player_random import RandomPlayer
from player_baier import BaierPlayer
from board import Board


def play_match(white, black, time_limit=5):
    """
    Runs a single match

    white: Class for the White player
    black: Class for the Black player

    output: The Winner class
    """

    # Create players for each role
    player_white = white(Board.WHITE, time_limit)
    player_black = black(Board.BLACK, time_limit)

    white_name = "W-"+player_white.__class__.__name__
    black_name = "B-"+player_black.__class__.__name__

    # Start new Board
    board = Board()
    plies = 0

    # Run the match
    while True:

        # White plays
        print(board)
        board_copy = Board(board)  # Don't trust white
        (queen, nq_x, nq_y, a_x, a_y) = (None, None, None, None, None)
        try:
            if board_copy.can_play(Board.WHITE):
                queen, nq_x, nq_y, a_x, a_y = player_white.play(board_copy)
                Board.show_move(white_name, queen, nq_x, nq_y, a_x, a_y)
                plies += 1
            else:
                # White can't move. Black won
                print("%s won" % black_name)
                return (black, plies)
        except Exception as e:
            print("%s won.  %s lost by Exception(%s)" % (black_name, white_name, e))
            return (black, plies)

        # Update real board
        board = board.succ(queen, nq_x, nq_y, a_x, a_y)

        # Black plays
        print(board)
        board_copy = Board(board)  # Don't trust black
        (queen, nq_x, nq_y, a_x, a_y) = (None, None, None, None, None)
        try:
            if board_copy.can_play(Board.BLACK):
                queen, nq_x, nq_y, a_x, a_y = player_black.play(board_copy)
                Board.show_move(black_name, queen, nq_x, nq_y, a_x, a_y)
                plies += 1
            else:
                # Black can't move. White won
                print("%s won" % white_name)
                return (white, plies)
        except Exception as e:
            print("%s won.  %s lost by Exception(%s)" % (white_name, black_name, e))
            return (white, plies)

        # Update real board
        board = board.succ(queen, nq_x, nq_y, a_x, a_y)


PLAYERS = [RandomPlayer]
RIVAL = BaierPlayer

GAMES = dict()
GAMES[BaierPlayer] = 0

SCORES = dict()
SCORES[BaierPlayer] = 0

for p in PLAYERS:
    GAMES[p] = 0
    SCORES[p] = 0


ROUNDS = 2
TIME_LIMIT = 2
for player in PLAYERS:

    tied = True
    for _ in range(ROUNDS):
        (winner1, _) = play_match(RIVAL, player, TIME_LIMIT)
        SCORES[winner1] += 1
        (winner2, _) = play_match(player, RIVAL, TIME_LIMIT)
        SCORES[winner2] += 1
        GAMES[RIVAL] += 2
        GAMES[player] += 2

        if winner1 == winner2:
            tied = False
    if tied:
        (winner3, _) = play_match(RIVAL, player, TIME_LIMIT)
        SCORES[winner3] += 1
        GAMES[RIVAL] += 1
        GAMES[player] += 1

print()
print("Results:")
print("  * %20s: %d/%d" % (RIVAL.__name__, SCORES[RIVAL], GAMES[RIVAL]))
for p in PLAYERS:
    print("  * %20s: %d/%d" % (p.__name__, SCORES[p], GAMES[p]))
