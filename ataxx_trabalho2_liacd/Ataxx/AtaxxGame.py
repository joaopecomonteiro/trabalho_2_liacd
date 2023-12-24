from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .AtaxxLogic import Board
import numpy as np 
import pygame

SQUARE_SIZE = 75 #Tamanho dos quadrados da interface

PLAYER1 = 1
PLAYER2 = -1

#Cores
BLUE = (0,0,255) 
RED = (255,0,0) 
WHITE_COLOR = (255,255,255) 
BLACK_COLOR = (0,0,0) 




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
        return b.matrix

    def getBoardSize(self):
        return (self.size, self.size)

    def getActionSize(self):
        return self.size*self.size+1
    
    def getNextState(self, board, player, action):
        if action == self.size*self.size:
            return(board, -player)
        b = Board(self.size)
        b.matrix = np.copy(board)
        
        move = (int(action/self.size), action%self.size)
        
        b.execute_move(move, player)

        return (b.matrix, -player)

    def getValidMoves(self, board, player):
        valids = np.zeros(self.getActionSize()).astype(int)
        b = Board(self.size)
        b.matrix = np.copy(board)
        legalMoves = b.available_moves(player)
        if len(legalMoves)==0:
            valids[-1]=1
            valids
        
        for old_coords, new_coords in legalMoves:
            valids[self.size*new_coords[0]+new_coords[1]]=1
    
        return valids

    def getGameEnded(self, board, player):

        b = Board(self.size)
        b.matrix = np.copy(board)
        
        if b.is_game_over():
            if b.count_diff(player) > 0:
                return 1
            elif b.count_diff(player) < 0:
                return -1
            else:
                return 0
        
        return None
    
    def getCanonicalForm(self, board, player):
        return player*board
    
    
    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.size**2+1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.size, self.size))
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

    def getScore(self, board, player):
        b = Board(self.size)
        b.matrix = np.copy(board)
        return b.count_diff(player)

    def draw_lines(self, screen):
        for i in range(self.size -  1):
            pygame.draw.line(screen, WHITE_COLOR, ((i+1)*SQUARE_SIZE,0), ((i+1)*SQUARE_SIZE,SQUARE_SIZE*self.size), 2) 
            pygame.draw.line(screen, WHITE_COLOR, (0,(i+1)*SQUARE_SIZE), (SQUARE_SIZE*self.size,(i+1)*SQUARE_SIZE),2)    
        pygame.display.update() 

    def draw_pieces(self, screen, board): 
        for k in range(self.size):
            for l in range(self.size):
                if board[k][l] == PLAYER1: 
                    pygame.draw.circle(screen, RED, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
                
                elif board[k][l] == PLAYER2: 
                    pygame.draw.circle(screen, BLUE, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
                
                else: 
                    pygame.draw.circle(screen, BLACK_COLOR, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
        
        pygame.display.update() 
    

    @staticmethod
    def display(board, screen):
        size = len(board)
        for i in range(size -  1):
            pygame.draw.line(screen, WHITE_COLOR, ((i+1)*SQUARE_SIZE,0), ((i+1)*SQUARE_SIZE,SQUARE_SIZE*size), 2) 
            pygame.draw.line(screen, WHITE_COLOR, (0,(i+1)*SQUARE_SIZE), (SQUARE_SIZE*size,(i+1)*SQUARE_SIZE),2)    

        for k in range(size):
            for l in range(size):
                if board[k][l] == PLAYER1: 
                    pygame.draw.circle(screen, RED, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
                
                elif board[k][l] == PLAYER2: 
                    pygame.draw.circle(screen, BLUE, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
                
                else: 
                    pygame.draw.circle(screen, BLACK_COLOR, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
        
        pygame.display.update() 


        #self.draw_lines(screen)
        #self.draw_pieces(screen, board)

    

















