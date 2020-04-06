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
