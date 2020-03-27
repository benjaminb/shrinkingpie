

# Classes needed

# singleton class for the history object
    # include a component for current game state/scores

class History():
    """History object for the game"""

    def __init__(self):
        self.history = []


# Class for agent
class Agent():

    def __init__(self):
        raise NotImplementedError


    # Needs to determine how to make an offer
    def offer(self, pie, history):
        raise NotImplementedError

    # Needs to determine a response
    def response(self, offer, pie, history):
        # Given an offer and the history, how would I respond?
# Class for meets
class Meet():
    """Determines structure for a round of actions"""

    def __init__(self):
        raise NotImplementedError
