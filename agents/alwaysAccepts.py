from agent import Agent
from constants import *

class AlwaysAccepts(Agent):

    def offer(self, table):
        return 0.5

    def response(self, table, offer):
        return ACCEPT
