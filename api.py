import csv
import inspect
import numpy as np
import matplotlib.pyplot as plt
import random
import seaborn as sns
import pandas as pd
from constants import *
from copy import deepcopy
from dataclasses import dataclass
from inspect import signature
import pprint as pp

sns.set(style='darkgrid')


@dataclass
class GameConstants:
    discounts: int
    names: list
    odd_player: int


@dataclass
class TableRecord:
    offerer: int  # game id of player to make offer
    responder: int
    players: list  # [id1, id2]
    offer: float  # in [0, 1] range
    response: int  # [0 = accept, 1 = counter, 2 = reject]
    discounts: list  # [d1, d2]

    def asdict(self):
        return {
            'offerer': self.offerer,
            'responder': self.responder,
            'offer': self.offer,
            'response': self.response,
            'discounts': self.discounts
        }


@dataclass
class State:
    tables: list
    num_players: int
    scores: list
    avg_score_per_round: list
    avg_score_per_offer: list
    table_count: list
    cumulative_tables: list
    round: int = 1

    def update_avg_scores(self):
        self.avg_score_per_round = [
            score / self.round for score in self.scores
        ]
        self.avg_score_per_offer = [
            score / tot
            for (score, tot) in zip(self.scores, self.cumulative_tables)
        ]


class ISPT():
    """Structure of the game
       Data that should be available to agents is stored as class attributes and
       accessed via getters. Data that should never be accessed by agents is
       stored in the instance. This way, agents can call ISPT.some_getter()
       without 'knowing' where the game instance is, or accidentally mutating history.
    """
    __players = None
    __num_players = None
    __state = None
    __history = list()
    __discounts = None
    __names = None
    __odd_player = None
    __instance = None

    # max_rounds=1000, termination_prob=(100, 0.01), response_noise=0.01, export_csv=False
    def __init__(self,
                 players,
                 discounts=None,
                 default_discount=0.9,
                 info_availability=None,
                 initial_scores=None,
                 max_rounds=1000,
                 termination_prob=(100, 0.01),
                 response_noise=0.0,
                 export_csv=False):
        # Validate input
        num_players = len(players)
        ISPT.__num_players = len(players)
        if num_players < 3:
            errmsg = "ISPT is defined for 3 or more players only"
            raise ValueError(errmsg)

        if discounts and len(discounts) != num_players:
            errmsg = "Length of discount list passed in does not equal number of players"
            raise ValueError(errmsg)

        if initial_scores and len(initial_scores) != num_players:
            errmsg = "Length of intial_scores does not match number of players"
            raise ValueError(errmsg)

        # Set game parameters
        self.max_rounds = max_rounds
        self.termination_prob = termination_prob
        self.response_noise = response_noise
        self.export_csv = export_csv

        # Set initial game values
        self.players = players

        ISPT.__instance = self
        ISPT.__players = players
        ISPT.__names = self.set_player_names(players)
        ISPT.__discounts = discounts if discounts is not None else [
            default_discount
        ] * num_players
        ISPT.__odd_player = None
        ISPT.__info_availability = info_availability if info_availability is not None else {}
        ISPT.__state = State(tables=None,
                             num_players=num_players,
                             round=0,
                             scores=initial_scores if initial_scores else [0] *
                             num_players,
                             avg_score_per_round=[0] * num_players,
                             avg_score_per_offer=[0] * num_players,
                             table_count=[0] * num_players,
                             cumulative_tables=[0] * num_players)
        ISPT.history = list()

    # Various getters
    @classmethod
    def get_history(self, players=[]):
        '''History getter for agents.

           Returns a list of lists, the index of the parent list corresponds to the
           rounds of the game, then the child lists are the tables in which the
           specified players participated'''

        # Get set of players' history requested
        all_players = set(range(ISPT.__num_players))
        players_requested = set(players) if players else all_players

        # TODO: If game played with complete information then a lot of this is unnecessary
        #TODO factor this out
        # Get the index of the requester
        frame = inspect.stack()[1].frame  # The frame of the caller.
        instance = frame.f_locals['self']  # The caller's locals dict.
        requester = ISPT.__players.index(instance)

        # Remove from players list any players the requester doesn't have access to
        allowed = set(ISPT.__info_availability.get(requester, all_players))
        players = players_requested.intersection(allowed)
        results = []
        for round in ISPT.__history:
            results.append([
                t for t in round.tables
                if t.offerer in players or t.responder in players
            ])

        if not results:
            return [[]]  # so that get_history()[-1] still works
        return results

    @classmethod
    def get_state(cls):
        return cls.__state

    @classmethod
    def get_rankings(cls, stat='score'):
        stat_dict = {
            'score': ISPT.__state.scores,
            'avg_score_per_round': ISPT.__state.avg_score_per_round,
            'avg_score_per_offer': ISPT.__state.avg_score_per_offer
        }
        rankings = list(range(ISPT.num_players()))
        rankings.sort(key=lambda x: stat_dict[stat][x], reverse=True)
        return rankings

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
           Returns a list of lists, corresponding to the TableRecords in which
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
        return [
            t for round in self.history for t in round.tables if player in t
        ]

    def get_past_responses(self, player):
        return [
            round.tables[t]['response'] for round in self.history
            for t in round.tables if player == t[1]
        ]

    def get_accepted_offers(self, player):
        return [
            round.tables[t]['offer'] for round in self.history
            for t in round.tables
            if player == t[1] and round.tables[t]['response'] == ACCEPT
        ]

    def set_player_names(self, players):
        names = []
        ctr = 0  # suffix for unnamed players
        for i, player in enumerate(players):
            player.name = player.__class__.__name__ if not player.name else player.name

        for i, player in enumerate(players):
            if hasattr(player, 'name') and isinstance(player.name, str):

                name = player.name if player.name not in names else player.name + str(
                    names.count(player.name))
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
        scores = list(ISPT.__state.scores)
        for i in range(2):
            scores[players[i]] += splits[i] * discounts[i]

        ISPT.__state.scores = scores
        return

    # Play the tournament
    def play(self):
        '''termination_prob = [round, probability]: each round after the round
            given in this list the game randomly terminates with the given
            probability. Note that after max_rounds, the game terminates regardless.
        '''
        print("@@@@@@@@@@ THE ISPT @@@@@@@@@@@")

        tables = self.init_tables()
        ISPT.__state.tables = [t.record for t in tables]

        while ISPT.__state.round < self.max_rounds:
            results = []
            new_tables = []
            ISPT.__state.round += 1

            # Test for random termination
            # TODO come up with better name for random termination params
            if ISPT.__state.round > self.termination_prob[0] and random.random(
            ) < self.termination_prob[1]:
                break

            while tables:
                # Play each table & record the results in history
                table = tables.pop(0)
                result = table.process()
                players = result.players
                discounts = result.discounts

                # Check for random noise case
                if random.random() < self.response_noise:
                    false_responses = {0, 1, 2} - {result.response}
                    result.response = random.choice(false_responses)

                results.append(result)

                # Determine scoring and next round tabling
                if result.response == REJECT:
                    # Re-match any untabled players. Otherwise, do nothing
                    # TODO should untabled player check happen only at end of round?
                    for i, player in enumerate(players):
                        if not ISPT.__state.table_count[player]:
                            new_opponent = random.choice([
                                j for j in range(ISPT.__state.num_players)
                                if j not in players
                            ])
                            new_pair = player, new_opponent

                            # Apply discount
                            new_discounts = (discounts[i] *
                                             ISPT.__discounts[player], 1)
                            new_tables.append(
                                Table(players=new_pair,
                                      game=self,
                                      current_discounts=new_discounts))

                # Offer accepted or countered:
                else:
                    if result.response == ACCEPT:
                        self.award_points(players, discounts, result.offer)
                        new_discounts = [1, 1]
                    else:  # Counteroffer    note: tuple wrapper needed since Python does not have tuple comprehension
                        new_discounts = [
                            discounts[i] * ISPT.__discounts[players[i]]
                            for i in range(2)
                        ]

                    # Either case: create table with player roles switched, appropriate discounts
                    new_tables.append(
                        table.switch_players(discounts=new_discounts))

            # Update game information
            tables = new_tables

            # Update round
            ISPT.__state.update_avg_scores()

            # Prepare history object
            result_obj = deepcopy(ISPT.__state)  # Is this line necessary?
            result_obj.tables = results
            ISPT.__history.append(result_obj)
            # End of round

        if self.export_csv:
            self.export_data()

        return ISPT.__history

    def init_tables(self):
        pairs = []
        indices = {i for i in range(ISPT.__state.num_players)}

        # If we have an odd number of players
        if ISPT.__state.num_players % 2:
            # Create a second table with a randomly chosen player
            pair = random.sample(indices, 2)
            ISPT.__odd_player = pair[1]
            indices -= {pair[0]}
            pairs.append(pair)

        # Now we're guaranteed to have an even number of players
        while indices:
            pair = random.sample(indices, 2)
            indices -= set(pair)
            pairs.append(pair)

        return [Table(players=pair, game=self) for pair in pairs]

    def increase_table_count(self, players):
        table_counts = ISPT.__state.table_count
        cumulative_tables = ISPT.__state.cumulative_tables

        for p in players:
            table_counts[p] += 1
            cumulative_tables[p] += 1

        ISPT.__state.table_count = table_counts
        ISPT.__state.cumulative_tables = cumulative_tables
        return

    def decrease_table_count(self, players):
        # table_counts = list(self.state.table_count)
        table_counts = ISPT.__state.table_count

        for p in players:
            table_counts[p] -= 1

        ISPT.__state.table_count = table_counts
        return

    def graph_scores(self):
        # x = range(ISPT.round())
        x = range(ISPT.round())
        fig, axs = plt.subplots(2, 2)

        for i in range(ISPT.get_state().num_players):
            a = [rnd.scores[i] for rnd in ISPT.__history]
            b = [rnd.avg_score_per_round[i] for rnd in ISPT.__history]
            c = [rnd.avg_score_per_offer[i] for rnd in ISPT.__history]

            # print("vars:\n", ISPT.round(), len(a))
            axs[0, 0].plot(x, a, label=str(i))
            axs[0, 0].set_title('Score')
            axs[0, 1].plot(x, b)
            axs[0, 1].set_title('Average Score per Round')
            axs[1, 0].plot(x, c)
            axs[1, 0].set_title('Average Score per Offer')
            axs[1, 1].axis('off')

        fig.legend(labels=ISPT.get_names(),
                   loc='lower right',
                   bbox_to_anchor=(0.91, 0.1))
        fig.set_size_inches(11, 8.5)
        plt.grid()
        plt.savefig('data/graphs.png')

    def sb(self):
        fig, axs = plt.subplots(2, 2)
        names = ISPT.get_names()
        history = ISPT.__history

        # Total score
        plots = []
        data = {
            name: [rnd.scores[names.index(name)] for rnd in history]
            for name in names
        }
        df = pd.DataFrame(data)
        plots += [sns.lineplot(data=df, dashes=False, ax=axs[0, 0])]

        data = {
            name:
            [rnd.avg_score_per_offer[names.index(name)] for rnd in history]
            for name in names
        }
        df = pd.DataFrame(data)
        plots += [sns.lineplot(data=df, dashes=False, ax=axs[0, 1])]

        data = {
            name:
            [rnd.avg_score_per_round[names.index(name)] for rnd in history]
            for name in names
        }
        df = pd.DataFrame(data)
        plots += [sns.lineplot(data=df, dashes=False, ax=axs[1, 0])]

        for plot in plots:
            plot.get_legend().remove()

        axs[1, 1].axis('off')
        fig.legend(labels=ISPT.get_names(), loc='lower right')
        plt.show()

    def heatmap(self):
        plt.clf()
        score_matrix = np.zeros((ISPT.__num_players, ISPT.__num_players))
        for round in ISPT.__history:
            for table in round.tables:
                if table.response == ACCEPT:
                    points_offerer = table.discounts[0] * (1 - table.offer)
                    points_responder = table.discounts[1] * table.offer
                    score_matrix[table.offerer,
                                 table.responder] += points_offerer
                    score_matrix[table.responder,
                                 table.offerer] += points_responder

        score_df = pd.DataFrame(score_matrix)
        score_df.columns, score_df.index = ISPT.__names, ISPT.__names
        ax = sns.heatmap(score_df, linewidths=0.5, annot=True, cmap="YlGn")

        # Replace diagonal with player name
        for i, name in zip(range(ISPT.__num_players), ISPT.__names):
            ax.texts[i * ISPT.__num_players + i]._text = name

        plt.savefig('data/heatmap.png')
        # plt.show()

    def export_data(self):
        with open('data/tables.csv', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file,
                                    fieldnames=[
                                        'round', 'offerer', 'responder',
                                        'offer', 'response', 'discounts'
                                    ])

            writer.writeheader()

            hist = ISPT.__history
            for round in ISPT.__history:
                for table in round.tables:
                    row = table.asdict()
                    row['round'] = round.round
                    writer.writerow(row)

        score_attrs = [
            'scores', 'avg_score_per_offer', 'avg_score_per_round',
            'table_count', 'cumulative_tables'
        ]
        score_headers = [
            name + '_' + s for s in score_attrs for name in ISPT.__names
        ]
        other_stats = ['num_players', 'round']
        column_names = other_stats + score_headers

        with open('data/stats.csv', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=column_names)
            writer.writeheader()
            for round in ISPT.__history:
                row = {'num_players': round.num_players, 'round': round.round}

                # Get the score tuples from round and place into row dict
                score_tuples = [getattr(round, attr) for attr in score_attrs]
                scores = [value for score in score_tuples for value in score]
                for col, score in zip(score_headers, scores):
                    row[col] = score
                writer.writerow(row)


class Table():
    """Determines structure for a round of actions"""
    def __init__(self, players, game, offerer=False, current_discounts=(1, 1)):
        """    """
        # Get the offerer and responder
        if not offerer:
            p = list(zip(players, current_discounts))
            random.shuffle(p)
            players, current_discounts = zip(*p)

        self.record = TableRecord(offerer=players[0],
                                  responder=players[1],
                                  players=players,
                                  offer=None,
                                  response=None,
                                  discounts=current_discounts)
        self.game = game
        self.game.increase_table_count(players)

    def process(self):
        '''Gets each players' action, decreases the table count (since this table
           will be discarded) and returns the record for game history'''

        offer = self.game.players[self.record.offerer].offer(self.record)
        if offer is None:
            print('none offer from player:')
            print(self.game.players[self.offerer].__class__.__name__)
        self.record.offer = offer
        self.record.response = self.game.players[
            self.record.responder].response(self.record, offer)
        self.game.decrease_table_count(self.record.players)

        return self.record

    def switch_players(self, discounts):
        return Table(players=(self.record.responder, self.record.offerer),
                     game=self.game,
                     offerer=True,
                     current_discounts=(discounts[1], discounts[0]))
