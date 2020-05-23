from agent import Agent
from constants import *

class Hardballer(Agent):
    def offer(self, table):
        return 0.01

    def response(self, table, offer):
        return COUNTER
