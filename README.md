# The Iterated Shrinking Pie Tournament Ruleset
#### version 0.0

## Abstract

In the shrinking pie game, players negotiate how to split a fixed number of points between them. Each turn they do not come to an agreement, the ‘pie’ (points available to be split) shrinks according to a discount factor. Each player aims to maximize their own score. Between two players and with a fixed number of rounds, backward propagation shows the optimal offer that should be made and accepted in the first round. This ruleset expands this game to support multiple players negotiating in pairs with the option of leaving a negotiation to attempt striking a deal with a more amenable player.

## Basic Rules


### Initial setup


Players are randomly matched in pairs. Each match will be called a “meet”. If there are an odd number of players, then one player is randomly matched with another player who has 'already' been paired. I.e., the randomly picked player will be set to meet with two different players in the same round.


### Actions
In round 1, one player in each pair is randomly chosen to offer first. This will be Player A, who will offer to Player B a split of the pie. Specifically, Player A's actions are to offer any value between 0 and 1 inclusive according to the proportion they wish to split: $O \in [0, 1]$.

Player B then has 3 available actions:
1. Accept ("A")
2. Counteroffer ("C")
3. Reject ("R")

-If Playber B accepts: both players split the value of the pie as proposed by Player A. The points get added to each players’ scores. On subsequent rounds, the previous meet is repeated with Player B now making an offer to Player A. Player B chooses an action $O \in [0, 1]$ and Player A responds with an action in $\{A, C, R\}$

-If Player B counteroffers: the pie shrinks by the discount parameter and the game advances to the next round. Player A may now choose A, C, or R. If they accept, the pie is split by Player B's proposed proportion and the points added to each player's score.

If Player B rejects: Both players receive nothing for this round. Player B, who rejected, gets randomly paired with another player (not including player A) and a new meet begins with a new pie shrunk by the discount parameter. Player A waits to be paired with another player by this same mechanism.

Alternate: instead of present value, multiply each split by discount parameter. Since d represents opportunity cost, if a player has money in the bank it should make d % per turn

Game Parameters:
-Discount parameter: one global parameter or different values for different players
-Information: do players have complete information or something less?
-Length of game: number of rounds

Variations:
-Add a cost per round (a maintenance expense). Players start with a bank of points from which some amount is subtracted each round. If a player reaches 0, they are eliminated from the tournament.
-Some other kind of replicator mechanism?
