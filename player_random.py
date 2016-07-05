"""
Random
"""

from random import choice
from signal import alarm, signal, SIGALRM


class RandomPlayer:
    """Random"""

    def __init__(self, color, time=1):
        self.color = color
        self.time = time

    def play(self, board_copy):
        def handler(signum, frame):
            raise IOError

        signal(SIGALRM, handler)
        alarm(self.time)

        try:  # here we do the hard computation
            moves = board_copy.moves(self.color)
            x = 0
            while self.time != 0:  # pretend we are doing something
                x += 1

        except IOError:  # here quickly obtain a move
            alarm(0)

        # here we return a solution very quickly
        queen, xf, yf, xb, yb = choice(moves)

        if not board_copy.is_legal_move(queen, xf, yf):
            raise Exception("Ilegal move")
        if not board_copy.is_legal_jump(queen, xf, yf, xb, yb):
            raise Exception("Ilegal jump")

        return queen, xf, yf, xb, yb
