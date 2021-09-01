from agent import Agent
from constants import *


class AlwaysRejects(Agent):
    def __init__(self, name=None, offer=0.5, reject=0.5):
        super().__init__(name)
        self.offer_value = offer
        self.reject_value = reject

    def offer(self, table):
        return self.offer_value

    def response(self, table, offer):
        return ACCEPT if offer >= self.reject_value else REJECT
