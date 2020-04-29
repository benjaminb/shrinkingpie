from api import *
from agents import *

# agents = {
#   'aa': AlwaysAccepts,
#   'tt': TitForTat,
#   'tt10': lambda: TitForTat(0.1),
#   'j': Jonabot,
# }
# agents['j']()

aa = AlwaysAccepts("AlwaysAccepts")
aap = AcceptsAnyPositive()
ar = AlwaysRejects()
h = Hardballer()
tt = TitForTat()
tt10 = TitForTat(0.1)
j = Jonabot()
j1 = Jonabot()
g = GhostofRudin()
g2 = GhostofRudin()
m = Mimic()
dd = DD()

game = ISPT(players=[aa, ar, h, tt])
history = game.play(max_rounds=10, export_csv=True)
print("method:")
pp.pprint(game.get_accepted_offers(0))
# game.graph_scores()
