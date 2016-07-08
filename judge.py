#!/usr/bin/env python3
"""
Judge
"""

from time import time
from argparse import ArgumentParser

from color_print import Color

from board import Board

from player_random import RandomPlayer
from player_baier import BaierPlayer
from player_uct_julio import JulioMonteCarlo
from player_salas_a import Jorge_SalasA
from player_salas_d import Jorge_SalasD
from player_oliva import OlivaPlayer
from player_wolf import WolfPlayer
from player_felix import FelixPlayer
from player_gomez import KocoPlayer
from player_franco import FMPlayer
from player_gasevi import GaseviPlayer
from ivan_player import MapachePlayer

PARSER = ArgumentParser(description='Process some queries')

PARSER.add_argument('--margin', metavar='M', type=float, default=1.2,
                    help='Extra time before disqualification')
PARSER.add_argument('--turns', metavar='n', type=int, default=100,
                    help='Turn limit (100)')
PARSER.add_argument('--time', metavar='t', type=int, default=5,
                    help='Time limit (5s)')
PARSER.add_argument('--rounds', metavar='r', type=int, default=1,
                    help='Rounds to play (1 => Best of 2*r+1 games)')

PARSER.add_argument('--p1', metavar='a', type=int, default=-1,
                    help='Player 1 index')
PARSER.add_argument('--p2', metavar='b', type=int, default=-1,
                    help='Player 2 index')
ARGS = PARSER.parse_args()

TIME_MARGIN = ARGS.margin
ROUNDS = ARGS.rounds
TURNS = ARGS.turns
TIME_LIMIT = ARGS.time
P1 = ARGS.p1
P2 = ARGS.p2


def play_match(white, black, time_limit=5, turn_limit=100):
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

    if turn_limit < 100:
        Color.YELLOW.print("####################")
        Color.YELLOW.print("TURN LIMIT SET TO %d" % turn_limit)
        Color.YELLOW.print("####################")
    if time_limit < 2:
        Color.YELLOW.print("--------------------")
        Color.YELLOW.print("TIME LIMIT SET TO %d" % time_limit)
        Color.YELLOW.print("--------------------")

    # Run the match
    for _ in range(turn_limit):
        # White plays
        print(board)
        board_copy = Board(board)  # Don't trust white
        (queen, nq_x, nq_y, a_x, a_y) = (None, None, None, None, None)
        try:
            if board_copy.can_play(Board.WHITE):
                t = time()
                queen, nq_x, nq_y, a_x, a_y = player_white.play(board_copy)
                if time() - t > TIME_MARGIN * time_limit:
                    raise Exception("TLE")
                Board.show_move(white_name, queen, nq_x, nq_y, a_x, a_y)
                plies += 1
            else:
                # White can't move. Black won
                print("%s won" % black_name)
                return (black, plies, None)
        except Exception as e:
            print("%s won.  %s lost by Exception(%s)" % (black_name, white_name, Color.RED(e)))
            return (black, plies, white)

        # Update real board
        board = board.succ(queen, nq_x, nq_y, a_x, a_y)

        # Black plays
        print(board)
        board_copy = Board(board)  # Don't trust black
        (queen, nq_x, nq_y, a_x, a_y) = (None, None, None, None, None)
        try:
            if board_copy.can_play(Board.BLACK):
                t = time()
                queen, nq_x, nq_y, a_x, a_y = player_black.play(board_copy)
                if time() - t > TIME_MARGIN * time_limit:
                    raise Exception("TLE")
                Board.show_move(black_name, queen, nq_x, nq_y, a_x, a_y)
                plies += 1
            else:
                # Black can't move. White won
                print("%s won" % white_name)
                return (white, plies, None)
        except Exception as e:
            print("%s won.  %s lost by Exception(%s)" % (white_name, black_name, Color.RED(e)))
            return (white, plies, black)

        # Update real board
        board = board.succ(queen, nq_x, nq_y, a_x, a_y)

    # Game terminated
    print("Turn limit reached, no winner")
    return (None, 0, None)


