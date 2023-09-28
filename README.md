# Eight Puzzle Solver

## Introduction

Puzzles have entertained people around the world for a long time, testing their intellect and creativity. One such puzzle is the sliding tile puzzle, in which the player must slide tiles on a square frame in order to rearrange the tiles until the correct ordering is reached. Figure 1 below shows an example of a sliding tile puzzle, known as the 15-puzzle. The square has one tile missing for the player to be able to slide the tiles. The player starts the puzzle with tiles out of order, as seen in the Initial State in Figure 1. The player must slide the tiles around until the numbers are all in ascending order, as seen in the Goal State in Figure 1. Sliding puzzles are not restricted to numbered tiles, the tiles could be things like colors or pieces of an image, and the desired ordering, or goal state, may vary as well.

[Figure 1: 15-Puzzle example, found on Resource 2a. Slide 10.]()

This project focuses specifically on the numbered sliding tile puzzle with a frame size of 3x3, also known as the 8-puzzle because of the eight numbered tiles. The project implements three distinct algorithms to solve the puzzle: Uniform Cost Search, A* with the Misplaced Tiles Heuristic, and A* with the Manhattan Distance Heuristic. The individual performance of the three algorithms is evaluated and compared in this report. I decided to write this project using the Python programming language. Python is not my strongest programming language, so this was a challenging yet very rewarding experience as I was able to increase my mastery of the language. 

## Comparison of Algorithms

As mentioned before, the project is able to solve 8-puzzles using three algorithms: Uniform Cost Search, A* with Misplaced Tile Heuristic, and A* with Manhattan Distance Heuristic. All three of these are variations of the A* algorithm, which explores the possible moves you can perform on an 8-puzzle at each stage, and choses the one that is most likely to get you to the solution. 

A* uses two values to estimate at each puzzle state, or node, the cost to get to the solution state. The first value is referred to as g(n), which is the cost to reach the current node n. For sliding tile puzzles, we have at most four possible operations that can be performed on the blank tile: up, down, left, right. 
 
[Figure 2: Possible operations on a sample puzzle. Number 0 is used to represent blank tile.]()

All these operations have the same cost, meaning that it takes the same amount of effort to perform any one operation. Because of this, the g(n) value for any node will always be equal to the number of operations performed to get to that node, also known as the depth. 

The second value to estimate the cost to the solution is the h(n) value. The h(n) value is the number returned by a heuristic function, and it gives us an approximation of the distance from node n to the solution. A* sums up these two values to get the total estimated cost from a specific node to the final goal state. The algorithm then chooses, or expands, the node with the lower cost (excluding repeat nodes previously seen), performs the possible moves that can be made from that node (referred to as creating or expanding the node’s children), calculates their cost, chooses the cheapest one, and repeats until a solution is found. At any point, A* will select the cheapest node possible, and if two nodes have the same cost, the one with the lower depth will be given priority. 
	
The difference between the three algorithms implemented in this project is the heuristic function used to calculate the h(n) value.

## Uniform Cost Search

As expressed by Dr. Keogh “Uniform Cost Search is just A* with h(n) hardcoded to equal zero” (Resource 1a. Page 1). Meaning that, at all times, all nodes have the same cost, that being their g(n) value, or their respective depth. Because of this, none of the children nodes have priority over any other, so they will be expanded in the same order they are created, or in a First In First Out manner. This type of search is referred to as a blind or uninformed search, since no actual estimation, or heuristic, is being used to guide the search. We are simply exploring the possibilities until a solution is found.

## A* with Misplaced Tile Heuristic

For this algorithm, a heuristic function is implemented in order to better estimate the cost of each node and make a more informed decision on which node to expand. Therefore, this heuristic allows for better guesses to be made that are more probable to lead to a solution faster, without expanding as many nodes. 

