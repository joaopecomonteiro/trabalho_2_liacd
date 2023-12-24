from Ataxx.tensorflow.NNet import NNetWrapper as nn
from MCTS import MCTS
from utils import *


import numpy as np
import time
import pygame
import sys
import math

SQUARE_SIZE = 75


class GreedyPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        time.sleep(2)
        valids = self.game.getValidMoves(board, 1)
        candidates = []
        for a in range(self.game.getActionSize()):
            if valids[a]==1:
                next_board, _ = self.game.getNextState(board, 1, a)
                score = self.game.getScore(next_board, 1)
                candidates.append((-score, a))
        candidates.sort()
        return candidates[0][1]




class AlphaBeta():
    def __init__(self, game):
        self.game = game
        self.candidates = {}
        self.s = ""

    def alpha_beta(self, board, player, depth, alpha, beta, max_player, prev_action=None):
        #print("board")
        #print(board)
        #print(f"player -> {player}")
        if depth == 2:
            self.s = self.game.stringRepresentationReadable(board)
            self.candidates[self.s] = 0
            

        if depth == 0 or self.game.getGameEnded(board, player):
            #print(self.game.getScore(board, player))
            #print(board)
            #s = self.game.stringRepresentationReadable(board)
            self.candidates[self.s] = self.game.getScore(board, player)
            return self.game.getScore(board, player), board

        if max_player:
            max_eval = -np.inf
            best_action = None
            #print(self.game.getValidMoves(board, player))
            valids = self.game.getValidMoves(board, player)

            for action in range(self.game.getActionSize()):
                if valids[action]==1:
                    #print(f"action -> {action}")
                    next_board, _ = self.game.getNextState(board, player, action)
                    #print("next_board max")
                    #print(next_board)
                    evaluation =  self.alpha_beta(next_board, -player, depth-1, alpha, beta, False)[0]
                    max_eval = max(max_eval, evaluation)
                    if max_eval == evaluation:
                        best_action = action
                    alpha = max(alpha, max_eval)
                    if alpha >= beta:
                        break
            return max_eval, best_action
        
        else:
            min_eval = np.inf
            best_action = None
            valids = self.game.getValidMoves(board, player)

            for action in range(self.game.getActionSize()):
                if valids[action]==1:
                    next_board, _ = self.game.getNextState(board, player, action)
                    #print("next_board min")
                    #print(next_board)
                    evaluation = self.alpha_beta(next_board, -player, depth-1, alpha, beta, True)[0]
                    min_eval = min(min_eval, evaluation)
                    if min_eval == evaluation:
                        best_action = action
                    beta = min(beta, min_eval)
                    if alpha >= beta:
                        break
            return min_eval, best_action


    def play(self, board, player):
        time.sleep(2)
        board = board*player
        print(board)
        print(f"player -> {player}")
        score, action = self.alpha_beta(board, player, 3, -math.inf, math.inf, True)
        #for candidate in self.candidates:
        #    print(candidate, self.candidates[candidate])
        #    print()
        #print(score)
        #print(action)
        self.candidates.clear()
        return action


class A4x4():
    def __init__(self, game):
        self.game = game
        self.nnet = nn(game)
        self.nnet.load_model('C:/Users/joaom/Desktop/ataxx_trabalho2_liacd/models/', 'A4x4.h5')
    
    def play(self, board):
        """ 
        one, two = self.nnet.predict(board)
        print(one)
        print(two)
        print(len(one))
        valids = self.game.getValidMoves(board, 1)
        print(valids)
        print(np.argmax(one))
        """

        args = dotdict({'numMCTSSims': 25, 'cpuct': 1.0})
        mcts = MCTS(self.game, self.nnet, args)

        #action = players[curPlayer + 1](self.game.getCanonicalForm(board, curPlayer))
        return np.argmax(mcts.getActionProb(board, temp=0))














class HumanPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
        pygame.init()
        valid = self.game.getValidMoves(board, 1)
        #for i in range(len(valid)):
        #    if valid[i]:
        #        print("[", int(i/self.game.size), int(i%self.game.size), end="] ")
        while True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posy = event.pos[0]
                    y = int(math.floor(posy/SQUARE_SIZE)) 
                    posx = event.pos[1]
                    x = int(math.floor(posx/SQUARE_SIZE)) 
                    try:
                        if ((0 <= x) and (x < self.game.size) and (0 <= y) and (y < self.game.size)) or \
                            ((x == self.game.size) and (y == 0)):
                            a = self.game.size * x + y if x != -1 else self.game.size ** 2
                        if valid[a]:
                            return a
                        else:
                            print("invalid move")
                    except ValueError:
                        'Invalid integer'
            #print('Invalid move')
                        


            """
            input_move = input()
            input_a = input_move.split(" ")
            if len(input_a) == 2:
                try:
                    #x,y = [int(i) for i in input_a]
                    if ((0 <= x) and (x < self.game.size) and (0 <= y) and (y < self.game.size)) or \
                            ((x == self.game.size) and (y == 0)):
                        a = self.game.size * x + y if x != -1 else self.game.size ** 2
                        if valid[a]:
                            break
                except ValueError:
                    # Input needs to be an integer
                    'Invalid integer'
            print('Invalid move')
            """
        return a

















