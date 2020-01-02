# The Iterated Shrinking Pie Tournament Ruleset
#### version 0.0

## Abstract

In the shrinking pie game, players negotiate how to split a fixed number of points between them. Each turn they do not come to an agreement, the ‘pie’ (points available to be split) shrinks according to a discount factor. Each player aims to maximize their own score. Between two players and with a fixed number of rounds, backward propagation shows the optimal offer that should be made and accepted in the first round. This ruleset expands this game to support multiple players negotiating in pairs with the option of leaving a negotiation to attempt striking a deal with a more amenable player. 

## Basic Rules

### Initial setup


Players are randomly matched in pairs. Each match will be called a “meet”. If there are an odd number of players, then one player is randomly matched with another player who has ‘already been paired. I.e., the randomly picked player will be set to meet with two different players. 



### Actions
In round 1, one player per meet is randomly chosen to move first. They offer to split the pie with the other player accordion to a proportion of their choice between 0 and 1 inclusive. 

The other player at the meet may
1. Accept (“A”)
2. Counteroffer 
3. Reject

-If the player accepts, both players split the (present) value of the pie as proposed. The points get added to each players’ scores immediately. 
If counteroffer:
  Pie shrinks by the discount parameter. From this amount, the counteroffering player makes a counteroffer
If reject
  Both players receive nothing for this round. The rejecting player is randomly paired with another player next round

Subsequent rounds
If previous round, offer had been accepted:
  Both parties split the agreed amount

If previous round, counteroffer had been made:
  Player receiving the offer can accept, counteroffer, or reject

If previous round ended in rejection:
  Player who rejected is randomly matched to another player, but not the player who they just rejected. The pie 

Alternate: instead of present value, multiply each split by discount parameter. Since d represents opportunity cost, if a player has money in the bank it should make d % per turn

Information:
What information is available to players in each turn?
Version 1: complete information
Players, offer & rejection history
All scores in all turns

Incomplete information
# of players in game
Own score in each turn

Length of Game
A fixed number of turns (500, 1000, ...)
0.001 or so chance of tournament ending each round
