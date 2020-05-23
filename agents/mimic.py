from agent import Agent
from constants import *


from statistics import mean

class Mimic(Agent):
    def offer(self, table):
        # TODO: fix this
        # if table.game.state.round == 1:
        #     return 0.01
        # return mean([t['offer'] for t in table.game.history[-1].current_discounts.values()])
        return 0.5

    def response(self, table, offer):
        # if table.game.state.round == 1:
        #     return ACCEPT
        #
        # responses = [t['response'] for t in table.game.history[-1].current_discounts.values()]
        # counts = {ACCEPT: responses.count(ACCEPT),
        #             REJECT: responses.count(REJECT),
        #             COUNTER: responses.count(COUNTER)}
        # return max(counts, key=counts.get)
        return ACCEPT
