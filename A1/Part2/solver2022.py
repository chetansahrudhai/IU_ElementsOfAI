#!/usr/local/bin/python3
# solver2022.py : 2022 Sliding tile puzzle solver
#
# Code by: Megha Nagabhushana Reddy (menaga@iu.edu)
#
# Based on skeleton code by D. Crandall & B551 Staff, Fall 2022
#

import sys

from queue import PriorityQueue

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

def innerRingRotation(current_map,direction):
    # extracting inner matrix
    innerMap = list(map(list, zip(*list(map(list, zip(*current_map[1:-1])))[1:-1])))
    innerMap = outerRingRotation(innerMap, direction)
    
    innerMap.append(current_map[-1][1:-1])
    innerMap.insert(0, current_map[0][1:-1])

    innerMap = list(map(list,zip(*innerMap)))
    current_map = list(map(list,zip(*current_map)))
    
    innerMap.append(current_map[-1])
    innerMap.insert(0, current_map[0])

    innerMap = list(map(list,zip(*innerMap)))
    
    return innerMap

def outerRingRotation(current_map,direction):
    # idea of storing in a single list : https://www.codeproject.com/Questions/5299028/Rotatematrixrings-given-matrix-of-orderm-N-and-a-v
    # storing all values in a single list
    map_values = current_map[0][:-1] + [x[-1] for x in current_map][:-1] + current_map[-1][::-1][:-1] + [x[0] for x in current_map][::-1][:-1]
    if direction == 'c':
        map_values  = [map_values[-1]] + map_values[:-1]
    
    elif direction == 'cc':
        map_values  = map_values[1:] + [map_values[0]]
    # setting first and third side
    current_map[0] = map_values[:len(current_map[0])]
    current_map[-1] = map_values[len(current_map[0]) + len(current_map)-2: len(current_map[0]) + len(current_map)- 2 + len(current_map[0])][::-1]
    # setting second and fourth side
    current_map = list(map(list, zip(*current_map)))
    current_map[-1] = map_values[len(current_map[0]) - 1: len(current_map[0]) + len(current_map)-1]
    current_map[0] = [current_map[0][0]] + map_values[len(current_map[0]) + len(current_map) - 2+ len(current_map[0]) -1 : ][::-1]
    current_map = list(map(list, zip(*current_map)))
    return current_map 

def rowRotation(current_map,row, direction):
    if direction == 'R':
        current_map[row] = [current_map[row][-1]] + list(current_map[row][:-1])
    elif direction == 'L':
        current_map[row] = list(current_map[row][1:]) + [current_map[row][0]]  
    return current_map 

def columnRotation(current_map,col,direction):
    current_map = list(map(list, zip(*current_map)))
    if direction == 'U':
        current_map = rowRotation(current_map, col, 'L')
    elif direction == 'D':
        current_map = rowRotation(current_map, col, 'R')      
    return  list(map(list, zip(*current_map)))
# return a list of possible successor states
def successors(state):
    valid_moves = []
    # successor of rows
    for i in range(1,len(state)+1):
        valid_moves.append((rowRotation(list(map(list, state[:])),i-1,'L'), 'L' + str(i)))
        valid_moves.append((rowRotation(list(map(list, state[:])),i-1,'R'), 'R' + str(i)))
    # successor of colums
    for i in range(1,len(state[0])+1):
        valid_moves.append((columnRotation(list(map(list, state[:])),i-1,'U'), 'U' + str(i)))
        valid_moves.append((columnRotation(list(map(list, state[:])),i-1,'D'), 'D' + str(i)))
    
    valid_moves.extend([
        (outerRingRotation(list(map(list, state[:])), 'c'), 'Oc'), 
        (outerRingRotation(list(map(list, state[:])), 'cc'), 'Occ'), 
        (innerRingRotation(list(map(list, state[:])), 'c'), 'Ic'), 
        (innerRingRotation(list(map(list, state[:])), 'cc') , 'Icc')
    ])

    return valid_moves

# check if we've reached the goal
def is_goal(state,solution):
    if state == solution:
        return True
    else:
        return False

def solve(initial_board):
    initial_board = [initial_board[5*i:5*(i+1)] for i in range(5)]
    solution = [[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15], [16,17,18,19,20], [21,22,23,24,25]]    
    # generating the actual position of each value
    solution_loc = {}
    for i in range(len(solution)):
        for j in range(len(solution[0])):
            solution_loc[solution[i][j]] = (i,j)

    # generating the priority queue
    fringe = PriorityQueue()
    fringe.put((0, initial_board, []))
    visited_nodes = []

    while not fringe.empty():
        (current_cost, current_map, current_path)=fringe.get()
        visited_nodes.append(current_map)

        # checking the goal state
        if is_goal(current_map,solution):
            return ([i.replace('_', '') for i in current_path])
        
        for moves in successors(current_map):
            if moves[0] not in visited_nodes:
                tempCost =  heuristic(moves[0], solution_loc)
                # generating f(s) = path_travelled per tile + avg manhatten distance per tile
                # g(s) = path_travelled per tile
                # h(s) = avg manhatten distance per tile
                tempCost += len(current_path)/25
                fringe.put((tempCost,  moves[0], current_path + [moves[1]]))

    return []
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    #return ["Oc","L2","Icc", "R4"]

def manhatten_distance(num1,num2, N):
    # implementation of modified manhatten distance 
    # that covers the corner cases for the problem
    a = abs(num1[0] - num2[0])
    b = abs(num1[1] - num2[1])
    
    distance1 = a + b
    distance2 = abs(N -  a) + b
    distance3 = a + abs(N - b)
    distance4 = abs(N -  a) + abs(N - b)

    return min(distance1,distance2, distance3, distance4)

def heuristic(current_map, solution_loc):

    # modified manhatten distance
    manhattenDistance = []
    for i in range(len(current_map)):
        for j in range(len(current_map[0])):
            if solution_loc[current_map[i][j]] != (i,j):
                distance = manhatten_distance((i,j), (solution_loc[current_map[i][j]]), len(current_map))
                manhattenDistance += [distance]

    # getting the weighted average of manhatten distance as the heuristic
    sumManDist = sum(manhattenDistance)
    if sumManDist != 0:
        sumManDist /= len(manhattenDistance)
    else:
        sumManDist = 0
    return sumManDist 



# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
