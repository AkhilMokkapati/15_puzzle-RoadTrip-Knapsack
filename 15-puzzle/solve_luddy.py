#!/usr/local/bin/python3
# solve_luddy.py : Sliding tile puzzle solver
#
# Code by: Akhil Mokkapati, Vijay Sai Kondamadugu, Vivek Shreshta - akmokka, vikond, vivband
#
# Based on skeleton code by D. Crandall, September 2019
#
from queue import PriorityQueue
import sys
import numpy as np
import time
import math

# Original moves
MOVES = { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }

# Circular moves
CMOVES = { "R": [(0, -1),(0,-3)], "L": [(0, 1),(0,3)], "D": [(-1, 0),(-3,0)], "U": [(1,0),(3,0)] }

def circular_moves(CMOVES):
    return [(c,val[k]) for (c, val) in CMOVES.items() for k in range(2)]

# Luddy moves
LMOVES = { "A": (2,1), "B": (2,-1), "C": (-2,1), "D":(-2,-1), "E": (1,2), "F": (1,-2), "G": (-1,2), "H": (-1,-2) }

def rowcol2ind(row, col):
    return row*4 + col

def ind2rowcol(ind):
    return (int(ind/4), ind % 4)

def valid_index(row, col):
    return 0 <= row <= 3 and 0 <= col <= 3

def swap_ind(list, ind1, ind2):
    return list[0:ind1] + (list[ind2],) + list[ind1+1:ind2] + (list[ind1],) + list[ind2+1:]

def swap_tiles(state, row1, col1, row2, col2):
    return swap_ind(state, *(sorted((rowcol2ind(row1,col1), rowcol2ind(row2,col2)))))

def printable_board(row):
    return [ '%3d %3d %3d %3d'  % (row[j:(j+4)]) for j in range(0, 16, 4) ]
  
#------------Heuristic Started--------------------------
# check if we've reached the goal
def is_goal_heuristic(state,i):
    return state[i-1]==i

# return a list of possible successor states
def successors_heuristic(state,i,variant):
    (empty_row, empty_col) = ind2rowcol(state.index(i))
    if variant == 'luddy':
        return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
                     for (c, (i, j)) in LMOVES.items() if valid_index(empty_row+i, empty_col+j) ]
    if variant == 'circular':
        return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
                     for (c, (i, j)) in circular_moves(CMOVES) if valid_index(empty_row+i, empty_col+j) ]
    if variant == 'original':
        return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
                     for (c, (i, j)) in MOVES.items() if valid_index(empty_row+i, empty_col+j) ]
       
# The solver for heuristic - uses BFS!
def solve_heuristic(initial_board,i,variant):
    visited = []
    fringe = []
    fringe.append((initial_board,""))
    while len(fringe)!=0:
        (state, route_so_far) = fringe.pop(0)
        if is_goal_heuristic(state,i):
            return( len(route_so_far) )
        for (succ,move) in successors_heuristic( state,i,variant ):
            if (succ not in visited):
                fringe.append((succ, route_so_far + move))
                visited.append(state)

    return math.inf

def heuristic(board,variant):
    cost=0
    for i in start_state:
        if i>0:
            cost+= solve_heuristic(board,i,variant)
    return cost
#------------Heauristic Ended--------------------------

# calculate permutation Inversionfor a state
def permutation_inversion(state):
    state = list(state)
    return sum([len([state[j] for j in range(i+1,len(state)) if state[j] != 0 and state[j] < val]) \
                for i,val in enumerate(state)]) + int(np.where(np.array([state[i:i+4] \
                                      for i in range(0, len(state), 4)]) == 0)[0])+1

# does goal exists for a state    
def is_solution(state):
    return permutation_inversion(state)%2 == 0
    
# return a list of possible successor states
def successors(gs,state,variant):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    if variant == 'circular':
        return [ (gs+heuristic(swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j),variant), \
                  swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
                 for (c, (i, j)) in circular_moves(CMOVES) if valid_index(empty_row+i, empty_col+j) ]
    elif variant == 'original':
        return [ (gs+heuristic(swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j),variant), \
                  swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
                 for (c, (i, j)) in MOVES.items() if valid_index(empty_row+i, empty_col+j) ]
    elif variant == 'luddy':
        return [ (gs+heuristic(swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j),variant), \
                  swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
                 for (c, (i, j)) in LMOVES.items() if valid_index(empty_row+i, empty_col+j) ]

# check if we've reached the goal
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) and state[-1]==0

# The solver! - considers g(s)+h(s)
def solve(initial_board,variant):
    closed = []
    fringe = PriorityQueue()
    fringe.put((0,initial_board,""))
    while not fringe.empty():
        (cost,state, route_so_far) = fringe.get()
        closed.append(state)
        if is_goal(state):
            return( route_so_far )
        for (fs,succ,move) in successors( len(route_so_far)+1, state, variant ):
            if (succ not in closed):
                fringe.put((fs,succ, route_so_far + move))
    return False

# main function
if __name__ == "__main__":
    start_time = time.time()
    
    if(len(sys.argv) != 3):
        raise(Exception("Error: expected 2 arguments"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if not (sys.argv[2] == "original" or sys.argv[2] == "circular" or sys.argv[2] == "luddy"):
        raise(Exception("Error: unsupported variant entered -- all characters need to be small!"))

    if len(start_state) != 16:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))
    
    variant = sys.argv[2]  
    if is_solution(start_state):
        print("Solving...")
        route = solve(tuple(start_state),variant)
        print("--- %s seconds ---" % (time.time() - start_time))
        print("Solution found in " + str(len(route)) + " moves:" + "\n" + route)
    else:
        print(permutation_inversion(start_state))
        print("Inf")
        
    
    
    
    

