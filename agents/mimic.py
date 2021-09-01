from agent import Agent
from constants import *
from api import ISPT
from statistics import mean


class Mimic(Agent):
    # Returns the mean offer of all offers made in previous round
    def offer(self, table):
        if ISPT.round() == 1:
            return 0.01
        last_round = ISPT.get_history()[-1]
        return mean([t.offer for t in last_round])

    def response(self, table, offer):
        if ISPT.round() == 1:
            return ACCEPT

        last_round = ISPT.get_history()[-1]
        responses = [t.response for t in last_round]
        counts = {
            ACCEPT: responses.count(ACCEPT),
            REJECT: responses.count(REJECT),
            COUNTER: responses.count(COUNTER)
        }
        return max(counts, key=counts.get)
