from agent import Agent
from constants import *


# class Jonabot(Agent):
#     name = 'Jonabot'
#     def __init__(self, name=name):
#         super().__init__(name)
#         self.last_offer = {}
#
#     def offer(self, table):
#         # if first time meeting this particular player, offer 0.5
#         opponent = table.players[1]
#         if opponent not in self.last_offer:
#             return 0.5
#         # else
#         if self.last_offer[opponent] > 0.5:
#             return 1 - self.last_offer[opponent]
#
#         diff = 0.5 - self.last_offer[opponent]
#         return 1 - (self.last_offer[opponent] + diff / 2)
#
#     def response(self, table, offer):
#         self.last_offer[table.players[0]] = offer
#
#         if offer >= 0.5:
#             return ACCEPT
#
#         discount = table.game.state.current_discounts[table.players][1]
#         if discount < 0.3:
#             return REJECT
#
#         return COUNTER
