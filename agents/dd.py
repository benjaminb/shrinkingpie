from agent import Agent
from api import ISPT
from statistics import mean
from constants import *

# TODO: FIX
class DD(Agent):
    def offer(self, table):
#         # Determine the last offer the opponent accepted, make that offer
#         if table.game.state.round == 1:
#             return 0.5
        if ISPT.round() == 1:
            return 0.5

        last_accepted = self.last_accepted(table.players[1])
        return last_accepted if last_accepted else 0.5

    def response(self, table, offer):
        if ISPT.round() == 1:
            return ACCEPT

        # If current offer better than last round's average, accept
        offers = [t.offer for t in ISPT.get_history()[-1]]
        avg_offer = mean(offers) if offers else 0
        return ACCEPT if avg_offer <= offer else REJECT

    def last_accepted(self, player):
        '''Gets the last offer accepted by the player, if any.'''

        history = ISPT.get_history()
        for i in reversed(range(len(history))):
            if history[i]:      # Check that the round isn't an empty list
                for t in history[i]:
                    if t.players[1] == player and t.response == ACCEPT:
                        return t.offer
        return None
