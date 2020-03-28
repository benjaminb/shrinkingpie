# ITERATED SHRINKING PIE TOURNAMENT

# from api import ISPT
from api import *

# Game Parameters
# dictionary for various game Parameters
parameters = {
    'discount': 0.1,
    'min_rounds': 1000, # minimum no. rounds
    'end_prob': 0.001 # prob. game ends each round after min
}

"""Functions"""


# at the end of each round, put the history into the history object

# run the game
def main():
    # instantiate objects
    agent1 = Agent(split=0.4)

    agents = []
    game = ISPT(players=agents)
        # Get agents. For files in agents directory:
            # read in file and execute
            # for file in files:
            # agent = exec(open(file).read())
            # agents.append(agent)
            # agents = [exec(open(file).read()) for file in files]

    # Test if game should be over
        # If game is over, report results

    # if game is not over,
    # handle meets
    # process actions
    # record results in history
    # iterate
    print("END OF PROGRAM")

if __name__ == "__main__":
    main()
