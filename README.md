# The Iterated Shrinking Pie Tournament Ruleset
#### version 0:0:0.01

## Abstract

In the shrinking pie game, two players negotiate how to split a fixed number of points between them. Each turn they do not come to an agreement, the ‘pie’ (points available to be split) shrinks according to a discount factor. Each player aims to maximize their own score. Between two players and with a fixed number of rounds, backward propagation shows the optimal offer that should be made and accepted in the first round. This ruleset expands the two-player game to a tournament with three or more players negotiating in pairs. Most notably, players have an additional action they can play: the option of leaving a negotiation to attempt striking a deal with a more amenable player.

## Basic Rules


### Initial setup


Players are randomly matched in pairs. Each match is called a "table", i.e. a negotiation table. If there are an odd number of players in the tournament then one player is randomly chosen to be tabled with two different players, so that all players have at least one table.


### Actions

At each of these initial tables, one player is randomly selected to go first (the 'offerer'). The offerer makes an offer between 0 and 1 inclusive, representing the proportion of the pie they are offering to the other player (the 'responder'). Specifically, the offerer's available actions are $O \in [0, 1]$.

The responder then has 3 available actions: accept, counteroffer, or reject (or actions $= \{ A, C, R\}$). At all tables, the offerers simultaneously propose their splits and the responders immediately and simultaneously choose their responses.


-Responder accepts: both players split the value of the pie as proposed by Player A. The points get added to each players’ scores. On subsequent rounds, the this table is repeated with the roles reversed: the responder makes an offer $O \in [0, 1]$ and the offerer responds with an action in $\{A, C, R\}$. In other words, the same two players are placed at a table with the responder becoming the offerer and the offerer becoming the responder.

-Responder counteroffers: neither player wins any points and the pie shrinks by the discount parameter. In the next round the players are paired at a table with the roles reversed as in the 'accept' case (offerer becomes responder and vice versa), only now they are negotiating over the shrunken pie.

-Responder rejects: neither player wins any points and the players will not be paired together in the next round. If rejections would cause the responder to be in zero tables, then the responder is randomly paired with another player in the tournament excluding the offerer. In the next round, one of the players is randomly chosen to be the offerer, however the pie is discounted for the rejecting player, while it is full for the randomly chosen player$\dagger$. The same process applies to the offerer.


### Game Parameters:
The game currently defines these parameters:
-Length of game: The number of rounds are specified any integer 1 or greater. The default length is 1000 rounds. Future versions of the game will support a random termination parameter.
-Discount parameter: A discount parameter is specified for each player, any real number between 0 and 1. Players could all have the same discount parameter or players can individually have different discounts assigned.
-Information: the players have complete information. That is they are aware of all the actions that all players have taken in previous rounds. Additionally, they are aware of all discount factors, scores, and other game statistics. Future versions of the game will support restricting the information available to players.

### Game Statistics:

Each player of course has a score which is the sum of all points they have earned. Since this number is highly sensitive to the number of tables a player participates in (which itself is random), the game also tracks:
-Average points per round
-Average points per offer

Both these statistics may be meaningful: average points per round perhaps speaks to a player's ability to profit by maintaining relationships, while average points per offer may indicate the player's ability as a dealmaker.

## API
in development.

$\dagger$It may help to imagine that each player has their own pie which discounts round by round until they accept an offer or an offer is accepted, at which point they get what's left of their pie. Also, in the rare but possible case that a player is tabled with all other players in the same round, and all tables end in rejection, then the untabled player gets randomly paired with any player in the tournament.
