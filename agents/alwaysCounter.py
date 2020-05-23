from agent import Agent
from constants import *


class AlwaysCounterPrevious(Agent):

    def offer(self, table):
        # look up other player in history previous round
        # for round in history:

        # If the other player has never made an offer:
        return 0.5

    def response(self, table, offer):
        return COUNTER
