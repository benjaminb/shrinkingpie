# Some players mocked up
import random

class AlwaysAccepts():

    def __init__(self):
        pass

    def offer(self, table):
        return 0.5

    def response(self, table, offer):
        return 'accept'

class AcceptsAnyPositive():
    def __init__(self):
            pass

    def offer(self, table):
            return 0.5

    def response(self, table, offer):
            return 'accept' if offer else 'reject'

class AlwaysRejects():

    def __init__(self):
        pass

    def offer(self, table):
        return 0.5

    def response(self, table, offer):
        return 'reject'

class AlwaysCounterPrevious():
    def __init__(self):
        pass

    def offer(self, table):
        # look up other player in history previous round
        # for round in history:

        # If the other player has never made an offer:
        return 0.5

    def response(self, table, offer):
        return 'counter'

class Hardballer():
    def __init__(self):
        pass

    def offer(self, table):
        return 0.01

    def response(self, table, offer):
        return 'counter'

class TitForTat():
    def __init__(self, init_offer=0.5):
        self.init_offer = init_offer
        self.last_offer = {}

    def offer(self, table):
        opponent = table.players[1]
        if opponent in self.last_offer:
            return self.last_offer[opponent]
        return self.init_offer

    def response(self, table, offer):
        self.last_offer[table.players[0]] = offer # Record the offer
        return 'accept'

class Jonabot():
    name = 'Jonabot'
    def __init__(self):
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
            return 'accept'

        discount = table.game.state.current_discounts[table.players][1]
        if discount < 0.3:
            return 'reject'

        return 'counter'

class GhostofRudin():
        def __init__(self):
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
                return 'accept'

            if offer < 0.25:
                return 'reject'

            return 'counter'

from statistics import mean

class Mimic():

    def __init__(self):
        pass

    def offer(self, table):
        if table.game.state.round == 1:
            return 0.01
        return mean([t['offer'] for t in table.game.history[-1].current_discounts.values()])

    def response(self, table, offer):
        if table.game.state.round == 1:
            return 'accept'

        responses = [t['response'] for t in table.game.history[-1].current_discounts.values()]
        counts = {'accept': responses.count('accept'),
                    'reject': responses.count('reject'),
                    'counter': responses.count('counter')}
        return max(counts, key=counts.get)

class DD():
    def __init__(self):
        pass

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
            return 'accept'

        avg_offer = mean([t['offer'] for t in table.game.history[-1].current_discounts.values()])

        return 'accept' if avg_offer <= offer else 'reject'

    def last_accepted(self, player, table):
        for i in range(len(table.game.history)):
            for t in table.game.history[-(i + 1)].current_discounts:
                if player == t[1] and table.game.history[-(i + 1)].current_discounts[t]['response'] == 'accept':
                    return table.game.history[-(i + 1)].current_discounts[t]['offer']
        return None
