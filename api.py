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
        self.player_index = {player: i for i, player in enumerate(players)}

        # Create a dictionary mapping of player object to their index in self.players?
        self.history = []
        self.state = {  'num_players': len(players),
                        'round': 1,
                                        # Will match the index of players in self.players
                        'table_count': [0 for player in players]
                     } # Will contain current game state for convenience
        self.score = {idx: initial_score for idx in range(self.state['num_players'])}

        self.odd_player = None

    # A method that tells the instance to play the game
    def play(self, max_rounds=1000):
        if not self.players:
            print("No players added to the game!")
            return

        # Create the first round of tables by randomly pair player indices

        tables = [Table(players=pair, game=self) for pair in self.init_tables()]

        while self.state['round'] <= max_rounds:

            results = []
            new_tables = []

            while tables:
                # Each table must be processed, its result stored in history
                table = tables.pop()
                result = table.process(self.state, self.history)
                results.append(result)
                offerer = table.offerer_index
                responder = table.responder_index

                # Offer was rejected:
                if result['response'] == 'reject':
                    # See if either player is now untabled
                    players = [offerer, responder]
                    self.decrease_table_count(players)
                    for player in players:
                        if not self.state['table_count'][player]:
                            indices = [i for i in range(self.state['num_players']) if i not in players]
                            new_pair = [player, random.choice(indices)]
                            self.increase_table_count(new_pair)
                            new_tables.append(Table(players=new_pair, game=self))

                # Offer accepted or countered:
                else:
                    # Create a table with roles switched
                    new_tables.append(table.switch())

                    if result['response'] == 'accept':
                        # TODO add points
                        pass

            # End while tables -- wrap up the round
            new_tables.reverse()
            tables = new_tables

            # updates the history
            self.history.append(results)

            # Update the current game state
            self.state['round'] += 1

        # End tournament
        print("History of the game:")
        for i, round in enumerate(self.history):
            print("Round:", i + 1)
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


class Table():
    """Determines structure for a round of actions"""

    def __init__(self, players, game, offerer=None, pie=1):
        """Takes two players and runs a round
           If no offerer is specified, choose one randomly

           players is list of indices of players in game.players

           offerer = index of players which is the player
        """

        # Validate input
        if len(players) != 2:
            print("Table() didn't receive two players!")
            raise ValueError

        self.game = game
        # Get the class instances for the two players
        if offerer is not None:
            # Player class instances
            self.offerer = game.players[offerer]
            self.responder = game.players[players[0]] if game.players[players[0]] != self.offerer else game.players[players[1]]

            # Player indices
            self.offerer_index = offerer
            self.responder_index = players[0] if players[0] != offerer else players[1]
        else:
            indices = [0, 1]; random.shuffle(indices)
            self.offerer = game.players[indices[0]]
            self.responder = game.players[indices[1]]
            self.offerer_index = players[indices[0]]
            self.responder_index = players[indices[1]]

        # Set the offerer and responder or randomize if we don't have one
        self.pie = pie

        # TODO Update table count in game state
        # TODO Take in the indices of the players as well


    def create_record(self, offer, response):

        return {'offerer': self.offerer_index, 'responder': self.responder_index,
                    'offer': offer, 'response': response}

    def process(self, state, history):

        # Get actions and create record
        offer = self.offerer.offer(state, history, self.pie)
        response = self.responder.response(offer, state, history, self.pie)
        record = self.create_record(offer, response)
        return record

    def switch(self):
        return Table(players=[self.offerer_index, self.responder_index],
                    game=self.game, offerer=self.responder_index, pie=self.pie)


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
