# The Iterated Shrinking Pie Tournament Ruleset
#### version 0:0:0.01

## Abstract

In the shrinking pie game, two players negotiate how to split a fixed number of points between them. Each turn they do not come to an agreement, the ‘pie’ (points available to be split) shrinks according to a discount factor. Each player aims to maximize their own score. Between two players and with a fixed number of rounds, backward propagation shows the optimal offer that should be made and accepted in the first round. This ruleset expands the two-player game to a tournament with three or more players negotiating in pairs. Most notably, players have an additional action they can play: the option of leaving a negotiation to attempt striking a deal with a more amenable player.

## Basic Rules

Players are matched in pairs and negotiate over how to split a 'pie' of 1 point. One player offers some split and the other player responds with 'Accept', 'Counter', or 'Reject'. If the responder accepts, then they split the pie as proposed. In the next round, the offerer and responder meet again with roles reversed and negotiate over a new pie. If the responder chooses 'Counter', then both players meet in the next round with offerer and responder roles reversed, but for both players the pie shrinks according to their respective discount factors. If the responder chooses 'Reject' then the pairing between these two players is eliminated. If this leaves either player unpaired then in the next round they are randomly matched with a different player in the tournament. 

### Rules, In Depth

#### Initial Setup


Players are randomly matched in pairs. Each match is called a "table", i.e. a negotiation table. If there are an odd number of players in the tournament then one player is randomly chosen to be tabled with two different players, so that all players have at least one table. At each table is a 'pie' of 1 point to be split between the two players. 


#### Actions

At each of these initial tables, one player is randomly selected to make an initial offer. The offerer makes an offer between 0 and 1 (inclusive), representing the proportion of the pie they are offering to the other player (the 'responder'). Specifically, the offerer's available actions are $O \in [0, 1]$.

The responder then has 3 available actions: accept, counteroffer, or reject (actions $= \{ A, C, R\}$). At all tables, the offerers simultaneously propose their splits and the responders immediately and simultaneously choose their responses.


- Responder accepts: both players split the value of the pie as proposed by Player A. The points get added to each players’ scores. On subsequent rounds, the this table is repeated with the roles reversed: the responder makes an offer $O \in [0, 1]$ and the offerer responds with an action in $\{A, C, R\}$. In other words, the same two players are placed at a table with the responder becoming the offerer and the offerer becoming the responder.

- Responder counteroffers: neither player wins any points and each player's discount rate shrinks by their discount parameter. In the next round the players are paired at a table with the roles reversed as in the 'accept' case (offerer becomes responder and vice versa), only now they are negotiating over the shrunken pie.

- Responder rejects: neither player wins any points and the players will not be paired together in the next round. If the responding player would be in zero tables as the result of a rejection, then in the next round they are randomly paired with another player, excluding the offerer. Likewise, if the offerer becomes 'untabled' by rejection then in the next round they are randomly paired with another player, excluding the responder.

#### Discounts

It is possible for a player to participate in multiple tables per round: they may be an odd player and get assigned a second table in the first round or they may get assigned to additional tables as a result of other players choosing reject. Each player therefore has a discount factor *per table*, which decreases by their own discount parameter. To be precise, the 'pie' is always 1 point, and offers are always in terms of a *proportion* to be split. But the points each player actually receives is reduced by their current discount factor *at that table*.

In other words, if a player comes to a table by being randomly selected (either in the initial round or in later rounds), their discount factor is initialized to 1, otherwise their discount parameter is applied. I.e. players who arrive at a table because in the previous round they rejected or were rejected have their discount parameter applied; players who were randomly selected to participate in the table do not. 

For example, say a tournament includes 3 players, P1, P2, and P3, each with a discount rate of 0.9. P1 is tabled with P2, and P1 is also tabled with P3 (P1 is in two tables while P2 is only in one), and say P1 is the offerer at both tables. P3 accepts P1's offer, but P2 rejects. In the next round, P1 and P3 will be at a table together since P3 accepted, with P3 offering and P1 responding. So no new tables need to be generated on behalf of P1 or P3. However, since P2 rejected, there will not be a table with P1 and P2 in the next round, leaving P2 'untabled'. So P2 is randomly paired with another player in the tournament. If the tournament randomly selects P3 to play with P2 in the next round, then P2's discount parameter gets applied but for P3 it does not. As a result, P3's discount this round at this table is 1 while P2's is 0.9. If P3 offers 0.5 and P2 accepts, then P3 gets 0.5 points while P2 gets $0.9 \cdot 0.5 = 0.45$ points. If the table ends in 'Counter', then both players play each other in the next round but P2's discount becomes 0.9 while P3's discount becomes 0.81.

### Game Parameters:
The game currently supports these parameters:
- Length of game: The number of rounds are specified any integer 1 or greater. The default length is 1000 rounds. 
- Discount parameter: A discount parameter is specified for each player, any real number between 0 and 1. Players could all have the same discount parameter or players can individually have different discounts assigned.
- Information: the players have complete information. That is they are aware of all the actions that all players have taken in previous rounds. Additionally, they are aware of all discount factors, scores, and other game statistics. Future versions of the game will support restricting the information available to players.
- Noise: a noise parameter can be set, any real value in [0, 1], so that any player's response is randomly changed to one of the unchosen responses with a probability of this parameter. E.g. if the noise parameter is 0.01, and a player responds with 'Accept', then there is a 1% chance the response will be switched. If it is switched, then the response will be changed to 'Counter' or 'Reject' with equal likelihood.

### Future 
- Information Restriction: for example, players may have access only to tables in which they participated. Alternatively, players can be organized into 'teams' or social networks, with information available network-wide, perhaps after a delay of 1 or more rounds.
- Table caps: in the basic version of the game, there is no limit on how many tables a player can participate in simultaneously, and no limit on how many offers they can make or accept. However, we may want to restrict a player to being able to make or accept a certain number of offers. This may more closely model negotiations over a finite opportunity. For example, a laborer in the workforce can take on one full time job at a time, so they can only accept one offer per time period and all else being equal, would rationally accept the highest offer. If other players represent firms, then they likewise have a finite number of job positions to fill. 
- Random termination: each round after some stated minimum, the game will randomly terminate by a given probability.


### Game Statistics:

Each player of course has a score which is the sum of all points they have earned. Since this number is highly sensitive to the number of tables a player participates in (which itself is random), the game also tracks:
- Average points per round
- Average points per offer

Both these statistics may be meaningful: average points per round perhaps speaks to a player's ability to profit by maintaining relationships, while average points per offer may indicate the player's ability as a dealmaker.

## API
in development.

