import numpy as np
import subprocess

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanUtttPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        for i in range(len(valid)):
            if valid[i]:
                print("[", int(i/9), int(i%9), end="] ")
        while True:
            input_move = input()
            input_a = input_move.split(" ")
            if len(input_a) == 2:
                try:
                    x,y = [int(i) for i in input_a]
                    if ((0 <= x) and (x < 9) and (0 <= y) and (y < 9)):
                        a = 9 * x + y if x != -1 else 9 ** 2
                        if valid[a]:
                            break
                except ValueError:
                    # Input needs to be an integer
                    'Invalid integer'
            print('Invalid move')
        return a


class GreedyUtttPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        candidates = []
        for a in range(self.game.getActionSize()):
            if valids[a]==0:
                continue
            nextBoard, _ = self.game.getNextState(board, 1, a)
            score = self.game.getScore(nextBoard, 1)
            candidates += [(-score, a)]
        candidates.sort()
        return candidates[0][1]
