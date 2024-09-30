#!/usr/local/bin/python3
# solve_birds.py : Bird puzzle solver
#
# Code by: Manuel Schabel / mschabe
#
# Based on skeleton code by D. Crandall & B551 course staff, Fall 2022
#
# N birds stand in a row on a wire, each wearing a t-shirt with a number.
# In a single step, two adjacent birds can swap places. How can
# they rearrange themselves to be in order from 1 to N in the fewest
# possible steps?

# !/usr/bin/env python3
import sys

N=5

#####
# THE ABSTRACTION:
#
# Initial state:

# Goal state:
# given a state, returns True or False to indicate if it is the goal state
def is_goal(state):
    return state == list(range(1, N+1))

# Successor function:
# given a state, return a list of successor states
def successors(state):
    return [ state[0:n] + [state[n+1],] + [state[n],] + state[n+2:] for n in range(0, N-1) ]

# Heuristic function:
# given a state, return an estimate of the number of steps to a goal from that state
def h(state):
    delta = 0  # Sum of goal position differences
    for number in range(1, N+1):
        delta += abs(state.index(number)+1 - number)
    return delta / 2  # Divide by 2 to make h admissible (e.g. single swap can reduce delta by up to 2!)


#########
#
# THE ALGORITHM:
#
def solve(initial_state):
    fringe = []
    counter = 1  # represents g(s), i.e. cost from initial state to current state s
    states_visited = set()  # tracking of visited states to avoid cycles and increase runtime

    fringe += [(initial_state, [], h(initial_state))]
    while len(fringe) > 0:
        f_temp = [fringe[i][2] for i in range(len(fringe))]  # extract h(s) of all states in fringe
        min_index = f_temp.index(min(f_temp))  # identify index with min h(s)
        (state, path, f) = fringe.pop(min_index)
        states_visited.add(str(state))  # add state as str since lists are not hashable

        if is_goal(state):
            return path+[state,]

        for s in successors(state):
            if str(s) not in states_visited:
                fringe.append((s, path+[state,], h(s)+counter))

        counter += 1

    return []


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a test case filename"))

    test_cases = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            test_cases.append([ int(i) for i in line.split() ])
    for initial_state in test_cases:
        	print('From state ' + str(initial_state) + " found goal state by taking path: " + str(solve(initial_state)))

