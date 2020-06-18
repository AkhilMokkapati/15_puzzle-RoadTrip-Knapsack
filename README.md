### The Luddy Puzzle (Variants of 15 puzzle problem)

#### Initial State:

4X4 Board Configuration with numbers from 0-15(where '0' denotes an empty tile) which is Given as input.

#### Goal State:

Canonical Configuration of the board with numbers 1-15 and 0 at the bottom right tile arranged in order.

|  1    |  2    |   3   |    4  |
| ---- | ---- | :--: | ---- |
|   5   |   6   |   7   |    8  |
|    9  |   10   |  11   |   12   |
|   13   |   14   |   15   |   0   |


1. This is an Informed search problem as we know the goal state. It is 15-puzzle problem, given any board configuration of 4X4 grid with numbers 1 to 15 and one empty tile (represented by 0), we need to arrange it to a state where numbers 1 to 15 are in order with empty tile in last position. The possible moves are, any numbered tile can be swapped with empty tile in different possible ways based on variant given as an argument
- State Space: All valid board states with legal moves based on the variant
- Successor Function: Given a board state, all possible board states with one of the each legal moves based on the variant:
  - Original – Slide a numbered tile into an adjacent empty space
  - Circular – All moves valid for original variant and if the empty space is on the edge of the board, the tile on the opposite side of the board can be moved into the empty space
  - Luddy – this variant can have only “L” shaped moves, i.e, the empty tile may be swapped with the numbered tile that is two positions to the left or right and one position up or down, or two positions up or down and one position left or right
- Edge weights: 1 for each move 
- Heuristic function(s): We have written a generalised single function which takes variant as argument and gives different heuristic costs, which is sum of number of minimum steps each tile takes to go to its goal position with moves based on variant argument.
  - Original – This will be equal to manhattan distance
  - Circular or Luddy – It is the minimum distance for a numbered tile to reach its goal position with legal moves  
  - This heuristic is admissible for all 3 variants because it counts only the minimum number of possible moves to reach to the goal state, it never over estimates
  
2. Brief description of the algorithm
  - A* search is used
    - Priority queue is used to take minimum cost step
    - Cost here is the number of steps taken until now from initial state, plus heuristic cost from present state to goal state
    - In fringe we maintain, the cost, state and moves taken until now from initial state
    - We maintain a “closed” list which has states popped out from the fringe
    - We add only those states to the fringe which are not present in “closed” list, which is a very important step
  - Heuristic is designed using BFS to find the minimum number of steps taken for a numbered tile to reach to its goal position based on the variant:
    - Heuristic Initial state: 4X4 board with all empty tiles except single numbered tile at some random position
    - Heuristic Successor: All legal single moves it can take based on the variant argument
    - Heuristic Goal state: Board with number in its goal position with respect to the actual problem, e.g., 1 should be at first position of the board
    - Heuristic Cost: Cost one for each legal step taken
  - To check if the solution exists, we are checking if the permutation inversion(PI) is even as the PI for goal state is even. This PI is a valid check for all the 3 variants
 
3. Major problems faced are in designing the heuristic and below are fixes tried:
  - As per discussion in the class we have used basic sum of Manhattan distance for each tile in original variant
  - For circular, initially we calculated manhattan for non-edge tiles and manhattan minus 2 for edge tiles, as we wanted to maintain the admissible heuristic
  - Above two heuristics are admissible and were giving quick results for few test cases. But the circular heuristic was taking around five minutes for one of the complicated board that we created as a test case
  - Initially we used number of misplaced tiles as the heuristic for Luddy variant but it was taking more than 5 minutes for simple board4
  - For luddy variant, we checked minimum steps it takes for a tile when it is at 1, 2, 3 and so on till 6 manhattan distances from its goal position and generalized this as heuristic cost for each tile equal |m-4| where m is the manhattan distance from a tile to its goal position. This reasonably improved the speed of luddy variant problems
  - To further improve we have finalised and generalized the heuristic to sum of number of minimum steps each tile takes to go to its goal position with moves based on variant argument

### Part 2: Road trip!

#### Algorithm to find good driving directions between pairs of cities in USA based on user defined cost functions.


- The program uses A* search, using desired heuristics, respective to a particular case until the desired goal state(Destination city) is reached.

- The road-segments.txt is parsed into a dictionary such that each segment has two mappings
  - a->b mapping and b->a mapping provided a and b are city names.
  - The key would be the city name and the value would be a list of cities and their respective data.
  - This way, getting successors for a city would be of almost O(1) time.

- The city-gps.txt file too is parsed into a dictionary. The key name would be the city name and the value would be the longitude and latitudes. This data is used for calculating the eucledian distances between two cities

- State space: All the mappings present in the file, road segment
- Edge weights:
  - If cost function is segments, then the edge weight is 1
  - If the cost function is distance, then the length of the length of the road
  - If the cost function is time, then distance/speed of the on the road is the edge weight
  - If the cost function is mpg, then distance of the road/(400*v(1− v/150 )^4)/150 is the edge weight

- Goal state: Destination provided by the user

- Heuristic functions:
  - SEGMENTS: We take the biggest road length(Calculated during the parsing of road-segments.txt) and is divided with the eucledian distance of the successor and the destination city. This way, we get the minimum number of segments that can be there between the successor and the destination city.
  - DISTANCE: By using the GPS, we calculate the Eucledian distance between the current city and the destination city. Since the Eucledian distance is the least amount of distance, this heuristic is admissible.
  - TIME: Its calculated by dividing the Eucledian distance from the successor to the destination by the max highway speed, we get the Heuristic. The max highway speed is computed during the road-segments.txt.
  - This heuiristic is admissible since the time can never go below the distance/(current speed).
  - MPG: By calculating the max gas consumed during the parsing of road-segments.txt and dividing it with the current eucledian
distance to the destination city, we get the admissible heuristic of mpg.

- Assumptions and simplifications
  - If a point in road segments is not in gps file, then the distance is considered as 0.


### Part 3: Choosing a team 

#### We have used 0/1 knapsack branch and bound technique to choose a team of robots that has the greatest possible skill

- Unformed search – Need to find a team of robots that has the greatest possible skill (i.e., the sum of the skill levels is as high as possible), with in given budget (B).
- What is the set of valid states, the successor function, the cost function, the goal state definition, and the initial state?
    - State space: All the combinations of robots with team sizes between 0 to (# of robots in input data).
    - Successor function: Set of teams with addition of 1 more robot that’s within budget limit.
    - Edge weights: Cost of each robots.
    - Goal State: Team with greatest skill
    - Heuristic Function:  Haven’t used a heuristic function.
- Implemented Branch and Bound Algorithm as search.
    - Given list of Robots are sorted in descending order based on Skill/Cost ratio. Since high Skill/Cost robot has a better chance of being in highest skilled team (This is not compulsory but good to start with). 
    - Priority queue is used for Fringe
    - Fringe is structured as ( - of Skill, Team, Remaining Budget, Robots explored)
    - Considered cost as negative of skill of team till now as it will priorities to explore the path with highest skill first.
    - Keeps tracks of best solution till now among the combination of teams for which all the robots are explored or for which remaining budget is zero  
    - Reducing the Search space by checking whether the teams from successor functions are promising or not. It is done by checking max possible skill for a team with best solution till now.

