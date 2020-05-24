from agent import Agent
from constants import *

class TitForTat(Agent):
    def __init__(self, name=None, init_offer=0.5):
        super().__init__(name)
        self.init_offer = init_offer
        self.last_offer = {}

    def offer(self, table):
        responder = table.players[1]
        if responder in self.last_offer:
            return self.last_offer[responder]
        return self.init_offer

    def response(self, table, offer):
        self.last_offer[table.players[0]] = offer # Record the offer
        return ACCEPT
