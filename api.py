import csv
import numpy as np
import matplotlib.pyplot as plt
import random
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib_chord import chordDiagram


from constants import *
from copy import deepcopy
from dataclasses import dataclass
from inspect import signature
import pprint as pp

sns.set(style='darkgrid')

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

    def asdict(self):
        return {'offerer': self.offerer,
                'responder': self.responder,
                'offer': self.offer,
                'response': self.response,
                'discounts': self.discounts}
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
        ISPT.__num_players = len(players)
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
    def get_history(cls, players=[]):
        if not players:
            return cls.__history

        results = []
        for round in cls.__history:
            results.append([t for t in round.tables if t.offerer in players or t.responder in players])

        return results

    @classmethod
    def get_state(cls):
        return cls.__state

    @classmethod
    def num_players(cls):
        return cls.__num_players

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

    def get_past_offers(self, player):
        '''Player = id of player whose past offers we want to get
           Returns a list of lists, corresponding to the records in which
           the player was an offerer in each round'''

        results = []
        for round in cls.__history:
            results.append([t for t in round.tables if t.offerer == player])
        return results

    def get_past_responses(self, player):
        results = []
        for round in cls.__history:
            results.append([t for t in round.tables if t.responder == player])
        return results

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
        self.state.tables = tuple([t.data for t in tables])

        while self.state.round < max_rounds:
            results = []; new_tables = []
            self.state.round += 1

            while tables:
                # Play each table & record the results in history
                table = tables.pop(0)
                result = table.process()

                # TODO Get all this out of the return value in result instead?
                players = result.players
                discounts = result.discounts

                # Check for random noise case
                # TODO factor this out?
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

            # Update round
            self.state.update_avg_scores()
            ISPT.__state = self.state

            # Prepare history object
            result_obj = deepcopy(self.state)
            result_obj.tables = tuple(results)

            self.history = tuple(list(self.history) + [result_obj])
            ISPT.__history = self.history
            # End of round

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
        # table_counts = list(self.state.table_count)
        # cumulative_tables = list(self.state.cumulative_tables)

        table_counts = list(ISPT.__state.table_count)
        cumulative_tables = list(ISPT.__state.cumulative_tables)

        for p in players:
            table_counts[p] += 1
            cumulative_tables[p] += 1

        ISPT.__state.table_count = tuple(table_counts)
        ISPT.__state.cumulative_tables = tuple(cumulative_tables)
        return

    def decrease_table_count(self, players):
        # table_counts = list(self.state.table_count)
        table_counts = list(ISPT.__state.table_count)

        for p in players:
            table_counts[p] -= 1

        ISPT.__state.table_count = tuple(table_counts)
        return


    def graph_scores(self):
        x = range(ISPT.round())
        fig, axs = plt.subplots(2, 2)

        for i in range(ISPT.get_state().num_players):
            a = [rnd.scores[i] for rnd in ISPT.get_history()]
            b = [rnd.avg_score_per_round[i] for rnd in ISPT.get_history()]
            c = [rnd.avg_score_per_offer[i] for rnd in ISPT.get_history()]

            axs[0, 0].plot(x, a, label=str(i))
            axs[0, 0].set_title('Score')
            axs[0, 1].plot(x, b)
            axs[0, 1].set_title('Average Score per Round')
            axs[1, 0].plot(x, c)
            axs[1, 0].set_title('Average Score per Offer')
            axs[1, 1].axis('off')

        fig.legend(labels=ISPT.get_names(), loc='lower right')
        plt.grid()
        plt.savefig('data/graphs.png')


        plt.show()

    def sb(self):
        fig, axs = plt.subplots(2, 2)


        names = ISPT.get_names()
        history = ISPT.get_history()
        # TODO figure out how to make these attributes accessed programmatically

        # Total score
        plots = []
        data = {name: [rnd.scores[names.index(name)] for rnd in history] for name in names}
        df = pd.DataFrame(data)
        plots += [sns.lineplot(data=df, dashes = False, ax=axs[0,0])]
        # g1.get_legend().remove()

        data = {name: [rnd.avg_score_per_offer[names.index(name)] for rnd in history] for name in names}
        df = pd.DataFrame(data)
        plots += [sns.lineplot(data=df, dashes=False, ax=axs[0,1])]

        data = {name: [rnd.avg_score_per_round[names.index(name)] for rnd in history] for name in names}
        df = pd.DataFrame(data)
        plots += [sns.lineplot(data=df, dashes = False, ax=axs[1,0])]

        for plot in plots:
            plot.get_legend().remove()

        axs[1, 1].axis('off')
        fig.legend(labels=ISPT.get_names(), loc='lower right')
        plt.show()


    def export_data(self):
        """Export a CSV file for each player where rows are rounds and columns are
        tables? Also a master sheet for overall scores, avg score per round?"""

        with open('data/tables.csv', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file,
                fieldnames=['round', 'offerer', 'responder', 'offer', 'response', 'discounts'])

            writer.writeheader()

            hist = ISPT.__history
            for round in ISPT.__history:
                for table in round.tables:
                    row = table.asdict()
                    row['round'] = round.round
                    writer.writerow(row)

        columns = list(State.__dataclass_fields__.keys())
        columns.remove('tables')
        with open('data/stats.csv', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columns)

            writer.writeheader()
            for round in self.history:
                writer.writerow({col: round.__dict__[col] for col in columns})


class Table():
    """Determines structure for a round of actions"""

    def __init__(self, players, game, offerer=False, current_discounts=(1, 1)):
        """    """

        # Get the offerer and responder
        # TODO does this still work if players is a tuple? If so, make it a tuple everywhere Table() is instantiated
        if not offerer:
            p = list(zip(players, current_discounts))
            random.shuffle(p)
            players, current_discounts = zip(*p)

        self.data = Record(offerer = players[0],
                           responder = players[1],
                           players = tuple(players),
                           offer = None,
                           response = None,
                           discounts = current_discounts)
        self.game = game
        self.game.increase_table_count(players)

    # Is a record just a table with the offer filled in?
    def create_record(self, offer, response):
        return self.data

    def process(self):
        '''Gets each players' action, decreases the table count (since this table
           will be discarded) and returns the record for game history'''

        # TODO make offer and response methods somehow private, so agents can't
        offer = self.game.players[self.data.offerer].offer(self.data)
        if offer is None:
            print('none offer from player:')
            print(self.game.players[self.offerer].__class__.__name__)
        self.data.offer = offer
        self.data.response = self.game.players[self.data.responder].response(self.data, offer)
        self.game.decrease_table_count(self.data.players)
        return self.data

    def switch_players(self, discounts):
        return Table(players=(self.data.responder, self.data.offerer),
                     game=self.game,
                     offerer=True,
                     current_discounts=(discounts[1], discounts[0]))
