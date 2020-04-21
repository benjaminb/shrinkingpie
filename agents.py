# Some players mocked up
import random

class AlwaysAccepts():

    def __init__(self):
        pass

    def offer(self, players, state, history):
        return 0.5

    def response(self, players, offer, state, history):
        return 'accept'

class AcceptsAnyPositive():
    def __init__(self):
            pass

    def offer(self, players, state, history):
            return 0.5

    def response(self, players, offer, state, history):
            return 'accept' if offer else 'reject'

class AlwaysRejects():

    def __init__(self):
        pass

    def offer(self, players, state, history):
        return 0.5

    def response(self, players, offer, state, history):
        return 'reject'

class AlwaysCounterPrevious():
    def __init__(self):
        pass

    def offer(self, players, state, history):
        # look up other player in history previous round
        # for round in history:

        # If the other player has never made an offer:
        return 0.5

    def response(self, players, offer, state, history):
        return 'counter'

class Hardballer():
    def __init__(self):
        pass

    def offer(self, players, state, history):
        return 0.01

    def response(self, players, offer, state, history):
        return 'counter'

class TitForTat():
    def __init__(self, init_offer=0.5):
        self.init_offer = init_offer
        self.last_offer = {}

    def offer(self, players, state, history):
        opponent = players[1]
        if opponent in self.last_offer:
            return self.last_offer[opponent]
        return self.init_offer

    def response(self, players, offer, state, history):
        self.last_offer[players[0]] = offer # Record the offer
        return 'accept'

class Jonabot():
    name = 'Jonabot'
    def __init__(self):
        self.last_offer = {}

    def offer(self, players, state, history):
        # if first time meeting this particular player, offer 0.5
        opponent = players[1]
        if opponent not in self.last_offer:
            return 0.5
        # else
        if self.last_offer[opponent] > 0.5:
            return 1 - self.last_offer[opponent]

        diff = 0.5 - self.last_offer[opponent]
        return 1 - (self.last_offer[opponent] + diff / 2)

    def response(self, players, offer, state, history):
        self.last_offer[players[0]] = offer

        if offer >= 0.5:
            return 'accept'

        discount = state.current_discounts[players][1]
        if discount < 0.3:
            return 'reject'

        return 'counter'

class GhostofRudin():
        def __init__(self):
            self.split = 0.1

        def offer(self, players, state, history):
            # was I paired with this player last round?
            # if so, offer last offer + 0.1
            if 1 not in state.current_discounts[players]:
                self.split = min(1, self.split + 0.1)
            else:
                self.split = 0.1
            return self.split

        def response(self, players, offer, state, history):
            if offer >= 0.5:
                return 'accept'

            if offer < 0.25:
                return 'reject'

            return 'counter'

from statistics import mean

class Mimic():

    def __init__(self):
        pass

    def offer(self, players, state, history):
        if state.round == 1:
            return 0.01
        return mean([table['offer'] for table in history[-1].current_discounts.values()])

    def response(self, players, offer, state, history):
        if state.round == 1:
            return 'accept'

        responses = [table['response'] for table in history[-1].current_discounts.values()]
        counts = {'accept': responses.count('accept'),
                    'reject': responses.count('reject'),
                    'counter': responses.count('counter')}
        return max(counts, key=counts.get)

class DD():
    def __init__(self):
        pass

    def offer(self, players, state, history):
        # Determine the last offer the opponent accepted, make that offer
        if state.round == 1:
            return 0.5

        opponent = players[1]
        last = self.last_accepted(opponent, history)
        if last:
            return last
        # If they never accepted an offer, make the average offer
        return mean([table['offer'] for table in history[-1].current_discounts.values()])


    def response(self, players, offer, state, history):
        # if average offer of all OTHER players is higher than this offer, reject
        if state.round == 1:
            return 'accept'

        avg_offer = mean([table['offer'] for table in history[-1].current_discounts.values()])

        return 'accept' if avg_offer <= offer else 'reject'

    def last_accepted(self, player, history):
        for i in range(len(history)):
            for table in history[-(i + 1)].current_discounts:
                if player == table[1] and history[-(i + 1)].current_discounts[table]['response'] == 'accept':
                    return history[-(i + 1)].current_discounts[table]['offer']
        return None
