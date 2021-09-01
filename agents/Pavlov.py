from agent import Agent
from constants import *


class Pavlov(Agent):
    def __init__(self, name=None, accept_level=0.3, counter_level=0.2):
        super().__init__(name)
        self.not_cooperating = set()
        self.accept_level = accept_level
        self.counter_level = counter_level

    def offer(self, table):
        if table.responder in self.not_cooperating:
            return self.counter_level
        return self.accept_level

    def response(self, table, offer):
        response = REJECT
        # If Pavlov is cooperating, record response
        if table.offerer not in self.not_cooperating:
            if offer >= self.accept_level:
                response = ACCEPT
            elif offer >= self.counter_level:
                response = COUNTER

        # Update cooperation
        if offer < self.counter_level:
            self.not_cooperating.add(table.offerer)
        else:
            self.not_cooperating.discard(table.offerer)

        return response
