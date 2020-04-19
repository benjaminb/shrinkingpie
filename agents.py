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
class Overthinker():
        def __init__(self):
            pass

        def offer(self, players, state, history):
            # was I paired with this player last round?
            # if so, offer last offer + 0.1
            if state.round == 1:
                return 0.01
            return mean([record.offer for record in history[-1]])

        def response(self, players, offer, state, history):
            if state.round == 1:
                return 'accept'

            accept_count = sum([1 for record in history[-1] if record.response == 'accept'])
            counter_count = sum([1 for record in history[-1] if record.response == 'counter'])
            reject_count = sum([1 for record in history[-1] if record.response == 'reject'])
            counts = [accept_count, counter_count, reject_count]

            if accept_count == max(counts):
                return 'accept'
            if counter_count == max(counts):
                return 'counter'
            return 'reject'

class LinBot():
    def __init__(self):
        pass

    def offer(self, players, state, history):
        # average offer
        if state.round == 1:
            return 0.3

        offers = []
        for round in history:
            for table in round:
                offers.append(table.offer)
        return mean(offers)

    def response(self, players, offer, state, history):
        if offer >= 0.5:
            return 'accept'

        if offer >= 0.3:
            return 'counter'
        return 'reject'

class Rando():
    def __init__(self):
        pass

    def offer(self, players, state, history):
        # average offer
        return random.random()

    def response(self, players, offer, state, history):
        choice = random.choice(['accept', 'counter', 'reject'])
        return choice
