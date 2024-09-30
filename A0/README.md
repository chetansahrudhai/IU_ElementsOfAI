# Assignment 0 - Search and Python
## Problem 1 - Navigation
A certain autonomous agent, a pichu, likes to fly around the house and interrupt video recordings at the most inopportune moments. Suppose that a house consists of a grid of N × M cells, represented like this:
```
....XXX
.XXX...
....X..
.X.X...
.X.X.X.
pX...X@
```
As you can see, the map consists of N lines (in this case, 6) and M columns
(in this case, 7). Each cell of the house is marked with one of four symbols: p
represents the agent’s current location, X represents a wall through which the
agent cannot pass, . represents open space over which the agent can fly, and @
represents your location (presumably with video recording in progress).

Your goal is to write a program that finds the shortest path between the agent
and you. The agent can move one square at a time in any of the four principal
compass directions, and the program should find the shortest distance between
the two points and then output a string of letters (L, R, D, and U for left, right,
down, and up) indicating that solution. Your program should take a single
command line argument, which is the name of the file containing the map file.
```
[x@x ~] python3 route_pichu.py map1.txt
Shhhh... quiet while I navigate!
Here’s the solution I found:
16 UUURRDDDRRUURRDD
```
You can assume that there is always exactly one p and one @ in the map file. If there is no solution, your
program should display path length -1 and not display a path.

### My Solution
Terminology -
* Initial State - A pichu, that needs to reach a destination by avoiding walls.
* Goal State - The pichu reaches the target through the shortest path. 
* Cost Function - The written function, as it ultimately gives the final shortest path.

Approach - 
Initially, the code runs forever as there is no return function. I added a function, which can be returned, that traverses through the lists and checks the valid moves, while appending the path.
And, a list keeps track of all the visited nodes.

## Problem 2 - Hide-and-seek
Suppose that instead of a single agent as in Problem 1, you have adopted k agents. The problem is that these
agents do not like one another, which means that they have to be positioned such that no two agents can
see one another. 

Write a program called arrange_pichus.py that takes the filename of a map in the same
format as Problem 1 as well as a single parameter specifying the number k of agents that you have. You can
assume k ≥ 1. Assume two agents can see each other if they are on either the same row, column, or diagonal
of the map, and there are no walls between them. An agent can only be positioned on empty squares (marked
with .). It’s okay if agents see you, and you obscure the view between agents, as if you were a wall. 

Your program should output a new version of the map, but with the agents’ locations marked with p. Note that
exactly one p will already be fixed in the input map file. If there is no solution, your program should just
display False. Here’s an example on the same sample output on the same map as in Problem 1:
```
[x@x ~] python3 arrange_pichus.py map1.txt 5
....XXX
.XXXp..
.p..X..
.X.X...
.X.X.Xp
pX.p.X@
```

### My Solution
Terminology -
* Initial State - The map has walls with an agent and open spaces on a grid.
* Goal State - Placing the pichus in a way where in none of the conditions i.e. no pichu should be in the same column, row or diagonal.
* Failed State - If a given number of pichus can't fit in the grid adhering to the conditions, the program returns false.

Approach -
This is similar to the N-Queens problem and a back tracking approach, which checks every column, row and diagonal, would be suitable.
