# Assignment 1 - Searching

## Part 1: Birds, heuristics, and A*
### Question
On a power line sit five birds, each wearing a different number from 1 to N. They start in a random order
and their goal is to re-arrange themselves to be in order from 1 to N (e.g., 12345), in as few steps as
possible. In any one step, exactly one bird can exchange places with exactly one of its neighboring birds.
We can pose this as a search problem in which there is a set of states S corresponding to all possible
permutations of the birds (i.e., S = {12345, 12354, 12453, ...} for N = 5).

### Solution
(1) Search abstraction
	1. State space: Simple state representation as lists containing numbers 1:N in arbitrary order
	2. Successor fct: Implemented as sucessors()-fct that returns all pairwise adjacent permutations of input state, i.e. all states where two adjacent numbers/birds swap places
	3. Edge weights: NA, see heuristic fct
	4. Goal state: Ordered list, checked by is_goal()-fct that returns True if input state is goal state
	5. Heuristic function: h(s)-fct checks the positional differences of all numbers in input state vs. goal state, sums them up, and divides the sum by 2
		The final divison of the delta sum by 2 is to make h() admissible since a single swap/successor can reduce the delta by up to 2 and without this adjustment h() could overestimate the cost to reach the goal state, thus rendering h() inadmissble
		The priority value of all states in the fringe is composed of h(s) + g(s), where the latter represents the cost from the initial state to the current state s (see (2) below))

(2) Search algorithm: The solve()-fct searches through the state space by making use of a priority queue (based on h() described above) and returns the path from initial to goal state. 
	In more detail:
	1. Initialization of 1. fringe based on (row-wise) file input, 2. counter that represents g(s), i.e. cost from initial state to current state s, and 3. a set that tracks visited states to avoid cycles and increase runtime
	2. While fringe is not empty: Determine state in fringe with lowest heuristic cost (incl. cost to get there, i.e. g(s)), delete that state from fringe and add it to the set of visited states
		Check if state is goal state and, if true, return path to get there and break while loop
		If not goal state, 1. add all state successors, which are not in set of already visited states, to fringe, 2. attach path to successor state and 3. calculate and attach f(s), based on f(s) and g(s) represented by the counter, which tracks how many steps were necessary to reach added successor state
		Increase counter by 1 at the end of while loop, and return empty list if no solution is found, i.e. if while loop ends in case of an empty fringe
	

(3) Further discussion topics: 
	1. Priority queue: I first tried to implement this as a class that deletes and returns the min/max priority element based on input specification. However, given that this can also be coded more specifically with 2 lines of code in the while loop, introducing an extra class seemed to be somewhat overengineered.
		Instead, the priority queue now works as follows: Extract f(s) of all fringe states, determine index of minimum f-value, and pop the corresponding fringe state (using this index).
	2. Runtime measurement: Included in previous version, but removed from final version as per instruction "Please don't modify anything below this line"



## Part 2: The 2022 Puzzle
### Question
Consider the 2022 puzzle, which is a lot like the 15-puzzle we talked about in class, but: (1) it has 25 tiles, so
there are no empty spots on the board; (2) instead of moving a single tile into an open space,
a move in this puzzle consists of either (a) sliding an entire row of tiles left or right one space, with
the left- or right-most tile ‘wrapping around’ to the other side of the board, (b) sliding an entire
column of tiles up or down one space, with the top- or bottom-most tile ‘wrapping around’ to
the other side of the board, (c) rotating the outer ‘ring’ of tiles either clockwise or
counterclockwise, or (d) rotating the inner ring either clockwise or counterclockwise.

