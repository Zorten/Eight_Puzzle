#CS170 Project 1: The Eight Puzzle
#Program is meant to solve the eight puzzle using:
### Uniform Cost Search 
### A* with Misplaced Tile Heuristic.
### A* with Manhattan Distance Heuristic.

#####Functions

##Function to display puzzle
def printPuzzle(puzzle):
    print (puzzle[0])
    print (puzzle[1])
    print (puzzle[2])


#####Sample puzzles, blank space represented with 0

#Solution state
depth0 = [[1,2,3],
          [4,5,6],
          [7,8,0]]

depth2 = [[1,2,3],
          [4,5,6],
          [0,7,8]]

depth4 = [[1,2,3],
          [5,0,6],
          [4,7,8]]

depth8 = [[1,3,6],
          [5,0,2],
          [4,7,8]]

depth12 = [[1,3,6],
          [5,0,7],
          [4,8,2]]

depth16 = [[1,6,7],
          [5,0,3],
          [4,8,2]]

depth20 = [[7,1,2],
          [4,8,5],
          [6,3,0]]

depth24 = [[0,7,2],
          [4,6,1],
          [3,5,8]]

depth31 = [[8,6,7],
          [2,5,4],
          [3,0,1]]

          
###Welcome user and get input
print("Hello there, welcome to my 8-Puzzle Solver.")
print("If you want to use a preset puzzle, enter '1'. If instead you want to create your own, enter '2'.")
decision = int(input())

#preset puzzle
if (decision == 1):
    print("Using sample puzzle")
    currPuzzle = depth2

    printPuzzle(currPuzzle)
    print("FIXME")

#custom puzzle
elif (decision == 2):
    #Get user input
    print("Please enter your puzzle below. Use a SPACE as a delimiter for each number. Only valid 8-Puzzles are accepted. Press enter when you are done with each row.")
    row1 = str(input("First Row: "))
    row2 = str(input("Second Row: "))
    row3 = str(input("Third Row: "))

    #Split strings to get numbers
    row1 = row1.split(" ", 2)
    row2 = row2.split(" ", 2)
    row3 = row3.split(" ", 2)

    #change numbers from str to int
    row1 = list(map(int, row1))
    row2 = list(map(int, row2))
    row3 = list(map(int, row3))

    currPuzzle = [row1, row2, row3]

    printPuzzle(currPuzzle)
    print("FIXME")



