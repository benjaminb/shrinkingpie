from api import *
from agents import *


x = Agent(0.4)
y = Agent(0.3)
aa = AlwaysAccepts()
aap = AcceptsAnyPositive()
game = ISPT(players=[x, y, aa, aap])
game.play()
#
# t = Table(players=[x, y], offerer=0)
#
# print('offerer', t.offerer)
# print('responder', t.responder)
#
# t.process()
#
# print("history:", history)
