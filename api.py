import random
from inspect import signature
import pprint as pp



class ISPT():
    """Structure of the game"""

    def __init__(self, players, initial_score=0):
        """
        Attempting to refer to players by index rather than memory location unless
        player's methods are needed

        """
        self.players = players

        # Create a dictionary mapping of player object to their index in self.players?
        self.history = []
        self.state = {  'num_players': len(players),
                        'round': 1,
                                        # Will match the index of players in self.players
                        'table_count': [0 for player in players]
                     } # Will contain current game state for convenience
        self.score = {idx: initial_score for idx in range(len(players))}

        self.odd_player = None

    # A method that tells the instance to play the game
    def play(self, max_rounds=1000):
        if not self.players:
            print("No players added to the game!")
            return

        # Create the first round of tables by randomly pair player indices
        tables = [Table(players = [self.players[i] for i in pair])
                    for pair in self.init_tables()]

        print("Initial pairings:", tables)

        untabled_players = []
        while self.state['round'] < max_rounds:

            # Get untabled players, assign them to new tables
            # Except they cannot be assigned to players they were previously
            # tabled with
            # Process the tables
            results = []
            new_tables = []

            # pop tables and while table?
            for table in tables:
                result = table.process(self.state, self.history)

                # If responder rejected, they leave the table
                if result['response'] == 'reject':
                    print("REJECTED!!!")
                    # Get the index of the players
                    players = (self.players.index(table.offerer),
                                self.players.index(table.responder))

                    self.decrease_table_count(players)

                    # Hangle any untabled players
                    untabled_players = [p for p in players
                                        if not self.state['table_count'][p]]

                    for player in untabled_players:
                        indices = [i for i in range(self.state['num_players'])
                                    if i not in players]
                        new_pair = [player, random.choice(indices)]
                        self.increase_table_count(new_pair)
                        # TODO have instantiation of Table increment the table count
                        new_tables.append(Table(players=new_pair))

                    # If so, create new table excepting each other
                        # sample from all indices except self and other player
                        # create new table

                if result['response'] == 'counter':

                    players = (self.players.index(table.offerer),
                                self.players.index(table.responder))

                    tables.append(Table(players=players, offerer=table.responder))


                results.append(result)

            print("Untabled players:", untabled_players)
            # updates the history
            self.history.append(results)

            # Set up next round's tables

            # Update the current game state

            self.state['round'] += 1

        print("History of the game:")
        for i, round in enumerate(self.history):
            print("Round:", i)
            pp.pprint(round)

        # TODO: save output to csv
        return

    def init_tables(self):
        pairs = []
        indices = {i for i in range(self.state['num_players'])}

        # If we have an odd number of players
        if self.state['num_players'] % 2:
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

        for pair in pairs:
            self.increase_table_count(pair)

        return pairs

    def increase_table_count(self, indices):
        for i in indices:
            self.state['table_count'][i] += 1
        return

    def decrease_table_count(self, indices):
        ''' Pass change = -1 fo decrease '''
        for i in indices:
            self.state['table_count'][i] -= 1
        return


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
    def offer(self, state, history, pie):
        '''What offer to make
            depending on current state of the Game
            or anything from the past, in the history object

            1 idea: pass a tuple of game states to test

            this needs to return a proportion
        '''

        split = self.split
        # logic for split
        # if pie > x then split == 0.4
        # if I had a list of conditions I could iterate over them
        # and implement an offer strategy
        # for condition, action in [list passed in]:
        #   if condition1 then action1; break
        return split

    # Needs to determine a response
    def response(self, offer, state, history, pie):
        print("Agent's response as been called.")

        # start off by always accepting
        return self.actions[0]
        # Given an offer and the history, how would I respond?


# Class for tables
class Table(): # aka table
    """Determines structure for a round of actions"""

    def __init__(self, players, offerer=None, pie=1):
        """Takes two players and runs a round
           If no offerer is specified, choose one randomly

           players = [player A, player B]
           offerer = index of players which is the player
        """

        # Validate input
        if len(players) != 2:
            print("Table() didn't receive two players!")
            raise ValueError

        # Set the offerer and responder or randomize if we don't have one
        self.offerer = players[offerer] if offerer else random.choice(players)
        self.responder = players[(players.index(self.offerer) + 1) % 2]
        self.pie = pie

        # Update table count in game state



    def create_record(self, offer, response):

        return {'offerer': self.offerer, 'responder': self.responder,
                    'offer': offer, 'response': response}

    def process(self, state, history):

        # Get actions from players
        self.offer = self.offerer.offer(state, history, self.pie)
        self.response = self.responder.response(self.offer, state, history, self.pie)

        # Write the actions to the history object
        record = self.create_record(self.offer, self.response)

        # CASE: response is accept
        if self.response == "accept":


            return record

        # CASE: response is to counteroffer

        if self.response == "counter":
            # Decrease the pie by the disount parameter
            # Instantiate the Table for next round with offering player determined
            return record

        # CASE: response is to reject

        # Return the results...to what?
        # What should the return object be?
        return record

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
