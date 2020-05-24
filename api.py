import csv
import numpy as np
import matplotlib.pyplot as plt
import random
from constants import *
from copy import deepcopy
from dataclasses import dataclass
from inspect import signature
import pprint as pp

@dataclass
class GameConstants:
    discounts: int
    names: tuple
    odd_player: int

@dataclass
class Record:
    offerer: int
    responder: int
    players: tuple
    offer: float
    response: int
    discounts: tuple

@dataclass
class State:
    tables: dict
    num_players: int
    scores: tuple
    avg_score_per_round: tuple
    avg_score_per_offer: tuple
    table_count: tuple
    cumulative_tables: tuple
    round: int = 1

    # TODO implement post init constructor?
    # def __post_init__(self, num_players):
    #     self.avg_score_per_round = [0] * num_players
    #     self.avg_score_per_offer = [0] * num_players
    #     self.table_count = [0] * num_players
    #     self.cumulative_tables = [0] * num_players
    def update_avg_scores(self):
        self.avg_score_per_round = [score / self.round for score in self.scores]
        self.avg_score_per_offer = [score / tot for (score, tot) in zip(self.scores, self.cumulative_tables)]

class ISPT():
    """Structure of the game"""
    __players = None
    __num_players = None
    __state = None
    __history = tuple()
    __discounts = None
    __names = None
    __odd_player = None


    def __init__(self, players, discounts=None, default_discount=0.9, initial_score=0):
        # Validate input
        num_players = len(players)
        if num_players < 3:
            errmsg = "ISPT is defined for 3 or more players only"
            raise ValueError(errmsg)

        if discounts and len(discounts) != num_players:
            errmsg = "Length of discount list passed in does not equal number of players"
            raise ValueError(errmsg)

        # Todo: write function to check all players have the right attributes

        # Set game constants
        self.players = players
        ISPT.__players = players

        self.names = self.set_player_names(players)
        ISPT.__names = self.names

        self.discounts = tuple(discounts) if discounts is not None else ((default_discount,) * num_players)
        ISPT.__discounts = self.discounts

        self.odd_player = None
        ISPT.__odd_player = self.odd_player

        self.state = State(tables = {}, # TODO should this just be a Table object? # this would fix get_past_tables
                        num_players = num_players,
                        round = 0,
                        scores = (initial_score,) * num_players,
                        avg_score_per_round = (0,) * num_players,
                        avg_score_per_offer = (0,) * num_players,
                        table_count = (0,) * num_players,
                        cumulative_tables = (0,) * num_players # total number of tables each player has participated in
                     )
        ISPT.__state = self.state

        self.history = tuple()
        ISPT.history = tuple()

        for player in players:
            player.game = self

    # Various getters
    @classmethod
    def get_history(cls):
        return cls.__history

    @classmethod
    def get_state(cls):
        return cls.__state

    @classmethod
    def get_names(cls):
        return cls.__names

    @classmethod
    def get_discounts(cls):
        return cls.__discounts

    @classmethod
    def get_odd_player(cls):
        return cls.__odd_player

    @classmethod
    def round(cls):
        return cls.__state.round

    def get_past_offers(self, players):
        # TODO: implement for single player, then for mutliple players
        '''players = list of player id's whose offers are desired.
           Returns a list of dictionaries. List element corresponds to round,'''

        result = []
        raise NotImplementedError

    def get_past_tables(self, player):
        return [t for round in self.history for t in round.tables if player in t]

    def get_past_responses(self, player):
        return [round.tables[t]['response'] for round in self.history for t in round.tables if player == t[1]]

    def get_accepted_offers(self, player):
        return [round.tables[t]['offer'] for round in self.history for t in round.tables
                if player == t[1] and round.tables[t]['response'] == ACCEPT]

    def set_player_names(self, players):
        names = []
        ctr = 0 # suffix for unnamed players
        for i, player in enumerate(players):
            player.name = player.__class__.__name__ if not player.name else player.name

        for i, player in enumerate(players):
            if hasattr(player, 'name') and isinstance(player.name, str):

                name = player.name if player.name not in names else player.name + str(names.count(player.name))
                names.append(name)
                continue
            # No name passed in
            names.append("player" + str(ctr))
            # self.names[i] = "player" + str(ctr)
            ctr += 1
        return names

    def award_points(self, players, discounts, offer):
        """ Players = (offerer_index, responder_index)"""
        splits = (1 - offer, offer)
        scores = list(self.state.scores)
        for i in range(2):
            scores[players[i]] += splits[i] * discounts[i]

        self.state.scores = tuple(scores)
        return

    # Play the tournament
    def play(self, max_rounds=1000, response_noise=0.01, export_csv=False):
        print("@@@@@@@@@@ THE ISPT @@@@@@@@@@@")
        tables = self.init_tables()

        while self.state.round < max_rounds:
            results = []; new_tables = []

            self.state.round += 1
            while tables:
                # Play each table & record the results in history
                table = tables.pop(0)
                result = table.process()
                # TODO Get all this out of the return value in result instead?
                players = table.players
                discounts = table.discounts

                # Remove table discounts from tables game information
                del self.state.tables[players]

                # Check for random noise case
                if random.random() < response_noise:
                    false_responses = {0, 1, 2} - {result.response}
                    result.response = random.choice(list(false_responses))

                results.append(result)

                # Determine scoring and next round tabling
                if result.response == REJECT:
                    # Re-match any untabled players. Otherwise, do nothing
                    # TODO should untabled player check happen only at end of round?
                    for i, player in enumerate(players):
                        if not self.state.table_count[player]:
                            # TODO factor this out into a function?
                            new_opponent = random.choice([j for j in range(self.state.num_players) if j not in players])
                            new_pair = player, new_opponent

                            # Apply discount
                            new_discounts = (discounts[i] * self.discounts[player], 1)
                            new_tables.append(Table(players=new_pair, game=self, current_discounts=new_discounts))

                # Offer accepted or countered:
                else:
                    if result.response == ACCEPT:

                        self.award_points(players, discounts, result.offer)
                        new_discounts = (1, 1)
                    else: # Counteroffer    note: tuple wrapper needed since Python does not have tuple comprehension
                        new_discounts = tuple(discounts[i] * self.discounts[players[i]] for i in range(2))

                    # Either case: create table with player roles switched, appropriate discounts
                    new_tables.append(table.switch_players(discounts=new_discounts))

            # Update game information
            tables = new_tables

            # for table in tables:
            #     print("Players:", table.players, "Discounts:", table.discounts)


            # Update round
            self.state.update_avg_scores()
            ISPT.__state = self.state

            # Prepare history object
            result_obj = deepcopy(self.state)

            # TODO should 'current discoutns' be a Table object?
            result_obj.tables = {record.players: {'offer': record.offer,
                                                             'response': record.response,
                                                             'discounts': record.discounts}
                                            for record in results}

            self.history = tuple(list(self.history) + [result_obj])
            ISPT.__history = self.history

            # Run checks
            # self.check_tables()
            # self.check_discounts()

            # End of round



        # print("History of game:")
        # pp.pprint(self.history)
        #
        # print("Final game state:")
        # pp.pprint(self.state)

        if export_csv:
            self.export_data()

        return self.history

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
        table_counts = list(self.state.table_count)
        cumulative_tables = list(self.state.cumulative_tables)
        for p in players:
            table_counts[p] += 1
            cumulative_tables[p] += 1

        self.state.table_count = tuple(table_counts)
        self.state.cumulative_tables = tuple(cumulative_tables)
        return

    def decrease_table_count(self, players):
        table_counts = list(self.state.table_count)
        for p in players:
            table_counts[p] -= 1

        self.state.table_count = tuple(table_counts)
        return

    def graph_scores(self):
        x = range(self.state.round + 1)
        fig, axs = plt.subplots(2, 2)

        for i in range(self.state.num_players):
            a = [rnd.scores[i] for rnd in self.history]
            b = [rnd.avg_score_per_round[i] for rnd in self.history]
            c = [rnd.avg_score_per_offer[i] for rnd in self.history]
            axs[0, 0].plot(x, a, label=str(i))
            axs[0, 0].set_title('Score')
            axs[0, 1].plot(x, b)
            axs[0, 1].set_title('Average Score per Round')
            axs[1, 0].plot(x, c)
            axs[1, 0].set_title('Average Score per Offer')
            axs[1, 1].axis('off')

        fig.legend(loc='lower right')
        plt.grid()
        plt.savefig('data/graphs.png')
        plt.show()

    def export_data(self):
        """export a CSV file for each player where rows are rounds and columns are
        tables? Also a master sheet for overall scores, avg score per round?"""

        """Create an animated graph of tables & offers?"""

        with open('data/tables.csv', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file,
                fieldnames=['round', 'offerer', 'responder', 'offer', 'response', 'discounts'])

            writer.writeheader()
            for round in self.history:
                for table in round.tables:
                    result = round.tables[table]
                    row = {k: result[k] for k in result}
                    row['offerer'], row['responder'] = table
                    row['round'] = round.round
                    writer.writerow(row)


        columns = list(State.__dataclass_fields__.keys())
        columns.remove('tables')
        with open('data/stats.csv', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columns)

            writer.writeheader()
            for round in self.history:
                writer.writerow({col: round.__dict__[col] for col in columns})

    # Checks
    def check_discounts(self, verbose=False):
        no_problems = True
        for record in self.history[-1]:
            players = (record.responder, record.offerer)
            if record.response == 'accept':
                # THere should be a table with roles reverse and discounts [1, 1]
                if not players in self.state.tables:
                    no_problems = False
                    print("Table resulting from accept not found", players)
                    continue
                if self.state.tables[players] != [1, 1]:
                    no_problems = False
                    print("result of accept offer did not result in reset discounts", players)
                    continue

            if record.response == 'counter':
                # There should be a table with roles reversed and discounts applied
                if not players in self.state.tables:
                    no_problems = False
                    print("Table resulting from counter not found", players)
                    continue
                # get them discounts
                offerer_discount = record.discounts[0] * self.discounts[players[1]]
                responder_discount = record.discounts[1] * self.discounts[players[0]]
                if self.state.tables[players] != [responder_discount, offerer_discount]:
                    no_problems = False
                    print("Table resulting from counter has wrong discounts", players)
                    continue

            if record.response == 'reject':
                # There should be a table with this player with discount and 1
                for i in range(2):
                    tables = [table for table in self.state.tables if players[i] in table]

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
                    p_discount = record.discounts[(i + 1) % 2] * self.discounts[players[i]]
                    if self.state.tables[the_table] not in [[1, p_discount], [p_discount, 1]]:
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
                if not players in self.state.tables:
                    no_problems = False
                    print("players", players, "don't have a correct table")

                continue
            else:
                # Make sure the players are not tabled together
                if players in self.state.tables:
                    no_problems = False
                    print("response was reject but players", players, "are tabled together")

                # make sure both players have a table
                p0_table_count = [1 for pair in self.state.tables if players[0] in pair]
                p1_table_count = [1 for pair in self.state.tables if players[1] in pair]

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

    def __init__(self, players, game, offerer=False, current_discounts=(1, 1)):
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
        self.discounts = current_discounts
        self.game = game

        # Update the game information re this table's discounts
        self.game.state.tables[self.players] = self.discounts
        self.game.increase_table_count(players)

    # Is a record just a table with the offer filled in?
    def create_record(self, offer, response):
        return Record(offerer=self.offerer, responder=self.responder,
                        players=self.players, offer=offer, response=response,
                        discounts=self.game.state.tables[self.players])

    def process(self):
        '''Gets each players' action, decreases the table count (since this table
           will be discarded) and returns the record for game history'''

        # TODO make offer and response methods somehow private, so agents can't
        offer = self.game.players[self.offerer].offer(self)
        if offer is None:
            print('none offer from player:')
            print(self.game.players[self.offerer].__class__.__name__)
        response = self.game.players[self.responder].response(self, offer)
        self.game.decrease_table_count(self.players)
        return self.create_record(offer, response)

    def switch_players(self, discounts):
        return Table(players=(self.responder, self.offerer), game=self.game, offerer=True,
                     current_discounts=(discounts[1], discounts[0]))






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
