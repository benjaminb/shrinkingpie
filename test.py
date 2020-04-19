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
o = Overthinker()
l = LinBot()
r = Rando()
game = ISPT(players=[o, j, j1, g, h, tt, tt10, aa, ar, r, l])
game.play(max_rounds=50, export_csv=False)
print("Discounts:", game.state.discounts)
