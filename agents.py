# Some players mocked up
import random
from constants import *

class Agent():
    '''Duck type:
    an Agent must have an offer method and a response method
    The offer method must return a number 0 to 1, the proportion of the pie
    they propose to split.
    The response method must return one of three strings in the 'actions' list
    Any logic may be implemented to arrive at these return values.
    For complete information, the Agent must have access to the current
    state of the game as well as the complete history.'''

    def __init__(self, name=None):
        self.name = name
        self.id = None
        self.game = None
        pass

    def offer(self, table):
        pass

    def response(self, table, offer):
        pass

class Asker(Agent):
    def offer(self, table):
        # STATE, HISTORY
        history = self.game.history
        return 0.5

    def response(self, table, offer):
        history = self.game.history
        return ACCEPT


class AlwaysAccepts(Agent):

    def offer(self, table):
        return 0.5

    def response(self, table, offer):
        return ACCEPT


class AcceptsAnyPositive(Agent):

    def offer(self, table):
            return 0.5

    def response(self, table, offer):
            return ACCEPT if offer else REJECT

class AlwaysRejects(Agent):
    def offer(self, table):
        return 0.5

    def response(self, table, offer):
        return REJECT

class AlwaysCounterPrevious(Agent):
    def __init__(self):
        pass

    def offer(self, table):
        # look up other player in history previous round
        # for round in history:

        # If the other player has never made an offer:
        return 0.5

    def response(self, table, offer):
        return COUNTER

class Hardballer(Agent):
    def offer(self, table):
        return 0.01

    def response(self, table, offer):
        return COUNTER

class TitForTat(Agent):
    def __init__(self, name=None, init_offer=0.5):
        super().__init__(name)
        self.name = name
        self.id = None
        self.init_offer = init_offer
        self.last_offer = {}

    def offer(self, table):
        responder = table.players[1]
        if responder in self.last_offer:
            return self.last_offer[responder]
        return self.init_offer

    def response(self, table, offer):
        self.last_offer[table.players[0]] = offer # Record the offer
        return ACCEPT

class Jonabot(Agent):
    name = 'Jonabot'
    def __init__(self, name=None):
        super().__init__(name)
        self.last_offer = {}

    def offer(self, table):
        # if first time meeting this particular player, offer 0.5
        opponent = table.players[1]
        if opponent not in self.last_offer:
            return 0.5
        # else
        if self.last_offer[opponent] > 0.5:
            return 1 - self.last_offer[opponent]

        diff = 0.5 - self.last_offer[opponent]
        return 1 - (self.last_offer[opponent] + diff / 2)

    def response(self, table, offer):
        self.last_offer[table.players[0]] = offer

        if offer >= 0.5:
            return ACCEPT

        discount = table.game.state.current_discounts[table.players][1]
        if discount < 0.3:
            return REJECT

        return COUNTER

class GhostofRudin(Agent):
        def __init__(self, name=None):
            super().__init__(name)
            self.split = 0.1

        def offer(self, table):
            # was I paired with this player last round?
            # if so, offer last offer + 0.1
            if 1 not in table.discounts:
                self.split = min(1, self.split + 0.1)
            else:
                self.split = 0.1
            return self.split

        def response(self, table, offer):
            if offer >= 0.5:
                return ACCEPT

            if offer < 0.25:
                return REJECT

            return COUNTER

from statistics import mean

class Mimic(Agent):
    def offer(self, table):
        if table.game.state.round == 1:
            return 0.01
        return mean([t['offer'] for t in table.game.history[-1].current_discounts.values()])

    def response(self, table, offer):
        if table.game.state.round == 1:
            return ACCEPT

        responses = [t['response'] for t in table.game.history[-1].current_discounts.values()]
        counts = {ACCEPT: responses.count(ACCEPT),
                    REJECT: responses.count(REJECT),
                    COUNTER: responses.count(COUNTER)}
        return max(counts, key=counts.get)

class DD():
    def offer(self, table):
        # Determine the last offer the opponent accepted, make that offer
        if table.game.state.round == 1:
            return 0.5

        opponent = table.players[1]
        last = self.last_accepted(opponent, table)
        if last:
            return last
        # If they never accepted an offer, make the average offer
        return mean([t['offer'] for t in table.game.history[-1].current_discounts.values()])


    def response(self, table, offer):
        # if average offer of all OTHER players is higher than this offer, reject
        if table.game.state.round == 1:
            return ACCEPT

        avg_offer = mean([t['offer'] for t in table.game.history[-1].current_discounts.values()])

        return ACCEPT if avg_offer <= offer else REJECT

    def last_accepted(self, player, table):
        for i in range(len(table.game.history)):
            for t in table.game.history[-(i + 1)].current_discounts:
                if player == t[1] and table.game.history[-(i + 1)].current_discounts[t]['response'] == ACCEPT:
                    return table.game.history[-(i + 1)].current_discounts[t]['offer']
        return None
