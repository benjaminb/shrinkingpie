from api import *
from agents import *
import pprint as pp

# agents = {
#   'aa': AlwaysAccepts,
#   'tt': TitForTat,
#   'tt10': lambda: TitForTat(0.1),
#   'j': Jonabot,
# }
# agents['j']()

ask = Asker()
aa = AlwaysAccepts("AlwaysAccepts")
aap = AcceptsAnyPositive()
ar = AlwaysRejects()
h = Hardballer()
tt = TitForTat()
tt10 = TitForTat(0.1)
j = Jonabot()
j1 = Jonabot('j1')
g = GhostofRudin()
g2 = GhostofRudin()
m = Mimic()
dd = DD()

game = ISPT(players=[aa, aa, ask])
history = game.play(max_rounds=10, export_csv=True)
pp.pprint(history[0])
print('names', game.names)
print("aa name:", aa.name)
# game.graph_scores()
