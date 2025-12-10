import logging
log = logging.getLogger(__name__)
'''
Author: Eric P. Nichols
Date: Feb 8, 2008.
Board class.
Board data:
  1=white, -1=black, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
'''
class Board():
    def __init__(self):
        "Set up initial board configuration."
    
        self.pieces = []
        for _ in range(9):
            self.pieces.append([0]*9)
        
        self.pieces.append([10, 10, 0, 0, 0, 0, 0, 0, 0])

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def get_legal_moves(self, color=None):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        """
        moves = set()  # stores the legal moves.

        # Get all the squares with pieces of the given color.
        if abs(self.pieces[9][0]) == 10:
            for gIdx, group in enumerate(self.pieces[0:9]):
                for pIdx, piece in enumerate(group):
                    if piece == 0:
                        moves.add((gIdx, pIdx))
                    else:
                        log.error("Pieces found with init conditions")
                        return set()
            return moves
        
        if self.check_group_win(self.pieces[abs(self.pieces[9][1])]):
            for gIdx, group in enumerate(self.pieces[0:9]):
                for pIdx, piece in enumerate(group):
                    if not self.check_group_win(self.pieces[gIdx]) and self.pieces[gIdx][pIdx] == 0:
                        moves.add((gIdx, pIdx))
            return moves

        for pIdx, piece in enumerate(self.pieces[abs(self.pieces[9][1])]):
            if piece == 0:
                moves.add((abs(self.pieces[9][1]), pIdx))
        
        return moves


    def has_legal_moves(self):
        return len(self.get_legal_moves()) > 0

    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """

        #Much like move generation, start at the new piece's square and
        #follow it on all 8 directions to look for a piece allowing flipping.

        # Add the piece to the empty square.
        # print(move)
        self.pieces[move[0]][move[1]] = color
        self.pieces[9][0] = move[0]
        self.pieces[9][1] = move[1]

    def check_group_win(self, group):
        win_conditions = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        if any([all([group[win_condition[x]] == 1 for x in range(3)]) for win_condition in win_conditions]):
            return 1
        if any([all([group[win_condition[x]] == -1 for x in range(3)]) for win_condition in win_conditions]):
            return -1
        return 0

    def check_board_win(self, color = 1):
        win = self.check_group_win([self.check_group_win(group) for group in self.pieces[0:9]])
        if win != 0:
            return color*win
        if len(self.get_legal_moves()) == 0:
            win = sum([self.check_group_win(group) for group in self.pieces[0:9]])
            if win == 0:
                return 1
            if win > 0:
                return 1
            return -1
        return 0