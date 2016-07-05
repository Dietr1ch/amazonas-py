"""
Amazonas Board Module
"""
import copy


class Board:
    """
    Amazonas Board
    """

    BLANK = '--'
    WHITE = 'W'
    BLACK = 'B'
    BLOCKED = 'XX'

    def __init__(self,init_board=None):
        # create an initial board
        if init_board==None:
            self.board=[]
            for _ in range(10):
                self.board.append([Board.BLANK]*10)
            self.queens = [[3,0],[0,3],[0,6],[3,9],[6,0],[9,3],[9,6],[6,9]]
            num=0
            for q in self.queens:
                if num < 4:
                    ch = Board.BLACK
                else:
                    ch = Board.WHITE
                self.board[q[0]][q[1]] = ch+str(num%4)
                num += 1
        else:
            self.board  = copy.deepcopy(init_board.board)
            self.queens = copy.deepcopy(init_board.queens)

    def __repr__(self):
        s = "   "+"  ".join([str(i) for i in range(10)])+"\n"
        for i in range(10):
            s += str(i)+" "+" ".join(self.board[i]) + "\n"
        return s

    def __eq__(self, other):
        return isinstance(other, Board) and other.__repr__() == self.__repr__()

    def __hash__(self):
        return hash(self.board.__repr__())

    def succ(self,queen,xf,yf,xb,yb):
         # returns a new board like self but with queen moved to xf,yf and position xb,yb blocked
        bsucc=Board(self)
        xi=self.queens[queen][0]
        yi=self.queens[queen][1]
        bsucc.queens[queen][0] = xf
        bsucc.queens[queen][1] = yf
        bsucc.board[xf][yf] = bsucc.board[xi][yi]
        bsucc.board[xi][yi] = Board.BLANK
        bsucc.board[xb][yb] = Board.BLOCKED
        return bsucc

    def queen2str(q):
        if q<4:
            return Board.BLACK+str(q)
        return Board.WHITE+str(q%4)

    def show_move(color,q,xf,yf,xb,yb):
        print("Jugador",color,"mueve reina",q%4,"hasta","("+str(xf)+","+str(yf)+")","bloqueando","("+str(xb)+","+str(yb)+")"+"\n")

    def is_legal_jump(self, q,xi,yi,xf,yf):
        q_str = Board.queen2str(q)
        dx = xf - xi
        dy = yf - yi
        if dx == dy == 0 or (abs(dx)!=abs(dy) and abs(dx)!=0 and abs(dy)!=0):
            return False
        if dx!=0:
            dx //= abs(dx)
        if dy!=0:
            dy //= abs(dy)
        x = xi + dx
        y = yi + dy
        while True:
            if self.board[x][y] != Board.BLANK and self.board[x][y] != q_str:
                return False
            if (x,y) == (xf,yf):
                break
            x += dx
            y += dy

        return True

    def is_legal_move(self,queen,xf,yf):
        """
        true iff queen queen can move to xf to yf
        """
        xi=self.queens[queen][0]
        yi=self.queens[queen][1]
        return self.is_legal_jump(queen,xi,yi,xf,yf)

    def can_play(self, color):
        return self.moves(color, 1)!=[]

    def moves(self, color, limit=100000):
        n = 0
        if color==Board.BLACK:
            queens = range(4)
        else:
            queens = range(4,8)
        moves = []

        for q in queens:
            queen_str=color+str(q%4)
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if dx==dy==0:
                        continue
                    xf=self.queens[q][0]+dx
                    yf=self.queens[q][1]+dy
                    while 0<=xf<10 and 0<=yf<10:
                        if self.board[xf][yf] != Board.BLANK:
                            break
                        for ddx in [-1,0,1]:
                            for ddy in [-1,0,1]:
                                if ddx==ddy==0:
                                    continue
                                xb=xf+ddx
                                yb=yf+ddy
                                while 0<=xb<10 and 0<=yb<10:
                                    if self.board[xb][yb] != Board.BLANK and self.board[xb][yb] != queen_str:
                                        break
                                    moves.append((q,xf,yf,xb,yb))
                                    n += 1
                                    if n == limit:
                                        return moves
                                    xb += ddx
                                    yb += ddy
                        xf += dx
                        yf += dy
        return moves