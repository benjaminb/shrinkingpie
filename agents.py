# Some players mocked up

class AlwaysAccepts():

    def __init__(self):
        pass

    def offer(self, state, history, pie):
        return 0.5

    def response(self, offer, state, history, pie):
        return 'accept'

class AcceptsAnyPositive():
        def __init__(self):
            pass

        def offer(self, state, history, pie):
            return 0.5

        def response(self, offer, state, history, pie):
            return 'accept' if offer else 'reject'

class AlwaysRejects():

    def __init__(self):
        pass

    def offer(self, state, history, pie):
        return 0.5

    def response(self, offer, state, history, pie):
        return 'reject'

def AlwaysCounterPrevious():
    def __init__(self):
        pass

    def offer(self, state, history, pie):
        # look up other player in history previous round
        # for round in history:

        # If the other player has never made an offer:
        return 0.5

    def response(self, offer, state, history, pie):
        return 'counter'

class Hardballer():
    def __init__(self):
        pass

    def offer(self, state, history, pie):
        # look up other player in history previous round
        # for round in history:

        # If the other player has never made an offer:
        return 0.1

    def response(self, offer, state, history, pie):
        return 'counter'
