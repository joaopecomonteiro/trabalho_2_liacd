import numpy as np
import os
import time
import pygame
import math

SIZE = 7
WHITE = 1
BLACK = 2
BACKGROUND_COLOR = (240, 196, 52)
#BLUE = (0,0,255) 
#RED = (255,0,0) 
WHITE_COLOR = (255,255,255) 
BLACK_COLOR = (0,0,0) 
SQUARE_SIZE = 75
width = SIZE * SQUARE_SIZE 
height = SIZE * SQUARE_SIZE 
size = (width, height) 


class Board():
    def __init__(self, size):
        self.x_dim = size
        self.y_dim = size
        self.board_matrix = np.zeros((size, size)).astype(int)
        self.groups = []
        self.to_move = BLACK
        self.next = WHITE
    
    def valid_move(self, pos1, pos2):
        pos_count = 0
        open_count = 0

        if self.board_matrix[pos1][pos2] != 0:
            return False
        
        #print(f"{pos1-1}, {pos2} - {self.board_matrix[pos1-1][pos2]}")
        #print(f"{pos1}, {pos2+1} - {self.board_matrix[pos1][pos2+1]}")
        #print(f"{pos1+1}, {pos2} - {self.board_matrix[pos1+1][pos2]}")
        #print(f"{pos1}, {pos2-1} - {self.board_matrix[pos1][pos2-1]}")
        
        if pos1-1>=0:
            pos_count += 1
            if self.board_matrix[pos1-1][pos2] != self.next:
                open_count += 1
                
        if pos2-1>=0:
            pos_count += 1
            if self.board_matrix[pos1][pos2-1] != self.next:

                open_count += 1
                 
        if pos1+1<SIZE:
            pos_count += 1
            if self.board_matrix[pos1+1][pos2] != self.next:

                open_count += 1
        
        if pos2+1<SIZE:
            pos_count += 1
            if self.board_matrix[pos1][pos2+1] != self.next:

                open_count += 1

        #print(open_count)

        if open_count > 0:
            return True
        else:
            return False

    def play_move(self, pos1, pos2):

        if self.valid_move(pos1, pos2):

            self.board_matrix[pos1][pos2] = self.to_move


    def update_liberties(self, added_stone=None):
        """Updates the liberties of the entire board, group by group.

        Usually a stone is added each turn. To allow killing by 'suicide',
        all the 'old' groups should be updated before the newly added one.

        """
        for group in self.groups:
            if added_stone:
                if group == added_stone.group:
                    continue
            group.update_liberties()
        if added_stone:
            added_stone.group.update_liberties()




    def search(self, position=None, positions=[]):
        """Search the board for a stone.

        The board is searched in a linear fashion, looking for either a
        stone in a single point (which the method will immediately
        return if found) or all stones within a group of points.

        Arguments:
        point -- a single point (tuple) to look for
        points -- a list of points to be searched

        """
        stones = []
        for group in self.groups:
            for stone in group.stones:
                if stone.position == position and not positions:
                    return stone
                if stone.position in positions:
                    stones.append(stone)
        return stones
    

    def update_board(self):
        self.board_matrix = np.zeros((SIZE, SIZE)).astype(int)

        for group in self.groups:
            for stone in group.stones:
                self.board_matrix[stone.position[0]][stone.position[1]] = stone.color



    def turn(self):
        """Keep track of the turn by flipping between BLACK and WHITE."""
        if self.to_move == BLACK:
            self.to_move = WHITE
            self.next = BLACK
        else:
            self.to_move = BLACK
            self.next = WHITE


    def print_board(self):
        matrix = np.zeros((SIZE, SIZE)).astype(int)

        for group in self.groups:
            for stone in group.stones:
                matrix[stone.position[0]][stone.position[1]] = stone.color
        #time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')

        for i in range(SIZE): #Imprimir a matriz
            line = ""
            for j in range(SIZE):
                line += str(self.board_matrix[i][j]) + " "

            print(line)
        