The Misplaced Tiles heuristic is a function that for any puzzle state returns the total count of tiles that are out of place, excluding the blank tile. Looking at the example in Figure 3 below, only the number ‘8’ tile is not in its correct position, therefore the h(n) for this example would be 1. Thus, this algorithm calculates the cost of each node by adding the depth of that node to the total number of misplaced tiles ( g(n) + h(n) ). This heuristic improves the algorithm because counting how many tiles are out of place is a good estimation of how far you are from the solution. It is reasonable that the more misplaced tiles you have, the farther you are to solving the puzzle. Since nodes will have different costs, this algorithm can prioritize the nodes with lower costs when expanding, unlike Uniform Cost Search. As mentioned before, if two nodes have the same cost, then the one with the lesser depth will be prioritized.  
 
[Figure 3: Example 8-Puzzle from Resource 2c. Slide 24.]()

## A* with Manhattan Distance Heuristic

This algorithm works just like the previous one, except it uses a different heuristic to estimate the distance to the goal. The Manhattan Distance heuristic looks at every tile that is misplaced and then calculates the distance from its current position to the goal position. It does this by counting the total moves needed (either horizontally or vertically) to get the tile to its goal position, if no other tiles are present on the board. The h(n) value is then the sum of the Manhattan distances for all of the misplaced tiles. For the example in Figure 4, the 3, 8, and 1 tiles are out of place, so each of their distances is calculated to get a total Manhattan distance of 8.

This heuristic improves the algorithm because you are counting the ideal number of moves in order to get to the solution, and the puzzle with the less number of moves is more likely to get to the solution faster. Thus, the cost for nodes using the Manhattan Distance heuristic is the sum of the depth and the distances from the goal position for all misplaced tiles ( g(n) + h(n) )

[Figure 4: Manhattan Distance example from Resource 2c. Slide 25.]()

## Comparison of Algorithms on Sample Puzzles

After programming the three algorithms, I tested them using the sample cases provided by Dr. Keogh. These puzzles are ordered in level of difficulty, represented by the solution depth. The solution depth of a puzzle is the number of optimal moves needed to get to the solution state. Meaning, the depth is the maximum number of moves needed to solve the puzzle if you always pick the best possible move. Depth 0 is our solution state, depth 2 is two moves from being solved, and in the same way depth 31 is thirty one moves away from being solved. I tested these puzzles on all three algorithms, and I will compare their performance by looking at three metrics: CPU runtime, space complexity, and time complexity. For simplicity’s sake, I will refer to the three algorithms as Uniform Cost, Misplaced Tile, and Manhattan from now on.
 
[Figure 5: Test cases found on Resource 2d. Slides 10-11]()

### CPU Runtime

[Figure 6: Graph of Runtime vs Solution Depth]()

This graph compares the time in seconds each algorithm spent solving the different test cases on my machine. Up until depth 12, all three algorithms perform really well, finding a solution in under a second. Once we reach depth 16 however, we can see how Uniform Cost is beginning to take longer than the other two algorithms, and Misplaced Tile is also starting to perform just slightly worse than Manhattan at this same depth. This trend continues as the depth increases. The time Uniform Cost takes begins to increase significantly, and eventually so does Misplaced Tile. Manhattan remains the best performer throughout, still taking less than a second at depth 24, while Misplaced Tile stands at just over 2 seconds and Uniform Cost at 13 seconds. Eventually the time for Manhattan does increase, but even at the lowest depth of 31, it finds the solution way quicker than the other two algorithms, taking just over 3 seconds while Misplaced Tile and Uniform Cost take 14 and 17 seconds respectively. Manhattan finds the solution about 5 times faster than Uniform Cost. Thus, from this graph we can conclude that Manhattan will always arrive at the solution the fastest, followed by Misplaced Tile and then by Uniform Cost.

### Space Complexity

[Figure 7: Graph of Maximum Queue Size vs. Solution Depth]()
	
