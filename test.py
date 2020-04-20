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
m = Mimic()
game = ISPT(players=[j, j1, g, m])
history = game.play(max_rounds=4)
