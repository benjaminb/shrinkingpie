from agent import Agent
from constants import *

class AlwaysRejects(Agent):
    def offer(self, table):
        return 0.5

    def response(self, table, offer):
        return REJECT
