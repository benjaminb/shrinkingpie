from agent import Agent
from constants import *
from random import random, randint


class Random(Agent):
    def offer(self, table):
        return random()

    def response(self, table, offer):
        return randint(0, 2)
