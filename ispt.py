import csv, os, re, sys, importlib, time
import pprint as pp
from api import *

# Regex for parsing numeric agent parameters
FLOAT_PATTERN = r"^\d+(\.\d*)?$"


def main():
    sys.path.append(os.getcwd())

    # Read in csv file for agents in this game
    assert len(sys.argv) > 1, "Usage: python ispt.py player_list.csv"
    with open(sys.argv[1], 'r') as f:
        data = [line for line in csv.reader(f)]
        player_data, discounts = csv_to_player_data(data)

    # Instantiate players
    players = []
    sys.path.append('agents')
    for agent_str, args in player_data:
        module = importlib.import_module(agent_str)
        agent = getattr(module, agent_str)(*args)
        players.append(agent)

    # Instantiate game
    start = time.time()
    print("PLAYERS:", len(players))
    game = ISPT(players=players, discounts=discounts, max_rounds=100)
    history = game.play()
    end = time.time()
    game.graph_scores()
    game.heatmap()
    print(f"Processing time: {end - start:4f}")
    print_final_scores()


def float_converter(lst):
    result = []
    for item in lst:
        value = float(item) if re.match(FLOAT_PATTERN, item) else item
        result.append(value)
    return result


def csv_to_player_data(data):
    discounts = [float(d[1]) for d in data]
    player_data = [[d[0], float_converter(d[2:])] for d in data]
    return player_data, discounts


def print_final_scores():
    print("FINAL SCORES:")
    results = [(name, score) for name, score in zip(ISPT.get_names(),
                                                    ISPT.get_state().scores)]
    results.sort(key=lambda x: x[1], reverse=True)
    for name, score in results:
        print(f"{name}: {score:.3f}")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


if __name__ == "__main__":
    main()