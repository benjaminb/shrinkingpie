from api import *
from agents import *


x = Agent(0.4)
y = Agent(0.3)
aa = AlwaysAccepts()
aap = AcceptsAnyPositive()
ar = AlwaysRejects()
h = Hardballer()
tt = TitForTat()
tt10 = TitForTat(0.1)
game = ISPT(players=[tt, ar, tt10, h, h])
game.play(max_rounds=5)
print("Discounts:", game.state['discounts'])
#
# t = Table(players=[x, y], offerer=0)
#
# print('offerer', t.offerer)
# print('responder', t.responder)
#
# t.process()
#
# print("history:", history)
