from api import *
from agents import *

# agents = {
#   'aa': AlwaysAccepts,
#   'tt': TitForTat,
#   'tt10': lambda: TitForTat(0.1),
#   'j': Jonabot,
# }
# agents['j']()

aa = AlwaysAccepts()
aap = AcceptsAnyPositive()
ar = AlwaysRejects()
h = Hardballer()
tt = TitForTat()
tt10 = TitForTat(0.1)
j = Jonabot()
j1 = Jonabot()
g = GhostofRudin()
g2 = GhostofRudin()
game = ISPT(players=[j, j1, g, h, h, ar, ar, ar])
history = game.play(max_rounds=4)
print("History tests")
print("Round 2:")
print(history[2])
print("Accessing the tables from round 1:")
print(history[1].current_discounts)
print("Accessing scores from round 2:")
print(history[2].scores)
