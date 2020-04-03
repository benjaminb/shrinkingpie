import random
from inspect import signature

# Classes needed

# singleton class for the history object
    # include a component for current game state/scores
    # current round
history = {
            'round': [[]], # Each element is a list of records for the round
            'testdata': 'test value'

}


class ISPT():
    """Structre of the game"""

    def __init__(self, players=None, initial_score=0):
        self.history = []
        self.state = {'round': 1} # Will contain current game state for convenience
        self.players = players
        self.score = {player: initial_score for player in players}

        self.odd_player = None

    # A method that tells the instance to play the game
    def play(self, max_rounds=1000):
        if not self.players:
            print("No players added to the game!")
            return

        # Create the first round of tables by randomly pair player indices

        pairs = self.init_tables()
        print("Pairings:", pairs)

        while self.state['round'] < max_rounds:

            # Process the tables
                # updates the history

            # Set up next round's tables

            # Update the current game state

            self.state['round'] += 1

        return

    def init_tables(self):
        pairs = []
        num_players = len(self.players)
        indices = {i for i in range(num_players)}

        # If we have an odd number of players
        if num_players % 2:
            # Create a second table with a randomly chosen player
            pair = random.sample(indices, 2)
            self.odd_player = pair[1]
            print("Odd player chosen for 2nd table in round 1:", pair[1])
            indices -= {pair[0]}
            pairs.append(pair)

        # Now we're guaranteed to have an even number of players
        while indices:
            pair = random.sample(indices, 2)
            indices -= set(pair)
            pairs.append(pair)

        return pairs





# Class for agent
class Agent():
    '''Duck type:
        an Agent must have an offer method and a response method
        The offer method must return a number 0 to 1, the proportion of the pie
            they propose to split.
        The response method must return one of three strings in the 'actions' list
        Any logic may be implemented to arrive at these return values.
        For complete information, the Agent must have access to the current
            state of the game as well as the complete history.'''

    def __init__(self, split=0.0, name=None):
        self.split = split
        self.name = name

        # CONSIDER: should actions be an enum?
        self.actions = ['accept', 'counter', 'reject']
        # TODO make a helper function to ensure unique name strings
        # memory location of agent can serve as ID?
    # Needs to determine how to make an offer
    # TODO add history
    def offer(self, pie):
        '''What offer to make
            depending on current state of the Game
            or anything from the past, in the history object

            1 idea: pass a tuple of game states to test

            this needs to return a proportion
        '''
        global history
        global game
        split = self.split
        # logic for split
        # if pie > x then split == 0.4
        # if I had a list of conditions I could iterate over them
        # and implement an offer strategy
        # for condition, action in [list passed in]:
        #   if condition1 then action1; break
        return split

    # Needs to determine a response
    def response(self, offer, pie):
        global history
        global game
        global actions
        print("Agent's response as been called.")
        print('history object accessed:', history['testdata'])

        # start off by always accepting
        return self.actions[0]
        # Given an offer and the history, how would I respond?


# Class for tables
class Table(): # aka table
    """Determines structure for a round of actions"""

    def __init__(self, players, offerer=None, pie=1):
        """Takes two players and runs a round
           If no offerer is specified, choose one randomly"""
        """Offerer should be the index of the player whose offers"""

        # Validate input
        if len(players) != 2:
            print("Table() didn't receive two players!")
            raise ValueError

        # Set the offerer and responder or randomize if we don't have one
        self.offerer = players.index(offerer) if offerer else random.choice(players)
        self.responder = players[(players.index(self.offerer) + 1) % 2]

        self.pie = pie


    def create_record(self, offer, response):
        # Try to write something into history
        global history
        global game
        record = {'offerer': self.offerer, 'responder': self.responder,
                    'offer': offer, 'response': response}
        print("writing to game information")
        game.information[-1].append(record)
        print(game.information)

        return {'offerer': self.offerer, 'responder': self.responder,
                    'offer': offer, 'response': response}

    def process(self):
        global history

        # Get actions from players
        self.offer = self.offerer.offer(self.pie)
        self.response = self.responder.response(self.offer, self.pie)

        # Write the actions to the history object
        record = self.create_record(self.offer, self.response)
        history['round'][-1].append(record)

        # CASE: response is accept
        if self.response == "accept":
            # add points to singleton
            print("offer accepted!")
            print("offerer gets:", 1 - self.offer)
            print()

            return

        # CASE: response is to counteroffer

        if self.response == "counter":
            # Decrease the pie by the disount parameter
            print("offer countered!")

            # Instantiate the Table for next round
            return

        # CASE: response is to reject
        print("offer rejected!")

        # Return the results...to what?
        # What should the return object be?
        return

def valid_agent(player):
    '''An agent must have the methods .offer and .response,
       and they must have the same signature as that of Agent class'''

    # Constants
    OFFER_SIG = ['pie']
    RESPONSE_SIG = ['offer', 'pie']

    # Check player has correct methods
    if not all([hasattr(player, 'offer'), hasattr(player, 'response')]):
        print("player missing .offer or .response method")
        return False

    # Check methods have correct signature
    offer_sig = [p for p in signature(player.offer).parameters]
    if offer_sig != OFFER_SIG:
        print("player doesn't have correct signature for player.offer")
        return False

    response_sig = [p for p in signature(player.response).parameters]
    if response_sig != RESPONSE_SIG:
        print("player doesn't have correct signature for player.response")
        return False

    return True
