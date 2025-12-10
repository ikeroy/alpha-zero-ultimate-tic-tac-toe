from utttGame import utttGame
from utttLogic import Board
import unittest

class GetSquarePieceTest(unittest.TestCase):
    def test_x(self):
        g = utttGame()
        self.assertEqual(g.getSquarePiece(1), "X")

    def test_dash(self):
        g = utttGame()
        self.assertEqual(g.getSquarePiece(0), "-")
    
    def test_o(self):
        g = utttGame()
        self.assertEqual(g.getSquarePiece(-1), "O")

class GetNextStateTest(unittest.TestCase):
    def test1(self):
        g = utttGame()
        b = Board()
        nb, np = g.getNextState(b.pieces, 1, 0)
        self.assertTrue((nb == [[1,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]]).all())
        self.assertEqual(np,-1)

    def test2(self):
        g = utttGame()
        b = Board()
        nb, np = g.getNextState(b.pieces, 1, 80)
        self.assertTrue((nb == [[0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,1], [8,8,0,0,0,0,0,0,0]]).all())
        self.assertEqual(np,-1)

class GetGameEndedTest(unittest.TestCase):
    def test_get_game_ended1(self):
        b = Board()
        g = utttGame()
        b.execute_move((0,0),1)
        b.execute_move((0,1),1)
        b.execute_move((0,2),1)
        b.execute_move((1,0),1)
        b.execute_move((1,1),1)
        b.execute_move((1,2),1)
        b.execute_move((2,0),1)
        b.execute_move((2,1),1)
        b.execute_move((2,2),1)
        self.assertEqual(g.getGameEnded(b.pieces, 1),1)

    def test_get_game_ended2(self):
        b = Board()
        g = utttGame()
        b.execute_move((0,0),1)
        b.execute_move((0,1),1)
        b.execute_move((0,2),1)
        b.execute_move((1,0),1)
        b.execute_move((1,1),1)
        b.execute_move((1,2),1)
        b.execute_move((2,0),1)
        b.execute_move((2,1),1)
        b.execute_move((2,2),1)
        self.assertEqual(g.getGameEnded(b.pieces, -1),-1)