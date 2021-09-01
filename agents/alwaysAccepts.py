from agent import Agent
from constants import *


class AlwaysAccepts(Agent):
    def __init__(self, name=None, offer=0.5):
        super().__init__(name)
        self.offer = offer

    def offer(self, table):
        return self.offer

    def response(self, table, offer):
        return ACCEPT
