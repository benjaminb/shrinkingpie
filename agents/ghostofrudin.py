from agent import Agent
from constants import *


class GhostofRudin(Agent):
        def __init__(self, name=None):
            super().__init__(name)
            self.split = 0.1

        def offer(self, table):
            # was I paired with this player last round?
            # if so, offer last offer + 0.1
            if 1 not in table.discounts:
                self.split = min(1, self.split + 0.1)
            else:
                self.split = 0.1
            return self.split

        def response(self, table, offer):
            if offer >= 0.5:
                return ACCEPT

            if offer < 0.25:
                return REJECT

            return COUNTER
