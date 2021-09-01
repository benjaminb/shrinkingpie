from agent import Agent
from constants import *


class Grim(Agent):
    def __init__(self, name=None, offer=0.5, cooperation_level=0.3):
        super().__init__(name)
        self.offer_value = offer
        self.not_cooperating = set()
        self.cooperation_level = cooperation_level

    def offer(self, table):
        # Determine if Grim is cooperating with this player
        if table.responder in self.not_cooperating:
            return self.offer_value / 5
        return self.offer_value

    def response(self, table, offer):
        if offer < self.cooperation_level:
            self.not_cooperating.add(table.offerer)

        if table.offerer in self.not_cooperating:
            return REJECT
        return ACCEPT
