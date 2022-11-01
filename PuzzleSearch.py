#CS170 Project 1: The Eight Puzzle
#Program is meant to solve the eight puzzle using:
### Uniform Cost Search 
### A* with Misplaced Tile Heuristic.
### A* with Manhattan Distance Heuristic.

from queue import Empty, PriorityQueue
from turtle import down, position
import copy
from types import NoneType
#####Sample puzzles, blank space represented with 0
#Solution state
goal = [[1,2,3],
          [4,5,6],
          [7,8,0]]
#Baby Stuff
depth2 = [[1,2,3],
          [4,5,6],
          [0,7,8]]
#Very Easy
depth4 = [[1,2,3],
          [5,0,6],
          [4,7,8]]
#Easy
depth8 = [[1,3,6],
          [5,0,2],
          [4,7,8]]
#Not Too Bad
depth12 = [[1,3,6],
          [5,0,7],
          [4,8,2]]
#Starting to Sweat
depth16 = [[1,6,7],
          [5,0,3],
          [4,8,2]]
#Hard
depth20 = [[7,1,2],
          [4,8,5],
          [6,3,0]]
#Very Hard
depth24 = [[0,7,2],
          [4,6,1],
          [3,5,8]]
#Yikes! Good Luck!
depth31 = [[8,6,7],
          [2,5,4],
          [3,0,1]]

#####Coordinates of the puzzle borders in format [row, column]
upperRow = [[0,0], [0,1], [0,2]]
bottomRow = [[2,0], [2,1], [2,2]]
leftCol = [[0,0], [1,0], [2,0]]
rightCol = [[0,2], [1,2], [2,2]]

#####Classes

##Class for handling Node objects
class Nodes:
    def __init__(self, puzzle, depth, cost, parent):
        self.puzzle = puzzle
        self.depth = depth
        self.cost = cost
        self.parent = parent


#####Functions

##Function to display puzzle
def printPuzzle(puzzle):
    print (puzzle[0])
    print (puzzle[1])
    print (puzzle[2])
    print ("\n")

##Function to find blank space in puzzle
##returns the position as a list [row, column]
def findBlank(puzzle):
    #index each row for the number 0
    for row in puzzle:
        try:
            col = row.index(0)
        except:
            col = -1

        if col >= 0:
            position = [puzzle.index(row), col]
            return position

    return None

#####Operators
##Function to move blank space up
def goUp(puzzle):
    newPuzzle = copy.deepcopy(puzzle)
    blankPos = findBlank(newPuzzle)
    if blankPos in upperRow:
        return None

    row = blankPos[0]
    col = blankPos[1]
    newPuzzle[row][col] = newPuzzle[row-1][col]
    newPuzzle[row-1][col] = 0

    return newPuzzle

##Function to move blank space down
def goDown(puzzle):
    newPuzzle = copy.deepcopy(puzzle)
    blankPos = findBlank(newPuzzle)
    if blankPos in bottomRow:
        print("In down func. Blank was in bottomRow, returning None")
        #return [[-1], [-1], [-1]]
        return None

    row = blankPos[0]
    col = blankPos[1]
    newPuzzle[row][col] = newPuzzle[row+1][col]
    newPuzzle[row+1][col] = 0

    return newPuzzle

##Function to move blank space left
def goLeft(puzzle):
    newPuzzle = copy.deepcopy(puzzle)
    blankPos = findBlank(newPuzzle)
    if blankPos in leftCol:
        return None

    row = blankPos[0]
    col = blankPos[1]
    newPuzzle[row][col] = newPuzzle[row][col-1]
    newPuzzle[row][col-1] = 0

    return newPuzzle

##Function to move blank space right
def goRight(puzzle):
    newPuzzle = copy.deepcopy(puzzle)
    blankPos = findBlank(newPuzzle)
    if blankPos in rightCol:
        return None

    row = blankPos[0]
    col = blankPos[1]
    newPuzzle[row][col] = newPuzzle[row][col+1]
    newPuzzle[row][col+1] = 0

    return newPuzzle

##List of tuples to iterate over operators
# operators = []
# arg = ["puzzle"]
# operators.append(lambda:goUp(*arg))
            

##Main function
def main():      
    ###Welcome user and get input
    print("Hello there, welcome to my 8-Puzzle Solver.")
    print("If you want to use a preset puzzle, enter '1'. If instead you want to create your own, enter '2'.")
    decision = int(input())

    #preset puzzle
    if (decision == 1):
        #call function to have user select preset difficulty and then pass that puzzle to algorithm selection
        presetPuzzle = selectPreset()
        selectAlgorithm(presetPuzzle)
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

        #pass created puzzle to algorithm selection
        selectAlgorithm(currPuzzle)