![image](https://github.com/user-attachments/assets/285a34ac-7cf9-4d00-83bb-445017dc3bb8)

The goal of the puzzle is to find a short sequence of moves that restores the canonical configuration (on the
left above) given an initial board configuration. We’ve provided skeleton code to get you started. You can
run the skeleton code on the command line:

```python3 solver2022.py [input-board-filename]```

where input-board-filename is a text file containing a board configuration (we have provided an example).

You’ll need to complete the function called solve(), which should return a list of valid moves. The moves
should be encoded as strings in the following way:
* For sliding rows, R (right) or L (left), followed by the row number indicating the row to move left or
right. The row numbers range from 1-5.
* For sliding columns, U (up) or D (down), followed by the column number indicating the column to move
up or down. The column numbers range from 1-5.
* For rotations, I (inner) or O (outer), followed by whether the rotation is clockwise (c) or counterclock-
wise (cc).

For example, the above diagram performs the moves L3 (slide row 3 left), D3 (slide column 3 down), Occ
(outer counterclockwise), and Ic (inner clockwise).

The initial code does not work correctly. Using this code as a starting point, implement a fast version, using
A* search with a suitable heuristic function that guarantees finding a solution in as few moves as possible.
Try to make your code as fast as possible even for difficult boards, although it is not necessarily possible to
quickly solve all puzzles. For example, board1.txt can be solved in 11 moves. You will need to be creative
with your heuristic function in order to find this solution in less than 15 minutes.

In your report, answer the following questions:
1. In this problem, what is the branching factor of the search tree?
2. If the solution can be reached in 7 moves, about how many states would we need to explore before we
found it if we used BFS instead of A* search? A rough answer is fine.

### Solution

Question - What is the branching factor of the search tree?

Answer - The branching factor of the search tree would be 24

Question - If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we used BFS instead of A* search? A rough answer is fine.

Answer - If the solution is available at depth 7 of the tree, in BFS we will have to explore 24^7 = 4586471424 states.

(1) Description of search formulation
	
	1. State space: Consists the set of all orientations of the 25 tiled puzzle before and after various column, row and ring transformations (including the initial state which is usually given and the final canonical state which has the numbers 1 to 25 in order from left to right, row-wise).
	
	2. Successor function: This function returns all possible succeeding states to the current state we are in. All those states are appended to a list called moves[]. They are as follows: 
		L - row left rotation, R - row right rotation, U - column up rotation, D - column down rotation
		Oc - outer ring clockwise rotation, Occ - outer ring counter clockwise rotation
		Ic - inner ring clockwise rotation, Icc - inner ring counter clockwise rotation	
	
	3. Goal state(s): There is only one final/goal state in this puzzle i.e. the canonical state of the puzzle, where 1 is the top left tile and sequentially continued, leads to 25, bottom right tile.

	4. Heuristic functions: The heuristic function which we used is the modified version of the Manhattan distance (square block distance). We are taking a weighted average of the obtained Manhattan distance as the heuristic function, h(state).

(2) Search algorithm:

The goal of the problem to find the shortest sequence of moves from the current state to the canonical configuration. Manhattan distance is used as a heuristic function to achieve the above. Initially the problem was approached using A* which made wrap movements design of the states. I also faced issues in implementing Clockwise and anti clockwise rotation of the inner and outer rings, I referred the below websites to learn how to deal with these issues and modified it to suit our problem.

Heuristic function

h(s) = The weighted average of modified/wrap manhatten distance between the current location of a tile to it's target location.

f(n) is known as the cost function and it attaches the cost/penalty in taking a particular step.

Implemented Algorithm flow

—> initial board configuration is extracted

—> The fringe is defined as priority queue and the initial board is appended with cost 0

—> While Fringe is non empty:

—> current_state = pop the item from fringe in a way that it gives least value of f(s)

—> If GOAL?(current-state):

—> return path-taken

—> for every SUCC(current-state):

—> If current Successor is not visited: 

—> append (f(s), current board, path taken until now + current step) to the fringe

—> if path is not found:

—> return False

(3) Discussion material:

1. Assumptions:

	1. There always exists a solution to the given board.
	2. The map size is 5*5.
	
2. Problems faced:

		Manhattan distance is used as the heuristic function but this resulted in overestimated solution which makes it non admissible. Therefore, we modified the Manhattan distance to include wrap distance. This heuristic works correctly for a matrix that requires 3 moves I.e., board 0 but gets into an infinite loop for board 1. The reasons why it doesn’t work might be due to indentation of the problem or because of the choice of heuristic function.
		
3. Design decisions:

	            --> A* heuristic to modified manhattan as heuristic to include wrap movements



## Part 3: Road trip!
### Question
It’s time to start planning a post-pandemic road trip! If you stop and think about it, finding the shortest
driving route between two distant places — say, one on the east coast and one on the west coast of the U.S. —
is extremely complicated. There are over 4 million miles of roads in the U.S. alone, and trying all possible paths
between two places would be nearly impossible. So how can mapping software like Google Maps find routes
nearly instantly? The answer is A* search!

We’ve prepared a dataset of major highway segments of the United States (and parts of southern Canada
and northern Mexico), including highway names, distances, and speed limits; you can visualize this as a
graph with nodes as towns and highway segments as edges. We’ve also prepared a dataset of cities and
towns with corresponding latitude-longitude positions. Your job is to find good driving directions between
pairs of cities given by the user.

![image](https://github.com/user-attachments/assets/2b4fd35a-e756-4bb8-bb32-f78f46f97175)

Like any real-world dataset, our road network has mistakes and inconsistencies; in the example above, for
example, the third city visited is a highway intersection instead of the name of a town. Some of these “towns” will not have latitude-longitude coordinates in the cities dataset; you should design your code to still work
well in the face of these problems.

Extra credit: Implement an additional cost-function: statetour should find the shortest route from the start
city to the end city, but that passes through at least one city in each of the 48 contiguous U.S. states.

### Solution
(1) Description of search formulation
	1. State space: Defined by vertices (cities) and edges (highway segments) in a graph of major US highway connections. A node/city is defined by its name and geoposition while edges/segments are represented by their highway name, distance/length, and speed limit. In our implementation (see description below), a state is defined by its node name, accummulated route information (distance, time, highway segments traveled etc.) and a state evaluation based on a heuristic fct.
	2. Successor function: Successors()-fct gets specific city/node and all road segements as input and returns all connected cities as dictionary with cities as key and segment information (miles, speed limit, name) as values.
	3. Edge weights: Represented by segment information, i.e. distance (in miles) and speed limit (in miles). Depending on the cost function in use, these parameters define the weight of links/edges/connections in the highway network, i.e. distance or travel/delivery time.
	4. Goal state(s): Single city/node provided as input and checked by is_goal()-fct, which returns True if goal state is reached.
	5. Heuristic functions: Based on the provided cost function (i.e. the basis for route optimization), the heuristic function h() evaluates how promising a state is. To be admissible (i.e. never overestimate true cost to goal state), we implement a heuristic function that returns 1. the "great circle" distance between the current and goal city based on the geodata if the route distance is to be minimized, 2. the "great circle" distance divided by the maximum speed limit of all road segments considered (to ensure admissability) if general time or delivery time is to be optimized, and 3. simply 1 if the number of road segments is to be minimized. If the current node (e.g. highway junction) has no GPS data, the search algo simply reduces the prior h()-value by the time/distance traveled on the last road segment/edge.

(2) Search algorithm: A* algo with priority queue and heuristic fct. h(s)
	First, all city geolocations and road segment data are loaded, and the fringe + set of visited states/cities is initialized.
	Then, as long as the fringe is not empty, the following steps are executed.
		"Pop" minimum cost state/city (i.e. highest priority) from fringe and check if it is the goal state.
		For all successors of the min cost city, remove cities already visited before to avoid loops and check if city has geodata. If yes, use heuristic function h() to evaluate the current state. If not, decrease h() of the predecessor by time/distance travelled on current road segment (i.e. predecessor -> current city) depending on cost function.
		Calculate c(s) (i.e. cost to reach current state) depending on cost function and delivery time.
		Delete current city in fringe if already present with higher cost than currently evaluated path and add current city with minimum cost to set of visited states.
		Add all relevant path information of (minimum path) current city to fringe, incl. segment information, distance, time, f(s) = c(s) + h(s), and no. of segments 

(3) Discussion material:
	1. Parallel development: We developed the solution on this problem in parallel (i.e. two different approaches) and finally decided on which version to submit based on code readability/commenting, runtime and results. Admittedly, the submitted solution does not feature the fastest runtime (still decent for the problem at hand, based on extensive testing), but we believe that it features an easy-to-follow code structure and extensive commenting for better readability. In doing so, we invested a lot of effort and time in developing an algorithm for this problem.
	2. Runtime measurement: Included in previous version, but removed from final version as per instruction "Please don't modify anything below this line"
	3. Design: We moved from a code structure primarily structured around the provided cost function to a single A* search algorithm that implements the cost fct distinction within the heuristic function to eliminate code redundancy.
	4. Assumptions: To ensure admissibility of the heuristic function, the "great circle" distance and maximum speed limit was used to approximate/evaluate distance and travel time to the goal state.
			