Whenever a node is expanded and its children are created, they are added to a queue according to their priority. Therefore, the maximum size the queue reached while the program was running indicates the number of nodes created, and thus represents the space complexity of the algorithm. From the graph it can be seen that Uniform Cost has the worst space complexity, followed by Misplaced Tile, and then followed by Manhattan. As we reach the higher depths, Misplaced Tile ends up with a queue size closer to Uniform Cost than to Manhattan. The higher queue size indicates that the algorithms are not making very good estimates and are thus exploring and creating significantly more nodes. At a depth of 24, Manhattan ends with a max queue size of around 1400, while Uniform Cost ends with around 24000, meaning that Uniform Cost occupies about 17 times more memory to find the solution.

### Time Complexity

[Figure 8: Graph of Total Nodes Expanded vs the Solution Depth]()

The total number of nodes expanded represents all the nodes that were taken off the queue and whose children were created. This represents the time complexity as it tells you the number of nodes visited, and the more nodes you visit the longer the algorithm will run for. This graph continues the trend seen in the previous two graphs, with Manhattan performing the best, followed by Misplaced Tile and then by Uniform Cost. Starting at solution depth 12, Uniform Cost begins to expand significantly more nodes than the other two algorithms, and it continues to do so until the highest depth. Misplaced Tile and Manhattan expand a smaller number of nodes up until depth 20, where Misplaced Tile begins to expand a much higher number of nodes. At the highest depth, Manhattan expanded about 15000 nodes, while Uniform Cost expanded around 180000, meaning that Uniform Cost has a time complexity around 12 times worse than Manhattan.

## Additional Examples
I created some random puzzles and tested them with the Manhattan algorithm. Since my algorithm took under 4 seconds to complete the provided depth 31 puzzle, I decided that if no solution was found within 8 seconds, then no solution exists and the puzzle is unsolvable. Here are the results:


[Figure 9: Results from testing out random puzzle]()

The puzzle I created and tested is seen in Figure 9. When I tested this puzzle I timed it with my phone until 8 seconds passed, then I dismissed it as unsolvable. However, I kept my program running to see if my algorithm would eventually terminate by itself and declare that there indeed is no solution. My algorithm did so after 24 seconds, confirming my previous assumption.

[Figure 10: Second random puzzle tested]()

For the random puzzle seen in Figure 10, a solution was found at depth 22 in 1.8 seconds, which is consistent with the graph in Figure 6. The maximum queue size also fits nicely into the graph in Figure 7, however the nodes expanded are significantly higher than expected. 

[Figure 11: Third random puzzle tested]()
	
Similar to the first random puzzle, the one shown in figure 11 had no solution, and the program terminated after 22 seconds. 

## Conclusion

In this project, three different versions of the A* searching algorithm were implemented to solve the tile 3x3 sliding puzzle known as the 8-puzzle. The three algorithms implemented were then tested with increasingly difficult puzzles. Different metrics were used in order to analyze and compare the CPU runtimes, space complexities, and time complexities of the algorithms. 
For all metrics, the best performing algorithm was A* with the Manhattan Distance heuristic, followed by A* with the Misplaced Tile heuristic, and then the worst performance was Uniform Cost Search. This is to be expected, as the heuristics improve the algorithm by making informed decisions on which nodes to expand first. Furthermore, the Manhattan heuristic performs significantly better than the other algorithms at higher depths. This is due to the more accurate heuristic which allows for better decisions since Manhattan takes into account the number of misplaced tiles as well as their distance to their respective goal positions. 
From the data gathered here, it can be observed that for runtime, space complexity, and time complexity, Manhattan performs 5, 17, and 12 times better than Uniform Cost, respectively. Therefore, we can conclude that the A* algorithm with the Manhattan Distance heuristic will always outperform Uniform Cost Search and A* with the Misplaced Tile Heuristic. 

## Code and Tracebacks of Depth 8 and Depth 24 Puzzles

All my code, along with tracebacks for the depth 8 and depth 24 test case puzzles are in this GitHub repository.
The time results for these puzzles are longer since the traceback was printed, something I was not doing when running my test cases.