class Stone():
    def __init__(self, board, position, color):
        """
        Create and initialize a stone.

        Arguments:
        board -- the board which the stone resides on
        position -- location of the stone as a tuple, e.g. (3, 3)
                 represents the upper left hoshi
        color -- color of the stone
        """

        self.board = board
        self.position = position
        self.color = color
        self.group = self.find_group()


    def remove(self):
        """Remove the stone from board."""
        self.group.stones.remove(self)
        del self


    @property
    def neighbors(self):
        """Return a list of neighboring points."""

        neighboring = [(self.position[0] - 1, self.position[1]),
                       (self.position[0] + 1, self.position[1]),
                       (self.position[0], self.position[1] - 1),
                       (self.position[0], self.position[1] + 1)]
        neighbours = []
        for position in neighboring:
            if not (position[0] < 0 or  position[0] >= SIZE or position[1] < 0 or position[1] >= SIZE):
                neighbours.append(position)

        return neighbours


    @property
    def liberties(self):
        """Find and return the liberties of the stone."""
        liberties = self.neighbors
        stones = self.board.search(positions=self.neighbors)
        for stone in stones:
            liberties.remove(stone.position)
        return liberties


    def find_group(self):
        """Find or create a group for the stone."""
        groups = []
        stones = self.board.search(positions=self.neighbors)
        for stone in stones:
            if stone.color == self.color and stone.group not in groups:
                groups.append(stone.group)
        if not groups:
            group = Group(self.board, self)
            return group
        else:
            if len(groups) > 1:
                for group in groups[1:]:
                    groups[0].merge(group)
            groups[0].stones.append(self)
            return groups[0]



class Group(object):
    def __init__(self, board, stone):
        """Create and initialize a new group.

        Arguments:
        board -- the board which this group resides in
        stone -- the initial stone in the group

        """
        self.board = board
        self.board.groups.append(self)
        self.stones = [stone]
        self.liberties = None


    def merge(self, group):
        """Merge two groups.

        This method merges the argument group with this one by adding
        all its stones into this one. After that it removes the group
        from the board.

        Arguments:
        group -- the group to be merged with this one

        """
        for stone in group.stones:
            stone.group = self
            self.stones.append(stone)
        self.board.groups.remove(group)
        del group



    def remove(self):
        """Remove the entire group."""
        while self.stones:
            self.stones[0].remove()
        self.board.groups.remove(self)
        del self


    def update_liberties(self):
        """Update the group's liberties.

        As this method will remove the entire group if no liberties can
        be found, it should only be called once per turn.

        """
        liberties = []
        for stone in self.stones:
            for liberty in stone.liberties:
                liberties.append(liberty)
        self.liberties = set(liberties)
        if len(self.liberties) == 0:
            self.remove()

       
def draw_pieces(board): 
    for k in range(SIZE):
        for l in range(SIZE):
            if board[k][l] == 1: 
                pygame.draw.circle(screen, WHITE_COLOR, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
            elif board[k][l] == 2: 
                pygame.draw.circle(screen, BLACK_COLOR, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
            else: 
                pygame.draw.circle(screen, BACKGROUND_COLOR, (int((l+1)*SQUARE_SIZE - SQUARE_SIZE/2),int((k+1)*SQUARE_SIZE - SQUARE_SIZE/2)), SQUARE_SIZE/3)
    pygame.display.update() 
     
        
def draw_lines(board): 
    for i in range(SIZE -  1):
        pygame.draw.line(screen, BLACK_COLOR, ((i+1)*SQUARE_SIZE,0), ((i+1)*SQUARE_SIZE,SQUARE_SIZE*SIZE), 2) 
        pygame.draw.line(screen, BLACK_COLOR, (0,(i+1)*SQUARE_SIZE), (SQUARE_SIZE*SIZE,(i+1)*SQUARE_SIZE),2)    
    pygame.display.update() 




def main():
    board.print_board()

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
                if board.valid_move(pos1, pos2):
                    new_stone = Stone(board, (pos1, pos2), board.to_move)
                    #board.play_move(num1, num2)
                    board.update_liberties(new_stone)
                    board.update_board()
                    draw_pieces(board.board_matrix)
                    board.print_board()
                    board.turn()

        """
        num1, num2 = map(int, input("pos1, pos2: ").split())
        #print(board.valid_move(num1, num2))
        if board.valid_move(num1, num2):
            new_stone = Stone(board, (num1, num2), board.to_move)
            #board.play_move(num1, num2)
            board.update_liberties(new_stone)
            board.update_board()
            board.print_board()
        
            print(new_stone.neighbors)

            for neighbor in new_stone.neighbors:
                print(board.board_matrix[neighbor[0]][neighbor[1]])


            print()

            for group in board.groups:
                line = ""
                for stone in group.stones:
                    line += str(stone.position) + ": " + str(stone.color) + " | "
                print(line)
        """

            #print(new_stone.position)
        #else:
         #   print("invalid move")



if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(size) 
    #screen.blit(BACKGROUND_COLOR, (0, 0))
    screen.fill(BACKGROUND_COLOR)
    #board = Board(SIZE)
    #board.play_move(6, 6)
    #print(board.board_matrix)
    board = Board(SIZE)
    draw_lines(board.board_matrix) 
    draw_pieces(board.board_matrix) 
    main()













