import argparse
import os
import shutil
import time
import random
import numpy as np
import math
import sys
import tensorflow as tf

sys.path.append('../..')
from utils import *
from NeuralNet import NeuralNet


import argparse

from .AtaxxNNet import AtaxxNNet as ataxxnet

args = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 64,
    'cuda': False,
    'num_channels': 128,
})


class NNetWrapper(NeuralNet):
    def __init__(self, game):
        self.nnet = ataxxnet(game, args)
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()

    
    def train(self, examples):
        """
        examples: list of examples, each example is of form (board, pi, v)
        """
        input_boards, target_pis, target_vs = list(zip(*examples))
        input_boards = np.asarray(input_boards)
        exp_input_boards = np.expand_dims(input_boards, axis=-1)
        target_pis = np.asarray(target_pis)
        target_vs = np.asarray(target_vs)
        print("okok")
        print(exp_input_boards.shape)
        self.nnet.model.fit(x = exp_input_boards, y = [target_pis, target_vs], batch_size = args.batch_size, epochs = args.epochs)


    def predict(self, board):
        """
        board: np array with board
        """
        # timing
        start = time.time()

        # preparing input
        board = board[np.newaxis, :, :]

        # run
        pi, v = self.nnet.model.predict(board, verbose=False)

        #print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return pi[0], v[0]


    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.h5'):
        # change extension
        filename = filename.split(".")[0] + ".h5"

        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        self.nnet.model.save_weights(filepath)


    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.h5'):
        # change extension
        filename = filename.split(".")[0] + ".h5"

        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        
        if not os.path.exists(filepath):
            raise("No model in path {}".format(filepath))

        self.nnet.model.load_weights(filepath)


    def save_model(self, folder='checkpoint', filename='checkpoint.h5'):
        # change extension
        filename = filename.split(".")[0] + ".h5"

        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        self.nnet.model.save(filepath)



    def load_model(self, folder='checkpoint', filename='checkpoint.h5'):
                # change extension
        filename = filename.split(".")[0] + ".h5"

        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        
        if not os.path.exists(filepath):
            raise("No model in path {}".format(filepath))

        self.nnet.model = tf.keras.models.load_model(filepath)
        #self.nnet.model.load_model(filepath)




