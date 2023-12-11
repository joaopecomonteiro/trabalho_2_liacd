import numpy as np 
import pygame 
import math
import sys 
from copy import deepcopy 
import time 
import random 
import os



SIZE = 5
WHITE = 1
BLACK = -1
SQUARE_SIZE = 75 
BLUE = (0,0,255) 
RED = (255,0,0) 
WHITE_COLOR = (255,255,255) 
BLACK_COLOR = (0,0,0) 
GREY_COLOR = (182,179,179) 
width = SIZE * SQUARE_SIZE 
height = SIZE * SQUARE_SIZE 
width = SIZE * SQUARE_SIZE 
height = SIZE * SQUARE_SIZE 
size = (width, height) 


class Board():
    def __init__(self, size):
        self.size = size
        self.board_matrix = np.zeros((size, size)).astype(int)
        self.to_move = WHITE
        self.next = BLACK

        self.board_matrix[0][0] = WHITE
        self.board_matrix[self.size-1][self.size-1] = WHITE
        self.board_matrix[0][self.size-1] = BLACK
        self.board_matrix[self.size-1][0] = BLACK  

    
    def place(self, x, y): 
        self.board_matrix[x][y] = self.to_move 


    def jump(self, x, y, new_x, new_y): 
        self.board_matrix[x][y] = 0
        self.board_matrix[new_x][new_y] = self.to_move

    
    def calc_dist(self, x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2+(y1-y2)**2)


    def play_move(self, x, y, new_x, new_y):

        if new_x < 0 or new_x >= self.size or new_y < 0 or new_y >= self.size:
            return False

        if self.board_matrix[new_x][new_y] != 0:
            return False

        dist = self.calc_dist(x, y, new_x, new_y)

        if dist == 0:
            return False
        
        elif dist < 2:
            self.place(new_x, new_y)
            return True

        elif dist < 3:
            self.jump(x, y, new_x, new_y)
            return True

        else:
            return False
    

    def is_valid_piece(self, x, y):
        if self.board_matrix[x][y] == self.to_move:
            return True
        else:
            return False

    def eat(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if x+i < board.size and x+i >=0 and y+j < board.size and y+j >=0: 
                    if self.board_matrix[x+i][y+j] == -self.to_move:
                        self.board_matrix[x+i][y+j] = self.to_move

    
    
    def get_player_pieces(self): 
        pieces = []
        for x in range(self.size):
            for y in range (self.size): 
                if self.board_matrix[x][y] == self.to_move:
                    pieces.append([x,y])
        return pieces  
        
        
    
    def available_moves(self): 
        moves = []
        for piece in self.get_player_pieces():
            x = piece[0]
            y = piece[1]
            for i in range(-3, 3):
                for j in range(-3, 3):
                    temp1_board = Board(SIZE)
                    temp1_board.board_matrix = self.board_matrix.copy()
                    if temp1_board.play_move(x, y, x+i, y+j):
                        moves.append(temp1_board.board_matrix)
        return moves 

    def is_game_over(self):
        if len(self.available_moves()) == 0:
            return True
        return False

    
    def turn(self):
        """Keep track of the turn by flipping between BLACK and WHITE."""
        if self.to_move == BLACK:
            self.to_move = WHITE
            self.next = BLACK
        else:
            self.to_move = BLACK
            self.next = WHITE




    def print_board(self):
       
        os.system('cls' if os.name == 'nt' else 'clear')

        for i in range(SIZE): #Imprimir a matriz
            line = ""
            for j in range(SIZE):
                if self.board_matrix[i][j] != -1:
                    line += " " + str(self.board_matrix[i][j]) + " "
                else:
                    line += str(self.board_matrix[i][j]) + " "

            print(line)


            
    def draw_pieces(self, screen): 
        for k in range(SIZE):
            for l in range(SIZE):
                if self.board_matrix[k][l] == WHITE: 
                    pygame.draw.circle(screen, RED, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
                elif self.board_matrix[k][l] == BLACK: 
                    pygame.draw.circle(screen, BLUE, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
                #elif self.board_matrix[k][l] == 3 or board[k][l] == 4: 
                #    pygame.draw.circle(screen, GREY_COLOR, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
                #elif self.board_matrix[k][l] == 5: 
                #    pygame.draw.line(screen, WHITE_COLOR, (l*SQUARE_SIZE,k*SQUARE_SIZE), ((l+1)*SQUARE_SIZE,(k+1)*SQUARE_SIZE), 3)
                #    pygame.draw.line(screen, WHITE_COLOR, (l*SQUARE_SIZE,(k+1)*SQUARE_SIZE), ((l+1)*SQUARE_SIZE,k*SQUARE_SIZE), 3)
                else: 
                    pygame.draw.circle(screen, BLACK_COLOR, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
        pygame.display.update() 
        
            
    def draw_lines(self, screen): 
        for i in range(SIZE -  1):
            pygame.draw.line(screen, WHITE_COLOR, ((i+1)*SQUARE_SIZE,0), ((i+1)*SQUARE_SIZE,SQUARE_SIZE*SIZE), 2) 
            pygame.draw.line(screen, WHITE_COLOR, (0,(i+1)*SQUARE_SIZE), (SQUARE_SIZE*SIZE,(i+1)*SQUARE_SIZE),2)    
        pygame.display.update() 
        
    def draw_grey_circles(self, screen, x, y):
        for i in range(-2, 3):
            for j in range(-2, 3):
                if x+i >= 0 and x+i < SIZE and y+j >= 0 and y+j < SIZE:

                    if self.board_matrix[x+i][y+j] == 0:
                        # print(f"dawd {y+i}")
                        # print(f"ddaaiowjiaw {x+j}")
                        pygame.draw.circle(screen, GREY_COLOR, (int((y+j+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((x+i+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
                        






def main():
    game_over = False
    screen = pygame.display.set_mode(size)   
    board.draw_lines(screen)
    board.draw_pieces(screen)

    clicks = 0
    while not game_over:
        #print(board.to_move)
        pygame.display.update() 
        if board.is_game_over():
            print(f"Player {-board.to_move} won !!!!")
            break






        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            


            if event.type == pygame.MOUSEBUTTONDOWN: 
                #available_moves = board.available_moves()
               # print(len(available_moves))

                if clicks == 0:
                    board.draw_pieces(screen)
                    pygame.display.update() 
                    num1 = event.pos[1] 
                    x = int(math.floor(num1/SQUARE_SIZE)) 
                    num2 = event.pos[0] 
                    y = int(math.floor(num2/SQUARE_SIZE))
                    if board.is_valid_piece(x, y): 
                        #for event in pygame.event.get():
                        board.draw_grey_circles(screen, x, y)
                        pygame.display.update() 

                        clicks = 1
                elif clicks == 1:
                    new_num1 = event.pos[1] 
                    new_x = int(math.floor(new_num1/SQUARE_SIZE)) 
                    new_num2 = event.pos[0] 
                    new_y = int(math.floor(new_num2/SQUARE_SIZE))
                    if board.play_move(x, y, new_x, new_y):
                        board.eat(new_x, new_y)
                        board.draw_pieces(screen)
                        pygame.display.update() 
                        board.turn()
                        clicks = 0
                        board.print_board()

                    else:
                        if board.is_valid_piece(new_x, new_y):
                            x = new_x
                            y = new_y
                            board.draw_pieces(screen)
                            board.draw_grey_circles(screen, x, y)
                            pygame.display.update() 
                            clicks = 0
                        else:
                            board.draw_pieces(screen)
                            pygame.display.update() 
                            




                                
        # #x, y = map(int, input("piece: ").split())
        #         if board.is_valid_piece(x, y):


                   # for event in pygame.event.get():
                   #             if event.type == pygame.QUIT:
                   #                 exit()

                                
        #             board.draw_pieces(screen)
        #             pygame.display.update

        #             if event.type == pygame.MOUSEBUTTONDOWN: 
        #                 num1 = event.pos[1] 
        #                 new_x = int(math.floor(num1/SQUARE_SIZE)) 
        #                 num2 = event.pos[0] 
        #                 new_y = int(math.floor(num2/SQUARE_SIZE))

        # #new_x, new_y = map(int, input("coords: ").split())
        #                 played_move = board.play_move(x, y, new_x, new_y)
        #                 while not played_move:
                            
                                    
        #                     if event.type == pygame.MOUSEBUTTONDOWN: 
        #                         num1 = event.pos[1] 
        #                         new_x = int(math.floor(num1/SQUARE_SIZE)) 
        #                         num2 = event.pos[0] 
        #                         new_y = int(math.floor(num2/SQUARE_SIZE))
                            
                            
        #                     #new_x, new_y = map(int, input("coords: ").split())
        #                     played_move = board.play_move(x, y, new_x, new_y)
                            
        #                 board.turn()



if __name__ == "__main__":
    pygame.init()
    board = Board(SIZE)
    main()
