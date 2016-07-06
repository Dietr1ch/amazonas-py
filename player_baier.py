import copy
import random
import signal
from board import Board

class BaierPlayer:

    def __init__(self, color, time=1):
        self.color = color
        self.time = time
        self.nevals = 0


    def play(self, main_board):

        def inverse(color):
            if color == Board.BLACK:
                return Board.WHITE
            else:
                return Board.BLACK

        def random_ply(board):
            #simulate a random play and return the color of the winner
            b = Board(board)
            c = inverse(self.color) # start with the inverse color

            while True:
                if not b.can_play(c):
                    winner = inverse(c)
                    if winner == self.color:
                        return 1
                    else:
                        return 0
                q,xf,yf,xb,yb = random.choice(b.moves(c))
                b = b.succ(q,xf,yf,xb,yb)
                c = inverse(c)

        def evaluate_children(children,evaluations):
            # evaluates each children

            while True:
                for i in range(0,len(children)):
                    evaluations[i] += random_ply(children[i])
                    self.nevals += 1
                    if self.nevals % 100==0:
                        print(self.nevals)

                if self.time == 0:
                    break

        def handler(signum, frame):
            raise IOError

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(self.time)

        try:
            self.nevals = 0
            moves=main_board.moves(self.color)

            MAX_CHILDREN=50
            if len(moves)>MAX_CHILDREN:
                print("Pruning to 20 children over",len(moves),"possible ones.")
                new_moves = []
                for i in range(0,MAX_CHILDREN):
                    new_moves.append(random.choice(moves))
                moves = new_moves

             # compute all children
            children = []
            for m in moves:
                q,xf,yf,xb,yb = m
                children.append(main_board.succ(q,xf,yf,xb,yb))


            evaluations=[0]*len(children)
            self.nevals = 0
            evaluate_children(children,evaluations)

        except IOError: ## here quickly obtain a move
            signal.alarm(0)
            print("Interrupted after",self.nevals,"evaluations")
            print("Evaluations:",evaluations)
            q,xf,yf,xb,yb = moves[evaluations.index(max(evaluations))]

        if not main_board.is_legal_move(q,xf,yf):
            raise Exception("Ilegal Move")
        if not main_board.is_legal_jump(q,xf,yf,xb,yb):
            raise Exception("Ilegal Jump")

        return q,xf,yf,xb,yb

