from api import *

x = Agent(0.4)
y = Agent(0.3)

game = ISPT(players=[x, y, x, x, y])
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
