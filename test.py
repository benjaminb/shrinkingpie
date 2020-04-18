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
game = ISPT(players=[j, j1, tt, tt10, h, h, h,  aa, g, g2])
game.play(max_rounds=1000)
print("Discounts:", game.state['discounts'])
