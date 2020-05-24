from agent import Agent
from constants import *
from api import ISPT
from statistics import mean

class Mimic(Agent):
    def offer(self, table):
        if ISPT.round() == 1:
            return 0.01

        last_round = ISPT.get_history()[-1]
        return mean([t['offer'] for t in last_round.tables.values()])


    def response(self, table, offer):
        if ISPT.round() == 1:
            return ACCEPT

        last_round = ISPT.get_history()[-1].tables
        responses = [t['response'] for t in last_round.values()]
        counts = {ACCEPT: responses.count(ACCEPT),
                  REJECT: responses.count(REJECT),
                  COUNTER: responses.count(COUNTER)}
        return max(counts, key=counts.get)
