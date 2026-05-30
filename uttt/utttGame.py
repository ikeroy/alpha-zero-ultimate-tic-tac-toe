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

    def getNNBoardSize(self):
        return (9, 9)

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
        last_group = abs(last_move[0])
        last_cell = abs(last_move[1])
        no_last_move = (last_group == 10 and last_cell == 10)

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board_body, i)
                newPi = np.rot90(pi_board, i)
                new_last = last_move.copy()
                if not no_last_move:
                    r, c = int(last_group), int(last_cell)
                    r, c = self.rotate_coord(r, c, i)
                    if j:
                        c = 8 - c
                    new_last[0] = r if last_move[0] >= 0 else -r
                    new_last[1] = c if last_move[1] >= 0 else -c

                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)

                full = np.vstack([newB, new_last])
                l += [(full, list(newPi.ravel()))]
    
        return l
    
    def encodeBoard(self, board):
        try:
            import torch
            is_torch = torch.is_tensor(board)
        except Exception:
            is_torch = False

        if is_torch:
            if board.dim() == 2:
                board = board.unsqueeze(0)
                squeeze = True
            else:
                squeeze = False

            board_body = board[:, :9, :9].contiguous().view(board.size(0), 3, 3, 3, 3)
            encoded = board_body.permute(0, 1, 3, 2, 4).contiguous().view(board.size(0), 9, 9)

            x_plane = encoded.eq(1).to(board.dtype)
            o_plane = encoded.eq(-1).to(board.dtype)
            last_plane = torch.zeros_like(encoded)

            last_group = torch.abs(board[:, 9, 0]).to(torch.long)
            last_cell = torch.abs(board[:, 9, 1]).to(torch.long)
            no_last_move = (last_group == 10) & (last_cell == 10)
            invalid = ~no_last_move & ~((last_group >= 0) & (last_group < 9) & (last_cell >= 0) & (last_cell < 9))
            if invalid.any().item():
                raise ValueError("Invalid last move values detected: {}, {}".format(last_group, last_cell))

            valid = ~no_last_move
            if valid.any().item():
                r = (last_group // 3) * 3 + (last_cell // 3)
                c = (last_group % 3) * 3 + (last_cell % 3)
                batch_idx = torch.arange(board.size(0), device=board.device)
                last_plane[batch_idx[valid], r[valid], c[valid]] = 1

            stacked = torch.stack([x_plane, o_plane, last_plane], dim=1)
            return stacked[0] if squeeze else stacked

        board = np.asarray(board)
        if board.ndim == 2:
            board = board[None, ...]
            squeeze = True
        else:
            squeeze = False

        board_body = board[:, :9, :9].reshape(board.shape[0], 3, 3, 3, 3)
        encoded = board_body.transpose(0, 1, 3, 2, 4).reshape(board.shape[0], 9, 9)

        x_plane = (encoded == 1).astype(board_body.dtype)
        o_plane = (encoded == -1).astype(board_body.dtype)
        last_plane = np.zeros_like(encoded)

        last_group = np.abs(board[:, 9, 0]).astype(int)
        last_cell = np.abs(board[:, 9, 1]).astype(int)
        no_last_move = (last_group == 10) & (last_cell == 10)
        invalid = ~no_last_move & ~((last_group >= 0) & (last_group < 9) & (last_cell >= 0) & (last_cell < 9))
        if np.any(invalid):
            raise ValueError("Invalid last move values detected: {}".format(invalid.astype(int).sum()))

        valid = ~no_last_move
        if np.any(valid):
            r = (last_group // 3) * 3 + (last_cell // 3)
            c = (last_group % 3) * 3 + (last_cell % 3)
            batch_idx = np.arange(board.shape[0])
            last_plane[batch_idx[valid], r[valid], c[valid]] = 1

        stacked = np.stack([x_plane, o_plane, last_plane], axis=1)
        return stacked[0] if squeeze else stacked

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
