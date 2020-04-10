from api import *
from agents import *


x = Agent(0.4)
y = Agent(0.3)
aa = AlwaysAccepts()
aap = AcceptsAnyPositive()
ar = AlwaysRejects()
game = ISPT(players=[ar, ar, ar])
game.play(max_rounds=10)
#
# t = Table(players=[x, y], offerer=0)
#
# print('offerer', t.offerer)
# print('responder', t.responder)
#
# t.process()
#
# print("history:", history)
