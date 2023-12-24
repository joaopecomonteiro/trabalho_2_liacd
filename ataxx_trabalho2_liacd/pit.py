import Arena
from MCTS import MCTS
from Ataxx.AtaxxGame import AtaxxGame
from Ataxx.AtaxxPlayers import *
from Ataxx.tensorflow.NNet import NNetWrapper as NNet


import numpy as np
from utils import *
import tensorflow as tf

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

mini_ataxx = True  # Play in 6x6 instead of the normal 8x8.
human_vs_cpu = True

if mini_ataxx:
    g = AtaxxGame(4)
else:
    g = AtaxxGame(6)

# all players
#rp = RandomPlayer(g).play
gp = GreedyPlayer(g).play
abp = AlphaBeta(g).play
hp = HumanPlayer(g).play
#model = tf.keras.models.load_model('C:\Users\joaom\Desktop\ataxx_trabalho2_liacd\models\A4x4.h5')
A4x4p = A4x4(g).play
"""
# nnet players
n1 = NNet(g)
if mini_ataxx:
    n1.load_checkpoint('./pretrained_models/othello/pytorch/','6x100x25_best.pth.tar')
else:
    n1.load_checkpoint('./pretrained_models/othello/pytorch/','8x8_100checkpoints_best.pth.tar')
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

if human_vs_cpu:
    player2 = hp
else:
    n2 = NNet(g)
    n2.load_checkpoint('./pretrained_models/othello/pytorch/', '8x8_100checkpoints_best.pth.tar')
    args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.
"""


arena = Arena.Arena(hp, A4x4p, g, display=AtaxxGame.display)

print(arena.playGames(2, verbose=True))