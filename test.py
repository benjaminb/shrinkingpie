import os
import sys, inspect
import importlib
import pprint as pp
from api import *
from agent import Agent
from matplotlib_chord import chordDiagram
import numpy as np

# Add local path to sys
sys.path.append(os.getcwd())


player_data = [
                 # ['tester', ['t1']],
                 # ['tester', ['tester 0.1', 0.1]],
                 # ['tester', ['t3', 0.2]],
                 ['mimic', ['mimic']],
                 # ['titfortat', ['tft']],
                 # ['titfortat', ['tft01', 0.01]],
                 # ['jonabot', []],
                 # ['ghostofrudin', ['gor']],
                 # ['alwaysRejects', ['ar1']],
                 ['alwaysRejects', ['ar2']],
                 ['dd', ['dd']],
                 ['dd', ['dd2']],
                 ['dd', ['dd3']]
              ]

# Instantiate players
players = []
sys.path.append('agents')
for agent_str, args in player_data:
    importlib.import_module(agent_str)
    players += [obj(*args) for name, obj in inspect.getmembers(sys.modules[agent_str])
                    if name.lower() == agent_str and name != 'Agent']


# Instantiate game
game = ISPT(players=players, info_availability={0: [0, 1]})
history = game.play(max_rounds=5, termination_prob=(100, 0), export_csv=False)


# results = ISPT.get_history()
# print(results)
# pp.pprint(ISPT.get_history())

# game.sb()

# game.graph_scores()
# game.chord_chart()
