# Some players mocked up

class AlwaysAccepts():

    def __init__(self):
        pass

    def offer(self, opponent, state, history, pie):
        return 0.5

    def response(self, opponent, offer, state, history, pie):
        return 'accept'

class AcceptsAnyPositive():
    def __init__(self):
            pass

    def offer(self, opponent, state, history, pie):
            return 0.5

    def response(self, opponent, offer, state, history, pie):
            return 'accept' if offer else 'reject'

class AlwaysRejects():

    def __init__(self):
        pass

    def offer(self, opponent, state, history):
        return 0.5

    def response(self, opponent, offer, state, history):
        return 'reject'

class AlwaysCounterPrevious():
    def __init__(self):
        pass

    def offer(self, opponent, state, history):
        # look up other player in history previous round
        # for round in history:

        # If the other player has never made an offer:
        return 0.5

    def response(self, opponent, offer, state, history):
        return 'counter'

class Hardballer():
    def __init__(self):
        pass

    def offer(self, opponent, state, history):
        return 0.01

    def response(self, opponent, offer, state, history):
        return 'counter'

class TitForTat():
    def __init__(self, init_offer=0.5):
        self.init_offer = init_offer
        self.last_offer = {}

    def offer(self, opponent, state, history):
        # If
        if opponent in self.last_offer:
            return self.last_offer[opponent]
        return self.init_offer

    def response(self, opponent, offer, state, history):
        self.last_offer[opponent] = offer # Record the offer
        return 'accept'
