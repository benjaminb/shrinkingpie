import os
import sys, inspect
import importlib
import pprint as pp
from api import *
from agent import Agent

# Add local path to sys
sys.path.append(os.getcwd())
sys.path.append('agents')


# Import agent modules
agent_strings = [f[:-3] for f in os.listdir('agents') if f.endswith('.py')]
for a in agent_strings:
    importlib.import_module(a)

# Instantiate players
players = []
for agent in agent_strings:
    players += [obj() for name, obj in inspect.getmembers(sys.modules[agent])
                if inspect.isclass(obj) and name != 'Agent']

# Instantiate game
game = ISPT(players=players)
history = game.play(max_rounds=5, export_csv=False)
pp.pprint(history)
print(players[0].__class__.__name__)