#Function to prompt user to choose a puzzle difficulty, returns a preset puzzle.
def selectPreset():
    difficulty = int(input("Choose a difficulty for your puzzle. Difficulty ranges from 1-8, with 1 being the easiest and 8 the hardest.\n"))

    if (difficulty == 0):
        print("You chose the solution")
        return goal

    if (difficulty == 1): 
        print("You chose 'Baby Stuff' difficulty")
        return depth2

    if (difficulty == 2): 
        print("You chose 'Very Easy' difficulty")
        return depth4

    if (difficulty == 3): 
        print("You chose 'Easy' difficulty")
        return depth8

    if (difficulty == 4): 
        print("You chose 'Not Too Bad' difficulty")
        return depth12

    if (difficulty == 5): 
        print("You chose 'Starting to Sweat' difficulty")
        return depth16

    if (difficulty == 6): 
        print("You chose 'Hard' difficulty")
        return depth20

    if (difficulty == 7): 
        print("You chose 'Very Hard' difficulty")
        return depth24

    if (difficulty == 8): 
        print("You chose 'Yikes! Good Luck!' difficulty")
        return depth31

#Function to select which algorithm willl be used to solve the puzzle
def selectAlgorithm(puzzle):
    algorithm = int(input("Choose algorithm to solve puzzle. \n (1): Uniform Cost Search \n (2): A* with Misplaced Tile Heuristic \n (3): A* with Manhattan Distance Heuristic \n"))
    
    if (algorithm == 1):
        #UCS
        uniformCost(puzzle, 0)
    
    if (algorithm == 2):
        #Misplaced tile
        print("FIXME")
    if (algorithm == 3):
        #Manhattan
        print("FIXME")

#Function for Uniform Cost Search algorithm
def uniformCost(puzzle, heuristic):
    #Create root node and push to queue 
    initNode = Nodes(puzzle, heuristic, 1, None)
    workingQueue = PriorityQueue()
    workingQueue.put((initNode))
    #initializing stuff
    repeated = dict()
    nodesExpanded = 0
    maxQueue = 0

    #Loop as long as there are nodes in workingQueue
    while not workingQueue.empty():
        currNode = workingQueue.get()

        #if the current node is goal state then return it
        if (currNode.puzzle == goal):
            print("Reached goal state")
            return currNode

        ##Expand children

        # print("Down puzzle before")
        # print(currNode.puzzle)

        # downPuzzle = goDown(currNode.puzzle)

        # print ("Down puzzle after:")
        # print(downPuzzle)

        currPuzzle = currNode.puzzle
        upNode = Nodes(goUp(currPuzzle), currNode.depth+1, 1, currNode)
        #downNode = Nodes(goDown(currPuzzle), currNode.depth+1, 1, currNode)
       # leftNode = Nodes(goLeft(currPuzzle), currNode.depth+1, 1, currNode)
        rightNode = Nodes(goRight(currPuzzle), currNode.depth+1, 1, currNode)

        print("Upnode:")
        print(upNode)
        print("Rightnode:")
        print(rightNode)

        if upNode.puzzle:
            #printPuzzle(upNode.puzzle)
            workingQueue.put((upNode))
            nodesExpanded = nodesExpanded + 1

        # try:
        #     validPuzzle = downNode.puzzle[0].index(-1)
        # except:
        #     validPuzzle = -1

        # if (validPuzzle == -1):
        #     print("In downnode")
        #     printPuzzle(downNode.puzzle)
        #     #workingQueue.put((downNode))
        #     nodesExpanded = nodesExpanded + 1

        # if leftNode.puzzle:
        #     workingQueue.put((leftNode))
        #     nodesExpanded = nodesExpanded + 1

        if rightNode.puzzle:
            workingQueue.put((rightNode))
            nodesExpanded = nodesExpanded + 1
            
        
        # possibleNodes = [upNode, downNode, leftNode, rightNode]
        
        # print("Nodes expanded: ")
        # for item in possibleNodes:
        #     if item.puzzle:
        #         nodesExpanded = nodesExpanded + 1
        #         #workingQueue.put((item))
        #         printPuzzle(item.puzzle)
        #     else:
        #         del item

        # print(nodesExpanded)

        # print("About to print expanded nodes after first run")
        # while not workingQueue.empty():
        #     newNode = workingQueue.get()
        #     printPuzzle(newNode[1].puzzle)
            

        
    
    print("out of loop")

    
    



def misplacedTile(puzzle, heuristic):
    print("FIXME")

def manhattan(puzzle, heuristic):
    print("FIXME")


###RUN program
main()