PLAYERS = [
    FelixPlayer,                 # 0 Felix     Fischer
    KocoPlayer,                  # 1 Rodrigo   Gómez
    JulioMonteCarlo,             # 2 Julio     Hurtado
    FMPlayer,                    # 3 Franco    Muñoz
    OlivaPlayer,                 # 4 Sebastián Oliva
    MapachePlayer,               # 5 Iván      Rubio
    Jorge_SalasA, Jorge_SalasD,  # 6 Jorge     Salas
    GaseviPlayer,                # 7 Gabriel   Sepúlveda
    WolfPlayer,                  # 8 Iván      Wolf
    RandomPlayer
]
RIVAL = BaierPlayer

SHAME = dict()
SHAME[RIVAL] = 0
SHAME[None] = 0

GAMES = dict()
GAMES[RIVAL] = 0
GAMES[None] = 0

SCORES = dict()
SCORES[RIVAL] = 0
SCORES[None] = 0

for p in PLAYERS:
    GAMES[p] = 0
    SCORES[p] = 0
    SHAME[p] = 0


def duel(p1, p2, untie=False, tl=TIME_LIMIT, turns=TURNS, rounds=ROUNDS):
    """
    Plays a match
    """
    tied = True
    w1, w2 = (0, 0)
    for _ in range(rounds):

        (winner1, _, s) = play_match(p1, p2, tl, turns)
        SCORES[winner1] += 1
        GAMES[p1] += 1
        GAMES[p2] += 1
        if s:
            SHAME[s] += 1
        if winner1==p1:
            w1 += 1
        else:
            w2 += 1

        (winner2, _, s) = play_match(p2, p1, tl, turns)
        SCORES[winner2] += 1
        GAMES[p1] += 1
        GAMES[p2] += 1
        if s:
            SHAME[s] += 1
        if winner2==p1:
            w1 += 1
        else:
            w2 += 1

        if winner1 == winner2:
            tied = False

    if untie and tied:
        (winner3, _, s) = play_match(p1, p2, tl, turns)
        SCORES[winner3] += 1
        GAMES[p1] += 1
        GAMES[p2] += 1
        if s:
            SHAME[s] += 1
        if winner3==p1:
            w1 += 1
        else:
            w2 += 1

    return (w1, w2)



def rival():
    for player in PLAYERS:
        duel(RIVAL, player, True)

try:
    if P1 < 0 or P2 < 0:
        rival()
    else:
        P1 = PLAYERS[P1]
        P2 = PLAYERS[P2]
        PLAYERS = [P1, P2]
        RIVAL = None

        p1_name = P1.__name__
        p2_name = P2.__name__

        print("Match: %s v/s %s" % (p1_name, p2_name))
        print("  Rounds: %d" % ROUNDS)
        print("  TL: %ds" % TIME_LIMIT)
        if TURNS != 100:
            print("  Turns: %d" % TURNS)
        print("--")

        (w1, w2) = duel(P1, P2)
        fn = '%ds-%dr_%s-%s-wins.out' % (TIME_LIMIT, ROUNDS, p1_name, p2_name)

        with open(fn, 'w') as fd:
            for _ in range(w1):
                fd.write('%s\n' % p1_name)
            for _ in range(w2):
                fd.write('%s\n' % p2_name)

except KeyboardInterrupt:
    pass

print()
print("Results:")
if RIVAL is not None:
    print("  * %20s: %d/%d" % (RIVAL.__name__, SCORES[RIVAL], GAMES[RIVAL]))
for p in PLAYERS:
    print("  * %20s: %d/%d" % (p.__name__, SCORES[p], GAMES[p]))
print("Unfinished games: %d" % SCORES[None])

print()
print("Shame:")
if RIVAL is not None and SHAME[RIVAL] > 0:
    print("  =( %20s: %d" % (RIVAL.__name__, SHAME[RIVAL]))
for p in PLAYERS:
    if SHAME[p] > 0:
        print("  =( %20s: %d" % (p.__name__, SHAME[p]))
