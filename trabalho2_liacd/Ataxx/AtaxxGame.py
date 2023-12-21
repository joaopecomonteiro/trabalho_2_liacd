from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .AtaxxLogic import Board
import numpy as np 

class AtaxxGame(Game):
    square_content = {
        -1: "X",
        +0: "-",
        +1: "O"
    }

    @staticmethod
    def getSquarePiece(piece):
        return AtaxxGame.square_content[piece]


    def __init__(self, size):
        self.size = size

    def getInitBoard(self):
        b = Board(self.size)
        return np.array(b.matrix)

    def getBoardSize(self):
        return (self.size, self.size)

    def getActionSize(self):
        return self.size*self.size+1
    
    def getNextState(self, board, player, action):
        if action == self.size*self.size:
            return(board, -player)

        b = np.copy(board)
        b.execute_move(action, player)
        return (b, -player)

    def getValidMoves(self, board, player):
        valids = np.zeros(self.getActionSize()).astype(int)
        b = Board(self.size)
        b.matrix = np.copy(board)
        legalMoves = b.available_moves(player)

        if len(legalMoves)==0:
            valids[-1]=1
            valids
        
        for x, y in legalMoves:
            valids[self.size*x+y]=1

        return valids

    def getGameEnded(self, board, player):

        b = Board(self.size)
        b.matrix = np.copy(board)
        
        if b.is_game_over():
            if b.count_diff(player) > 0:
                return 1
            elif b.count_diff(player) <= 0:
                return -1
        
        return 0
    
    def getCanonicalForm(self, board, player):
        return player*board
    
    
    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2+1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l


    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s



    @staticmethod
    def display(board):
        n = board.shape[0]
        print("   ", end="")
        for y in range(n):
            print(y, end=" ")
        print("")
        print("-----------------------")
        for y in range(n):
            print(y, "|", end="")    # print the row #
            for x in range(n):
                piece = board[y][x]    # get the piece to print
                print(AtaxxGame.square_content[piece], end=" ")
            print("|")

        print("-----------------------")


























