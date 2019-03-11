# money.fish

Simple game and framework to study monetary phenomena

`app.py` runs as a flask application
`tick.py` provides a clock to advance the state of the game

a sample player is given in `example.py`

## Clearing algorithm

All orders are either to buy or sell exactly one fish for a given quantity of seashells.
In order to determine clearing, the algorithm proceeds as follow:

1. Sort all bids by descending price, resolve ties randomly
2. Sort all asks by ascending price, resolve ties randomly
3. Advance through both lists, element by element and stop just be fore the ask becomes greater than the bid, discard the rest
4. Take the highest undiscarded bid and the lowest undiscarded ask and compute their average. If the average is not an integer
randomly round up or down.

__Example__:

Suppose the buy orders are for 110, 102, 104, 109
and the sell orders for 99, 107, 105, 100, 110

The sorted buy orders are (110, 109, 104, 102) and the sorted sell orders (99, 100, 105, 107, 110).
The prices cross on the third element. Therefore only the buy orders at 110 and 109 will be executed
against the sell orders at 99 and 100. The actual price will be the average of 109 and 100, either
104 or 105, depending on a coinflip.

## Todo:
- deploy the application on money.fish
- provide registration link
- set schedule for test runs
   - at a set time, player can start joining the game
   - the game starts after 5 minutes
   - the game goes on for about 30 minutes, or 365 simulated days
   - display result on site

This is for testing purposes, a large batch of runs can be done
locally to compute an average.
