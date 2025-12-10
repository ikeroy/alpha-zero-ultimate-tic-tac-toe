from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
try:
    from .utttLogic import Board
except:
    from utttLogic import Board
import numpy as np

class utttGame(Game):
    square_content = {
        +1: "X",
        +0: "-",
        -1: "O"
    }

    @staticmethod
    def getSquarePiece(piece):
        return utttGame.square_content[piece]

    def __init__(self):
        pass

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board()
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (10, 9)

    def getActionSize(self):
        # return number of actions
        return 9*9

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board()
        b.pieces = np.copy(board)
        move = (int(action/9), action%9)
        b.execute_move(move, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board()
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves(player)
        for x, y in legalMoves:
            valids[9*x+y]=1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board()
        b.pieces = np.copy(board)
        return b.check_board_win(player)

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board
    
    def rotate_coord(self, r, c, k):
        for _ in range(k % 4):
            r, c = c, 8 - r
        return r, c

    def getSymmetries(self, board, pi):
        # mirror, rotational
        #assert(len(pi) == 9*90)
        last_move = board[-1]
        board_body = board[:-1]
        pi_board = np.reshape(pi, (9,9))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board_body, i)
                newPi = np.rot90(pi_board, i)

                r, c = int(last_move[0]), int(last_move[1])
                r, c = self.rotate_coord(r, c, i)

                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)

                new_last = last_move.copy()
                new_last[0], new_last[1] = r, c
                full = np.vstack([newB, new_last])
                l += [(full, list(newPi.ravel()))]
    
        return l

    def stringRepresentation(self, board):
        return ''.join(map(str, board))

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s

    def getScore(self, board, player):
        b = Board()
        b.pieces = np.copy(board)
        return b.check_board_win(player)

    @staticmethod
    def display(board):
        print("-------------------------")
        for bcol in range(3):
            for scol in range(3):
                print("|", end=" ")
                for group in range(3):
                    for x in range(3):
                        print(utttGame.getSquarePiece(board[group+bcol*3][x+3*scol]), end=" ")
                    print("|", end=" ")
                print()
            print("-------------------------")
