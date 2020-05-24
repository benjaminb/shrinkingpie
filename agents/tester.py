from agent import Agent
from constants import *
from api import ISPT


class Tester(Agent):
    def __init__(self, name=None, init_offer=0.5):
        super().__init__(name)
        print("called super")
        self.init_offer = init_offer


    def offer(self, table):
        return self.init_offer

    def response(self, table, offer):
        return ACCEPT
