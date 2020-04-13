import random
from inspect import signature
import pprint as pp



class ISPT():
    """Structure of the game"""

    def __init__(self, players, discounts=None, default_discount=0.9, initial_score=0):
        """
        Attempting to refer to players by index rather than memory location unless
        player's methods are needed

        """

        # Validate input
        num_players = len(players)
        if num_players < 3:
            errmsg = "ISPT is defined for 3 or more players only"
            raise ValueError(errmsg)

        if discounts and len(discounts) != num_players:
            errmsg = "Length of discount list passed in does not equal number of players"
            raise ValueError(errmsg)


        self.players = players

        # Maps player class instance to their index in self.players
        self.player_index = {player: i for i, player in enumerate(players)}

        # Initialize game information
        self.history = []
        self.state = {  'current_discount': [1] * num_players,
                        'discounts': discounts if discounts is not None else [default_discount] * num_players,
                        'num_players': num_players,
                        'odd_player': None,
                        'round': 1,
                        'scores': [initial_score] * num_players,
                        'table_count': [0] * num_players
                     } # Will contain current game state for convenience

        self.odd_player = None

    def award_points(self, players, offer):
        """ Players = [offerer_index, responder_index]
        """
        splits = (1 - offer, offer)
        for split, player in zip(splits, players):
            points = split * self.state['current_discount'][player]
            self.state['scores'][player] += points

            # Reset discount factor
            self.state['current_discount'][player] = 1
        return

    # Plays the tournament
    def play(self, max_rounds=1000):

        # Create the first round of tables by randomly pair player indices
        tables = [Table(players=pair, game=self) for pair in self.init_tables()]

        while self.state['round'] <= max_rounds:

            results = []
            new_tables = []

            while tables:
                # Play each table & record the results in history
                table = tables.pop()
                result = table.process(self.state, self.history)
                results.append(result)

                # Determine scoring and next round tabling for players based on response
                offerer = table.offerer_index
                responder = table.responder_index
                players = [offerer, responder]

                # Offer was rejected:
                if result['response'] == 'reject':
                    # See if either player is now untabled
                    self.decrease_table_count(players)
                    for player in players:
                        if not self.state['table_count'][player]:
                            indices = [i for i in range(self.state['num_players']) if i not in players]
                            new_pair = [player, random.choice(indices)]
                            self.increase_table_count(new_pair)
                            new_tables.append(Table(players=new_pair, game=self))

                        # Apply discount factor
                        self.state['current_discount'][player] *= self.state['discounts'][player]


                # Offer accepted or countered:
                else:
                    # Create a table with roles switched
                    new_tables.append(table.switch())

                    if result['response'] == 'accept':
                        self.award_points(players, result['offer'])
                        # Allocate points

                    else:
                        # Apply discount factor
                        for player in players:
                            self.state['current_discount'][player] *= self.state['discounts'][player]

            # End while tables -- wrap up the round
            new_tables.reverse()
            tables = new_tables

            print("RESULTS:")
            pp.pprint(results)
            print("SCORES:", self.state['scores'])
            print("CURRENT DISCOUNTS:", self.state['current_discount'])
            # Update game information
            self.history.append(results)
            self.state['round'] += 1

        # TODO: save output to csv
        return

    def init_tables(self):
        pairs = []
        indices = {i for i in range(self.state['num_players'])}

        # If we have an odd number of players
        if self.state['num_players'] % 2:
            # Create a second table with a randomly chosen player
            pair = random.sample(indices, 2)
            self.state['odd_player'] = pair[1]
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
