from agent import Agent
from constants import *

# TODO: FIX 
# class DD():
#     def offer(self, table):
#         # Determine the last offer the opponent accepted, make that offer
#         if table.game.state.round == 1:
#             return 0.5
#
#         opponent = table.players[1]
#         last = self.last_accepted(opponent, table)
#         if last:
#             return last
#         # If they never accepted an offer, make the average offer
#         return mean([t['offer'] for t in table.game.history[-1].current_discounts.values()])
#
#
#     def response(self, table, offer):
#         # if average offer of all OTHER players is higher than this offer, reject
#         if table.game.state.round == 1:
#             return ACCEPT
#
#         avg_offer = mean([t['offer'] for t in table.game.history[-1].current_discounts.values()])
#
#         return ACCEPT if avg_offer <= offer else REJECT
#
#     def last_accepted(self, player, table):
#         for i in range(len(table.game.history)):
#             for t in table.game.history[-(i + 1)].current_discounts:
#                 if player == t[1] and table.game.history[-(i + 1)].current_discounts[t]['response'] == ACCEPT:
#                     return table.game.history[-(i + 1)].current_discounts[t]['offer']
#         return None
