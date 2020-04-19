import csv
import numpy as np
import matplotlib.pyplot as plt
import random
from copy import deepcopy
from dataclasses import dataclass
from inspect import signature
import pprint as pp

# TODO replace offerer & responder with players tuple?
@dataclass
class Record:
    offerer: int
    responder: int
    offer: float
    response: str # TODO make this an enum?
    discounts: list

@dataclass
class State:
    current_discounts: dict # TODO rename table discounts?
    discounts: list
    num_players: int
    odd_player: int
    scores: list
    avg_score_per_round: list
    avg_score_per_offer: list
    table_count: list
    total_tables: list
    round: int = 1

    # TODO implement post init constructor?
    # def __post_init__(self, num_players):
    #     self.avg_score_per_round = [0] * num_players
    #     self.avg_score_per_offer = [0] * num_players
    #     self.table_count = [0] * num_players
    #     self.total_tables = [0] * num_players
    def update_avg_scores(self):
        self.avg_score_per_round = [score / self.round for score in self.scores]
        self.avg_score_per_offer = [score / tot for (score, tot) in zip(self.scores, self.total_tables)]

class ISPT():
    """Structure of the game"""

    def __init__(self, players, discounts=None, default_discount=0.9, initial_score=0):
        # Validate input
        num_players = len(players)
        if num_players < 3:
            errmsg = "ISPT is defined for 3 or more players only"
            raise ValueError(errmsg)

        if discounts and len(discounts) != num_players:
            errmsg = "Length of discount list passed in does not equal number of players"
            raise ValueError(errmsg)

        self.players = players
        self.history = []
        self.states = [] # TODO fold this into history?
        self.state = State(current_discounts = {}, # TODO rename table discounts?
                        discounts = discounts if discounts is not None else [default_discount] * num_players,
                        num_players = num_players,
                        odd_player = None,
                        round = 1,
                        scores = [initial_score] * num_players,
                        avg_score_per_round = [0] * num_players,
                        avg_score_per_offer = [0] * num_players,
                        table_count = [0] * num_players,
                        total_tables = [0] * num_players # total number of tables each player has participated in
                     )
        self.odd_player = None

    def award_points(self, players, discounts, offer):
        """ Players = (offerer_index, responder_index)
        """
        splits = (1 - offer, offer)
        for i in range(2):
            self.state.scores[players[i]] += splits[i] * discounts[i]
        return

    # Play the tournament
    def play(self, max_rounds=1000, export_csv=False):
        print("@@@@@@@@@@ THE ISPT @@@@@@@@@@@")

        # Create the first round of tables by randomly pair player indices
        tables = self.init_tables()
        while self.state.round < max_rounds:
            print("<><><> Round", self.state.round, "<><><>")
            results = []; new_tables = []
            while tables:
                # Play each table & record the results in history
                table = tables.pop(0)
                result = table.process()
                results.append(result)

                # Determine scoring and next round tabling for players based on response
                players = table.players
                discounts = table.discounts

                # Remove table discounts from current_discounts game information
                del self.state.current_discounts[players]

                # Offer was rejected:
                if result.response == 'reject':
                    # Re-match any untabled players. Otherwise, do nothing
                    for i, player in enumerate(players):
                        if not self.state.table_count[player]:
                            # TODO factor this out into a function?
                            new_opponent = random.choice([j for j in range(self.state.num_players) if j not in players])
                            new_pair = [player, new_opponent]

                            # Apply discount
                            new_discounts = [discounts[i] * self.state.discounts[player], 1]
                            new_tables.append(Table(players=new_pair, game=self, current_discounts=new_discounts))

                # Offer accepted or countered:
                else:
                    if result.response == 'accept':
                        self.award_points(players, discounts, result.offer)
                        new_discounts = [1, 1]
                    else: # Counteroffer
                        new_discounts = [discounts[i] * self.state.discounts[players[i]] for i in range(2)]

                    # Either case: create table with player roles switched, appropriate discounts
                    new_tables.append(table.switch_players(discounts=new_discounts))

            # End while tables -- wrap up the round

            # Update game information
            tables = new_tables
            self.history.append(results)
            for result in results:
                print(result)

            # Run checks
            # self.check_tables()
            # self.check_discounts()

            # Update round
            self.state.update_avg_scores()
            snapshot = deepcopy(self.state)
            self.states.append(snapshot)
            self.state.round += 1

        print("Final game state:")
        pp.pprint(self.state)

        print("final game history:")
        for i, s in enumerate(self.states):
            print("round:", i)
            print(s.scores)

        self.graph_scores()
        if export_csv:
            self.export_data()
        return

    def init_tables(self):
        pairs = []
        indices = {i for i in range(self.state.num_players)}

        # If we have an odd number of players
        if self.state.num_players % 2:
            # Create a second table with a randomly chosen player
            pair = random.sample(indices, 2)
            self.state.odd_player = pair[1]
            indices -= {pair[0]}
            pairs.append(pair)

        # Now we're guaranteed to have an even number of players
        while indices:
            pair = random.sample(indices, 2)
            indices -= set(pair)
            pairs.append(pair)

        return [Table(players=pair, game=self) for pair in pairs]

    def increase_table_count(self, players):
        for p in players:
            self.state.table_count[p] += 1
            self.state.total_tables[p] += 1
        return

    def decrease_table_count(self, players):
        for p in players:
            self.state.table_count[p] -= 1
        return

    def graph_scores(self):
        # x axis is the rounds
        x = range(self.state.round - 1)
        fig, axs = plt.subplots(2, 2)

        for i in range(self.state.num_players):
            a = [rnd.scores[i] for rnd in self.states]
            b = [rnd.avg_score_per_round[i] for rnd in self.states]
            c = [rnd.avg_score_per_offer[i] for rnd in self.states]
            axs[0, 0].plot(x, a, label=str(i))
            axs[0, 0].set_title('Score')
            axs[0, 1].plot(x, b)
            axs[0, 1].set_title('Average Score per Round')
            axs[1, 0].plot(x, c)
            axs[1, 0].set_title('Average Score per Offer')
            axs[1, 1].axis('off')

        fig.legend(loc='lower right')
        plt.grid()
        plt.show()
        # plot a line for each player score in the game

        # repeat for average score per round

        # repeat for average score per offer
    # TODO
    def export_data(self):
        """export a CSV file for each player where rows are rounds and columns are
        tables? Also a master sheet for overall scores, avg score per round?"""

        """Create an animated graph of tables & offers?"""
        record = self.history[-1][-1]
        fieldnames = [a for a in dir(record) if not a.startswith('__')]

        with open('game.csv', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for round in self.history:
                for record in round:
                    writer.writerow({k: v for (k, v) in record.__dict__.items()})


    # Checks
    def check_discounts(self, verbose=False):
        no_problems = True
        for record in self.history[-1]:
            players = (record.responder, record.offerer)
            if record.response == 'accept':
                # THere should be a table with roles reverse and discounts [1, 1]
                if not players in self.state.current_discounts:
                    no_problems = False
                    print("Table resulting from accept not found", players)
                    continue
                if self.state.current_discounts[players] != [1, 1]:
                    no_problems = False
                    print("result of accept offer did not result in reset discounts", players)
                    continue

            if record.response == 'counter':
                # There should be a table with roles reversed and discounts applied
                if not players in self.state.current_discounts:
                    no_problems = False
                    print("Table resulting from counter not found", players)
                    continue
                # get them discounts
                offerer_discount = record.discounts[0] * self.state.discounts[players[1]]
                responder_discount = record.discounts[1] * self.state.discounts[players[0]]
                if self.state.current_discounts[players] != [responder_discount, offerer_discount]:
                    no_problems = False
                    print("Table resulting from counter has wrong discounts", players)
                    continue

            if record.response == 'reject':
                # There should be a table with this player with discount and 1
                for i in range(2):
                    tables = [table for table in self.state.current_discounts if players[i] in table]

                    if not tables:
                        no_problems = False
                        print("Player has no tables:", players[i])
                        continue

                    if len(tables) > 1 and verbose:
                        print("player has more than 1 table and no new table would have been created")
                        continue

                    # Check if each table is not result of previous round then discounts should be determined
                    old_tables = [(r.offerer, r.responder) for r in self.history[-1]]

                    old_tables_with_player = [t for t in old_tables if players[i] in t]

                    if len(old_tables_with_player) > 1 and verbose:
                        print("last round player had", len(old_tables_with_player), "tables and no new table would have been created")
                        continue

                    # Else there the player has exactly one table and its discounts are determined
                    the_table = tables[0]
                    p_discount = record.discounts[(i + 1) % 2] * self.state.discounts[players[i]]
                    if self.state.current_discounts[the_table] not in [[1, p_discount], [p_discount, 1]]:
                        no_problems = False
                        print("Didn't find a table with the right discounts for player", players[i])

        if no_problems and verbose:
            print("No problems found in round", self.state.round)
        return

    def check_tables(self, verbose=False):
        # Get most recent round of tables
        no_problems = True
        for record in self.history[-1]:
            # was the result of the previous round an accept or counteroffer?
            # print("Checking result of table (", record.offerer, ",", record.responder, "):")
            players = (record.responder, record.offerer)
            if record.response in ['counter', 'accept']:
                # there should be a table with player roles reversed
                if not players in self.state.current_discounts:
                    no_problems = False
                    print("players", players, "don't have a correct table")

                continue
            else:
                # Make sure the players are not tabled together
                if players in self.state.current_discounts:
                    no_problems = False
                    print("response was reject but players", players, "are tabled together")

                # make sure both players have a table
                p0_table_count = [1 for pair in self.state.current_discounts if players[0] in pair]
                p1_table_count = [1 for pair in self.state.current_discounts if players[1] in pair]

                if not p0_table_count:
                    no_problems = False
                    print("Player 0 is untabled")
                if not p1_table_count:
                    no_problems = False
                    print("Player 1 is untabled")
                continue

        if no_problems and verbose:
            print("All good on round:", self.state.round)


class Table():
    """Determines structure for a round of actions"""

    def __init__(self, players, game, offerer=False, current_discounts=[1, 1]):
        """Takes two players and runs a round
           If offerer = True, player[0] is offerer
           If offerer = False, shuffle the players and 0th player is offerer

           players is list of indices of players in game.players

           offerer = index of players which is the player
        """

        # Get the offerer and responder
        # TODO does this still work if players is a tuple? If so, make it a tuple everywhere Table() is instantiated
        if not offerer:
            p = list(zip(players, current_discounts))
            random.shuffle(p)
            players, current_discounts = zip(*p)

        # Set agent class instances and indices
        self.offerer = players[0]
        self.responder = players[1] # TODO If I just make players a named tuple can I ditch these two properties?
        self.players = tuple(players)
        self.discounts = list(current_discounts)
        self.game = game

        # Update the game information re this table's discounts
        self.game.state.current_discounts[tuple(players)] = self.discounts

        self.game.increase_table_count(players)

    def create_record(self, offer, response):
        return Record(offerer=self.offerer, responder=self.responder, offer=offer, response=response,
                        discounts=self.game.state.current_discounts[self.players])

    def process(self):
        '''Gets each players' action, decreases the table count (since this table
           will be discarded) and returns the record for game history'''

        offer = self.game.players[self.offerer].offer(self.players, self.game.state, self.game.history)
        response = self.game.players[self.responder].response(self.players, offer, self.game.state, self.game.history)
        self.game.decrease_table_count(self.players)
        return self.create_record(offer, response)

        # TODO should discounts be tuples? Do they ever get mutated or just discarded?
    def switch_players(self, discounts=[1, 1]):
        discounts.reverse() # We reverse here so when method is called, discounts still match indexing of players
        return Table(players=[self.responder, self.offerer],
                    game=self.game,
                    offerer=True,
                    current_discounts=discounts)


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

    def offer(self, opponent, state, history, pie):
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
    def response(self, opponent, offer, state, history, pie):
                print("Agent's response as been called.")

                # start off by always accepting
                return self.actions[0]
                # Given an offer and the history, how would I respond?

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
