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
        if not name:
            print("instantiating name", self.__class__)
        self.name = name
        self.id = None
        self.game = None
        pass

    def offer(self, table):
        pass

    def response(self, table, offer):
        pass
