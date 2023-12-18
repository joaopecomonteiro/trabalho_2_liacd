#from __future__ import print_function

import pygame
from go_logic import Board
import numpy as np
import math

SIZE = 7
WHITE = -1
BLACK = +1
PASS_MOVE = (100, 100)

BACKGROUND_COLOR = (240, 196, 52)
#BLUE = (0,0,255) 
#RED = (255,0,0) 
WHITE_COLOR = (255,255,255) 
BLACK_COLOR = (0,0,0) 
SQUARE_SIZE = 75
width = SIZE * SQUARE_SIZE 
height = SIZE * SQUARE_SIZE 
size = (width, height) 

class GoGame():
    def __init__(self, size):
        self.n = size

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return b

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n * self.n + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        # print("getting next state from perspect of player {} with action {}".format(player,action))
        
        b = board.copy()
        if action == self.n * self.n:
            return (b, -player)

        #move = (int(action / self.n), action % self.n)
        # display(b)
        # print(player,move)
        if not b.execute_move(action,player):
            print("pldplawd")
            return (board, player)
        # display(b)
        return (b, -player)

    # modified
    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0 for i in range(self.getActionSize())]
        b = board.copy()
        legalMoves = b.get_legal_moves(player)
        # display(board)
        # print("legal moves{}".format(legalMoves))
        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n * x + y] = 1
        # display(b)
        # print(legalMoves)
        return np.array(valids)

    # modified
    def getGameEnded(self, board, player,returnScore=False):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1

        winner = 0
        (score_black, score_white) = self.getScore(board)
        by_score = 0.5 * (board.n*board.n + board.komi)

        if len(board.history) > 1:
            if (board.history[-1] is None and board.history[-2] is None\
                    and player == -1):
                if score_black > score_white:
                    winner = -1
                elif score_white > score_black:
                    winner = 1
                else:
                    # Tie
                    winner = 1e-4
            elif score_black > by_score or score_white > by_score:
                if score_black > score_white:
                    winner = -1
                elif score_white > score_black:
                    winner = 1
                else:
                    # Tie
                    winner = 1e-4
        if returnScore:
            return winner,(score_black, score_white)
        return winner

    def getScore(self, board):
        score_white = np.sum(board.pieces == -1)
        score_black = np.sum(board.pieces == 1)
        empties = zip(*np.where(board.pieces == 0))
        for empty in empties:
            # Check that all surrounding points are of one color
            if board.is_eyeish(empty, 1):
                score_black += 1
            elif board.is_eyeish(empty, -1):
                score_white += 1
        score_white += board.komi
        score_white -= board.passes_white
        score_black -= board.passes_black
        return (score_black, score_white)

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        canonicalBoard=board.copy()

        canonicalBoard.pieces= board.pieces* player

        # print('getting canon:')
        # print(b_pieces)
        return canonicalBoard

    # modified
    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2 + 1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []
        b_pieces = board.pieces
        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(b_pieces, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return np.array(board.pieces).tostring()


        
    def draw_pieces(self,board): 
        for k in range(SIZE):
            for l in range(SIZE):
                if board[k][l] == -1: 
                    pygame.draw.circle(screen, WHITE_COLOR, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
                elif board[k][l] == 1: 
                    pygame.draw.circle(screen, BLACK_COLOR, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
                else: 
                    pygame.draw.circle(screen, BACKGROUND_COLOR, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
        pygame.display.update() 
        
            
    def draw_lines(self): 
        for i in range(SIZE -  1):
            pygame.draw.line(screen, BLACK_COLOR, ((i+1)*SQUARE_SIZE,0), ((i+1)*SQUARE_SIZE,SQUARE_SIZE*SIZE), 2) 
            pygame.draw.line(screen, BLACK_COLOR, (0,(i+1)*SQUARE_SIZE), (SQUARE_SIZE*SIZE,(i+1)*SQUARE_SIZE),2)    
        pygame.display.update() 


def display(board):
    b_pieces = np.array(board.pieces)

    n = b_pieces.shape[0]

    for y in range(n):
        print(y, "|", end="")
    print("")
    print(" -----------------------")
    for y in range(n):
        print(y, "|", end="")    # print the row #
        for x in range(n):
            piece = b_pieces[y][x]    # get the piece to print
            if piece == 1:
                print("b ", end="")
            elif piece == -1:
                print("W ", end="")
            else:
                if x == n:
                    print("-", end="")
                else:
                    print("- ", end="")
        print("|")

    print("   -----------------------")



def main():
    board = game.getInitBoard()
    game.draw_lines() 
    to_move = BLACK
    #display(game.getInitBoard())    
    while True:
        pygame.display.update() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN: 
                num1 = event.pos[1] 
                pos1 = int(math.floor(num1/SQUARE_SIZE)) 
                num2 = event.pos[0] 
                pos2 = int(math.floor(num2/SQUARE_SIZE)) 
                #print(f"({pos1}, {pos2})")
                action = (pos1, pos2)
                #a = int(action / 7)
                #print(a)
                #b = action % 7
                #move = (int(action / 7), action % 7)
                board, to_move = game.getNextState(board, to_move, action)
                
                #print(board, to_move)
                game.draw_pieces(board) 
                print(game.getGameEnded(board, to_move))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    action = PASS_MOVE
                    print(to_move)
                    board, to_move = game.getNextState(board, to_move, action)
                    print(to_move)
                    #print(game.getGameEnded(board, to_move))
                    

if __name__ == "__main__":
    #pygame.init()
    screen = pygame.display.set_mode(size) 
    game = GoGame(SIZE)
    screen.fill(BACKGROUND_COLOR)
    main()