from agent import Agent
from constants import *


class Titfortat(Agent):
    def __init__(self, name=None, init_offer=0.5, cooperation_level=0.3):
        super().__init__(name)
        self.init_offer = init_offer
        self.last_offer_received = {}  # player_id: offer received
        self.last_offer_made = {}
        self.cooperation_level = cooperation_level

    def offer(self, table):
        return self.last_offer_received.get(table.responder, self.init_offer)

    def response(self, table, offer):
        previous_offer = self.last_offer_received.get(table.offerer, None)
        self.last_offer_received[table.responder] = offer  # Record the offer

        if offer < self.cooperation_level:
            return REJECT
        # If current offer >= the last offer received from this player:
        if previous_offer and offer >= previous_offer:
            return ACCEPT
        return COUNTER
