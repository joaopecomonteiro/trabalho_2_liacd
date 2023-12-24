import numpy as np
import math

PLAYER1 = 1
PLAYER2 = -1

class Board():
    """
    Classe do jogo ataxx

    Argumentos:
                size -> tamanho do tabuleiro

    """
    def __init__(self, size):
        """
        size -> tamanho do tabuleiro
        board_matrix -> matrix que representa o estado do tabuleiro
        to_move -> jogador 
        
        
        """
        self.size = size
        self.matrix = np.zeros((self.size, self.size)).astype(int)

        self.matrix[0][0] = PLAYER1
        self.matrix[self.size-1][self.size-1] = PLAYER1
        self.matrix[0][self.size-1] = PLAYER2
        self.matrix[self.size-1][0] = PLAYER2  


    def __getitem__(self, index): 
        return self.matrix[index]


    
    def place(self, x, y, player): 
        self[x][y] = player


    
    def jump(self, x, y, new_x, new_y, player): 
        self[x][y] = 0
        self[new_x][new_y] = player

        
    def calc_dist(self, x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2+(y1-y2)**2)



    def execute_move(self, action, player):
        #action = ((0,0), (0, 0))
        if type(action[0]) is int:

            new_x, new_y = action
            valid_moves = self.available_moves(player)
            x, y = 0, 0
            shortest_dist = np.inf
            for old_coords, new_coords in valid_moves:
                if new_coords == action:
                    dist = self.calc_dist(old_coords[0], old_coords[1], new_coords[0], new_coords[1])
                    if dist < shortest_dist:

                        x = old_coords[0]
                        y = old_coords[1]
                        shortest_dist = dist
        
        #print(x, y, new_x, new_y)
        else:
            x, y, new_x, new_y = action

        if new_x < 0 or new_x >= self.size or new_y < 0 or new_y >= self.size:
            return False

        if self[new_x][new_y] != 0:
            return False

        dist = self.calc_dist(x, y, new_x, new_y)

        if dist == 0:
            return False
        
        elif dist < 2:
            self.place(new_x, new_y, player)
            self.eat(new_x, new_y, player)
            return True

        elif dist < 3:
            self.jump(x, y, new_x, new_y, player)
            self.eat(new_x, new_y, player)
            return True

        else:
            return False
    

    def is_valid_piece(self, x, y, player):
        if self[x][y] == player:
            return True
        else:
            return False

    
    def eat(self, x, y, player):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if x+i < self.size and x+i >=0 and y+j < self.size and y+j >=0: 
                    if self[x+i][y+j] == -player:
                        self[x+i][y+j] = player
    
    
    def get_player_pieces(self, player): 
        pieces = []
        for x in range(self.size):
            for y in range (self.size): 
                if self[x][y] == player:
                    pieces.append([x,y])
        return pieces  
    
    
        
    def available_moves(self, player):
        moves = []
        for piece in self.get_player_pieces(player):
            x = piece[0]
            y = piece[1]
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if x+i < self.size and x+i >=0 and y+j < self.size and y+j >=0: 
                        if self[x+i][y+j] == 0:
                            moves.append(((x, y) ,(x+i, y+j)))
                        
                    #temp1_board = Board(self.size)
                    #temp1_board.matrix = self.matrix.copy()
                    #if temp1_board.execute_move((x, y, x+i, y+j), player):
        return moves 

    
    def is_game_over(self):
        if len(self.available_moves(PLAYER1)) == 0 or len(self.available_moves(PLAYER2)) == 0:
            return True
        return False
    
    
    def piece_counter(self):
        player_1_counter = len(self.get_player_pieces(PLAYER1))
        player_2_counter = len(self.get_player_pieces(PLAYER2))
        return player_1_counter, player_2_counter
    


    def count_diff(self, player):
        count = 0
        for y in range(self.size):
            for x in range(self.size):
                if self[x][y] == player:
                    count += 1
                elif self[x][y] == -player:
                    count -= 1
        return count


