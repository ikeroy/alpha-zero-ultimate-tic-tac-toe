from utttLogic import Board
import unittest

class BoardTest(unittest.TestCase):
    def test_init(self):
        b = Board()
        self.assertEqual(b.pieces, [[0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [10,10,0,0,0,0,0,0,0]])

class LegalMovesTest(unittest.TestCase):
    def test_init_error(self):
        b = Board()
        b.pieces = [[1,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [10,10,0,0,0,0,0,0,0]]
        self.assertEqual(b.has_legal_moves(), False)

    def test_init_error_moves(self):
        b = Board()
        b.pieces = [[1,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [10,10,0,0,0,0,0,0,0]]
        self.assertSetEqual(b.get_legal_moves(), set())

    def test_empty(self):
        b = Board()
        self.assertEqual(b.has_legal_moves(), True)

    def test_empty_moves(self):
        b = Board()
        x = set()
        for a in range(9):
            for y in range(9):
                x.add((a,y))
        self.assertSetEqual(b.get_legal_moves(), x)

    def test_captured_group(self):
        b = Board()
        b.pieces = [[1,1,1,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]]
        x = set()
        for a in range(1,9):
            for y in range(9):
                x.add((a,y))
        self.assertSetEqual(b.get_legal_moves(), x)
    
    def test1(self):
        b = Board()
        b.pieces = [[0,0,-1,0,0,-1,0,-1,-1],[-1,-1,-1,1,0,1,0,-1,-1],[1,0,0,1,0,1,1,0,0],[-1,-1,0,-1,0,0,1,0,0],[1,1,-1,0,1,0,0,0,0],[1,0,-1,0,-1,0,0,0,0],[0,0,0,0,-1,0,-1,-1,1],[1,1,-1,0,-1,0,1,-1,0],[0,1,-1,1,0,0,0,1,0],[8,2,0,0,0,0,0,0,0]]
        self.assertSetEqual(set(((3,2),(3,4),(3,5),(3,7),(3,8),(4,3),(4,5),(4,6),(4,7),(4,8),(5,1),(5,3),(5,5),(5,6),(5,7),(5,8),(6,0),(6,1),(6,2),(6,3),(6,5),(7,3),(7,5),(7,8),(8,0),(8,4),(8,5),(8,6),(8,8))), b.get_legal_moves())

    def test_to_captured_group(self):
        b = Board()
        b.pieces = [[1,1,1,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1], [0,0,0,0,0,0,0,0,0]]
        self.assertSetEqual(b.get_legal_moves(), set(((1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8))))

    def test_none(self):
        b = Board()
        b.pieces = [[-1,-1,1,1,1,-1,1,1,0],[1,1,1,-1,0,1,1,-1,-1],[0,1,0,0,-1,-1,-1,-1,-1],[-1,-1,-1,0,1,0,0,1,0],[0,0,-1,0,1,-1,0,0,-1],[1,1,1,0,0,1,-1,-1,1],[1,-1,1,-1,1,-1,1,-1,-1],[-1,-1,0,0,-1,-1,1,1,-1],[0,0,1,1,1,0,1,1,-1],[0,0,0,0,0,0,0,0,0]]
        self.assertEqual(b.check_board_win(), 1)
        
class ExecuteMoveTest(unittest.TestCase):
    def test_execute_move(self):
        b = Board()
        b.execute_move((1,1), 1)
        self.assertListEqual(b.pieces, [[0,0,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [1,1,0,0,0,0,0,0,0]])

class CheckGroupWinTest(unittest.TestCase):
    def test_horizontal1(self):
        b = Board()
        b.execute_move((0,0),1)
        b.execute_move((0,1),1)
        b.execute_move((0,2),1)
        self.assertEqual(b.check_group_win(b.pieces[0]), 1)

    def test_horizontal2(self):
        b = Board()
        b.execute_move((0,3),1)
        b.execute_move((0,4),1)
        b.execute_move((0,5),1)
        self.assertEqual(b.check_group_win(b.pieces[0]), 1)

    def test_horizontal3(self):
        b = Board()
        b.execute_move((0,6),1)
        b.execute_move((0,7),1)
        b.execute_move((0,8),1)
        self.assertEqual(b.check_group_win(b.pieces[0]), 1)
    
    def test_horizontal4(self):
        b = Board()
        b.execute_move((0,0),-1)
        b.execute_move((0,1),-1)
        b.execute_move((0,2),-1)
        self.assertEqual(b.check_group_win(b.pieces[0]), -1)

    def test_horizontal5(self):
        b = Board()
        b.execute_move((0,3),-1)
        b.execute_move((0,4),-1)
        b.execute_move((0,5),-1)
        self.assertEqual(b.check_group_win(b.pieces[0]), -1)

    def test_horizontal6(self):
        b = Board()
        b.execute_move((0,6),-1)
        b.execute_move((0,7),-1)
        b.execute_move((0,8),-1)
        self.assertEqual(b.check_group_win(b.pieces[0]), -1)

    def test_vertical1(self):
        b = Board()
        b.execute_move((0,0),1)
        b.execute_move((0,3),1)
        b.execute_move((0,6),1)
        self.assertEqual(b.check_group_win(b.pieces[0]), 1)

    def test_vertical2(self):
        b = Board()
        b.execute_move((0,1),1)
        b.execute_move((0,4),1)
        b.execute_move((0,7),1)
        self.assertEqual(b.check_group_win(b.pieces[0]), 1)

    def test_vertical3(self):
        b = Board()
        b.execute_move((0,2),1)
        b.execute_move((0,5),1)
        b.execute_move((0,8),1)
        self.assertEqual(b.check_group_win(b.pieces[0]), 1)

    def test_vertical4(self):
        b = Board()
        b.execute_move((0,0),-1)
        b.execute_move((0,3),-1)
        b.execute_move((0,6),-1)
        self.assertEqual(b.check_group_win(b.pieces[0]), -1)

    def test_vertical5(self):
        b = Board()
        b.execute_move((0,1),-1)
        b.execute_move((0,4),-1)
        b.execute_move((0,7),-1)
        self.assertEqual(b.check_group_win(b.pieces[0]), -1)

    def test_vertical6(self):
        b = Board()
        b.execute_move((0,2),-1)
        b.execute_move((0,5),-1)
        b.execute_move((0,8),-1)
        self.assertEqual(b.check_group_win(b.pieces[0]), -1)

    def test_diagonal1(self):
        b = Board()
        b.execute_move((0,0),1)
        b.execute_move((0,4),1)
        b.execute_move((0,8),1)
        self.assertEqual(b.check_group_win(b.pieces[0]), 1)

    def test_diagonal2(self):
        b = Board()
        b.execute_move((0,2),1)
        b.execute_move((0,4),1)
        b.execute_move((0,6),1)
        self.assertEqual(b.check_group_win(b.pieces[0]), 1)

    def test_diagonal3(self):
        b = Board()
        b.execute_move((0,0),-1)
        b.execute_move((0,4),-1)
        b.execute_move((0,8),-1)
        self.assertEqual(b.check_group_win(b.pieces[0]), -1)

    def test_diagonal4(self):
        b = Board()
        b.execute_move((0,2),-1)
        b.execute_move((0,4),-1)
        b.execute_move((0,6),-1)
        self.assertEqual(b.check_group_win(b.pieces[0]), -1)

class CheckBoardWinTest(unittest.TestCase):
    def test_check_board_win1(self):
        b = Board()
        b.execute_move((0,0),1)
        b.execute_move((0,1),1)
        b.execute_move((0,2),1)
        b.execute_move((1,0),1)
        b.execute_move((1,1),1)
        b.execute_move((1,2),1)
        b.execute_move((2,0),1)
        b.execute_move((2,1),1)
        b.execute_move((2,2),1)
        self.assertEqual(b.check_board_win(1),1)

    def test_check_board_win2(self):
        b = Board()
        b.execute_move((0,0),1)
        b.execute_move((0,1),1)
        b.execute_move((0,2),1)
        b.execute_move((1,0),1)
        b.execute_move((1,1),1)
        b.execute_move((1,2),1)
        b.execute_move((2,0),1)
        b.execute_move((2,1),1)
        b.execute_move((2,2),1)
        self.assertEqual(b.check_board_win(-1),-1)