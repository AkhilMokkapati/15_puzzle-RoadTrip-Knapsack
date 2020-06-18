#!/usr/local/bin/python3
#
# choose_team.py : Choose a team of maximum skill under a fixed budget
#
# Code by: [PLEASE PUT YOUR NAMES AND USER IDS HERE]
#
# Based on skeleton code by D. Crandall, September 2019
#
import sys
from queue import PriorityQueue

# Function to read input data having (robot names, skills, and rates)
def load_people(filename):
    people={}
    with open(filename, "r") as file:
        for line in file:
            l = line.split()
            people[l[0]] = [ float(i) for i in l[1:] ] 
    return people

# Returns team of robots with max skill found amoung explored teams
def solution_till_now(neg_skill,team,rem_budget,explored_robots,solution):
    if neg_skill< solution[0]:
        return (neg_skill,)+((team),)+(rem_budget,explored_robots)
    else: return solution

#Discards the team if (skill of team + skill of All unexplored robots)
# less than Skill of solution till now 
def is_promising_team(new_explored_robots,new_neg_skill,new_rem_budget,sorted_list,solution):
    rem_skill = 0; rem_budget =new_rem_budget
    for rem_robots in sorted_list[new_explored_robots:]:
        if rem_budget-rem_robots[1][1]>=0:
            rem_skill += rem_robots[1][0]
            rem_budget -= rem_robots[1][1]
        else:
            rem_skill+=(rem_budget/rem_robots[1][1])*rem_robots[1][0]
            break
    if(-rem_skill+new_neg_skill<solution[0]):
        return True
    else: False
    
# Returns promissing teams with and without adding next robot
def successors(neg_skill,team,rem_budget,explored_robots,sorted_list,solution):
    succ=[]
    for s in [1,0]:
        if s ==1:
            new_rem_budget = rem_budget- s * sorted_list[explored_robots][1][1]
            if new_rem_budget>=0:
                # subtracting skill of next robot since, we are maintaining -ve of skill
                new_neg_skill = neg_skill- s *sorted_list[explored_robots][1][0]
                if len(team)>0:
                    new_team = team + ((sorted_list[explored_robots][0],s),)
                else:
                    new_team = ((sorted_list[explored_robots][0],s),)
                new_explored_robots = explored_robots+1
            else:
                new_rem_budget = rem_budget 
                new_neg_skill = neg_skill
                new_team = team 
                new_explored_robots = explored_robots+1
        else:
            #if s=0 i.e creating a team with out that robot
            #just increments the explored_robots
            new_rem_budget = rem_budget 
            new_neg_skill = neg_skill
            new_team = team 
            new_explored_robots = explored_robots+1
        # checking if it is a promissing team to explore further
        if is_promising_team(new_explored_robots,new_neg_skill,new_rem_budget,sorted_list,solution):
            succ.append(((new_neg_skill,)+((new_team),)+(new_rem_budget,new_explored_robots)))
    return succ



def solve(people,budget):
    fringe = PriorityQueue()
    explored_teams = []
    #Sorting, list of robots based on Skill/Price in Decreasing order
    sorted_list = sorted(people.items(), key=lambda x: x[1][0]/x[1][1],reverse=True)
    
    fringe.put((0,(),budget,0))
    solution = (0,(),budget,0)
    
    while fringe.qsize()>0:
        (neg_skill,team,rem_budget,explored_robots) = fringe.get()
        if (explored_robots !=len(sorted_list)) and rem_budget!=0:
             for succ_team in successors(neg_skill,team,rem_budget,explored_robots,sorted_list,solution):
                if succ_team not in explored_teams:
                    fringe.put(succ_team)
                    explored_teams.append(succ_team)
        else:
            solution = solution_till_now(neg_skill,team,rem_budget,explored_robots,solution)

    return solution[1:-2][0]

if __name__ == "__main__":

    if(len(sys.argv) != 3):
        raise Exception('Error: expected 2 command line arguments')

    budget = float(sys.argv[2])
    people = load_people(sys.argv[1])
    solution = solve(people, budget)
    if len(solution)>0:
        print("Found a group with %d people costing %f with total skill %f" % \
                   ( len(solution), sum(people[p][1]*f for p,f in solution), sum(people[p][0]*f for p,f in solution)))
        for s in solution:
            print("%s %f" % s)
    else:
        print("Inf")
        


