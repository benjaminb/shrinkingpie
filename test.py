from api import *
from agents import *


x = Agent(0.4)
y = Agent(0.3)
aa = AlwaysAccepts()
aap = AcceptsAnyPositive()
ar = AlwaysRejects()
h = Hardballer()
game = ISPT(players=[aa, aa, ar, h, h])
game.play(max_rounds=20)
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
