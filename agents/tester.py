from agent import Agent
from constants import *
from api import ISPT


class Tester(Agent):
    def __init__(self, name=None, init_offer=0.5):
        super().__init__(name)
        self.init_offer = init_offer

    def offer(self, table):
        history = ISPT.get_history(players=[1, 5, 9])
        offers = []
        for round in history:
            offers += [t.offer for t in round]

        if offers:
            return sum(offers) / len(offers)
        else:
            return 0.25

    def response(self, table, offer):
        last = ISPT.get_history()[-1]
        accepted = [table.offer for table in last if table.response == ACCEPT]

        return ACCEPT if accepted else COUNTER