#####Author: Zergio Ruvalcaba
#####CS170 Project 1: The Eight Puzzle
## Project Description: This program will solve the eight puzzle using one of three algorithms:
##    Uniform Cost Search 
##    A* with Misplaced Tile Heuristic.
##    A* with Manhattan Distance Heuristic.
## The user can choose from 8 different preset puzzles, or they can enter their own.
## Only valid 8-Puzzles will be solved
#
# I acknowledge all content contained herein, excluding template, provided code, or example
# code, is my own original work.
#

from queue import PriorityQueue
import copy
import time
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
#These are used to check if blank is in the border of the puzzle
upperRow = [[0,0], [0,1], [0,2]]
bottomRow = [[2,0], [2,1], [2,2]]
leftCol = [[0,0], [1,0], [2,0]]
rightCol = [[0,2], [1,2], [2,2]]

#####Dictionary that stores the position of all the numbers in the solution board
###Position  stored as a tupple in (row, column) format
positionDict = {
    1 : (0,0),
    2 : (0,1),
    3 : (0,2),
    4 : (1,0),
    5 : (1,1),
    6 : (1,1),
    7 : (2,0),
    8 : (2,1),
    0 : (2,2)
}


#####Class for handling Node objects
class Nodes:
    def __init__(self, puzzle, depth, cost, parent):
        self.puzzle = puzzle
        self.depth = depth
        self.cost = cost
        self.parent = parent

    #comparison operator in order to properly sort queue by priorities: cost or depth
    def __lt__(self, other):
        if (self.cost < other.cost):
            return True
        elif (self.cost > other.cost):
            return False
        else:
            if (self.depth < other.depth):
                return True
            elif (self.depth > other.depth):
                return False
            
        
        

    #function to convert puzzle from lists to tuple
    def turnTupple(self):
        copyPuzzle = copy.deepcopy(self.puzzle)

        tupPuzzle = tuple(map(tuple, copyPuzzle))
        
        return tupPuzzle

#####Functions

##Function to display puzzle
def printPuzzle(puzzle):
    print (puzzle[0])
    print (puzzle[1])
    print (puzzle[2])
    print ("\n")

##Functions to print solution paths for testing purposes
#Needed separate function for UCS because of the way the priority queue is constructed
def solPathUCS(initNode):
    if initNode == None:
        return

    solPathUCS(initNode.parent)
    printPuzzle(initNode.puzzle)

def solPath(initNode):
    if initNode == None:
        return

    solPath(initNode[2].parent)
    printPuzzle(initNode[2].puzzle)

##Function to find blank space in puzzle
##returns the position of blank space as a list [row, column]
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

#####Operators possible on puzzle
##Function to move blank space up
def goUp(puzzle):
    newPuzzle = copy.deepcopy(puzzle)
    blankPos = findBlank(newPuzzle)
    #if blank is in the border, this move is invalid so return none
    if blankPos in upperRow:
        return None

    #perform move and return new puzzle
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
        print("You chose to solve the puzzle with the Uniform Cost Search algorithm")
        uniformCost(puzzle, 0)
    
    if (algorithm == 2):
        #Misplaced tile
        print("You chose to solve the puzzle with the A* algorithm and the Misplaced Tile heuristic")
        a_star(puzzle, 1)
    if (algorithm == 3):
        #Manhattan
        print("You chose to solve the puzzle with the A* algorithm and the Manhattan Distance heuristic")
        a_star(puzzle, 2)

#####Function for Uniform Cost Search algorithm
def uniformCost(puzzle, heuristic):
    #Begin timer to track time elapsed 
    startTime = time.time()

    #Print out puzzle we are trying to solve
    print("Initial puzzle: ")
    printPuzzle(puzzle)

    #For testing purposes
    trace = "n" #str(input("Would you like to print out the trace path? [Y/N] "))
    solution = "n" #str(input("Would you like to print out the solution path? [Y/N] "))

    #hardcode h(n) to be zero
    hVal = heuristic
    #keep track of total number of nodes expanded
    nodesExpanded = 0
    #keep track of the maximum size of the queue
    maxQueue = 0
    
    #Create root node and push to queue. Since all nodes have same cost, no priority given. 
    initNode = Nodes(puzzle, 0, hVal, None)
    workingQueue = PriorityQueue()
    workingQueue.put((initNode))

    #Initializing dictonary to detect duplicate states and add initial puzzle
    repeatDict = dict()
    repeatDict[initNode.turnTupple()] = "Root board"


    #Loop as long as there are nodes in workingQueue
    while not workingQueue.empty():
        #Update maximum queue if queue has increased
        maxQueue = max(maxQueue, workingQueue.qsize())
        #Get Node at top of queue
        currNode = workingQueue.get()
        #Get puzzle state and depth of current Node
        currPuzzle = currNode.puzzle
        currDepth = currNode.depth

        #Update nodes expanded var and print puzzle that was just expanded, except for root
        if (not workingQueue.empty()):
            nodesExpanded+= 1
            if(trace == "Y" or trace == "y"):
                print("The best state to expand with a g(n) = " + str(currDepth) + " and h(n) = " + str(hVal)  )
                printPuzzle(currPuzzle) 

        #if the current node is goal state then return it and print metrics
        if (currPuzzle == goal):
            print("Reached goal state!")
            if (solution == "Y" or solution == "y"):
                print("Here's the solution path:")
                solPathUCS(currNode)
            print("Solution Depth: " + str(currDepth))
            print("Total Nodes Expanded: " + str(nodesExpanded))
            print("Max Queue Size: " + str(maxQueue))
            #Print out time elapsed
            endTime = time.time() 
            totalTime = endTime - startTime
            if (totalTime >= 60):
                totalTime = totalTime / 60
                totalTime = round(totalTime, 1)
                print("Time elapsed: " + str(totalTime) + " minutes")
            elif (totalTime >= 1):
                totalTime = round(totalTime, 1)
                print("Time elapsed: " + str(totalTime) + " seconds")
            else:
                totalTime = totalTime * 1000
                totalTime = round(totalTime)
                print("Time elapsed: " + str(totalTime) + " milliseconds")

            return currNode

        ##Expand children
        #Get possible puzzles and store them in list
        upPuzzle = goUp(currPuzzle)
        leftPuzzle = goLeft(currPuzzle)
        rightPuzzle = goRight(currPuzzle)
        downPuzzle = goDown(currPuzzle)
        possibleMoves = [rightPuzzle, leftPuzzle, upPuzzle, downPuzzle]

        #iterate over list
        for puzzle in possibleMoves:
            #if the move was valid, expand new child Node
            if puzzle:
                newNode = Nodes(puzzle, currDepth+1, 1, currNode)
                #turn 2D array puzzle into a tupple
                tupPuzzle = newNode.turnTupple()
                #if puzzle is found in dict, it's a duplicate so delete node that was created
                if (tupPuzzle in repeatDict):
                    del newNode
                else:
                    #if puzzle is unseen one, add it to dictionary and put Node in queue
                    repeatDict[tupPuzzle] = "Unseen puzzle"
                    workingQueue.put((newNode)) 

    #Queue empty, out of loop, thus no solution
    print("Failure, no solution found.")
    return None      

#####Function for A* with Misplaced Tile Heuristic
def a_star(puzzle, heuristic):
    #Begin timer to track time elapsed 
    startTime = time.time()

    #Print out puzzle we are trying to solve
    print("Initial puzzle: ")
    printPuzzle(puzzle)

    #For testing purposes
    trace = "n" #str(input("Would you like to print out the trace path? [Y/N] "))
    solution = "n" #str(input("Would you like to print out the solution path? [Y/N] "))

    #keep track of total number of nodes expanded
    nodesExpanded = 0
    #keep track of the maximum size of the queue
    maxQueue = 0
    
    #Create root node and push to queue 
    initNode = Nodes(puzzle, 0, 0, None)
    workingQueue = PriorityQueue()
    #using cost as first priority value: the lower the cost the higher the priority
    #using depth as second priority value: if costs are equal, then priority will be based on the lowest depth value.
    workingQueue.put((initNode.cost, initNode.depth, initNode))
    
    #Initializing dictonary to detect duplicate states and add initial puzzle
    repeatDict = dict()
    repeatDict[initNode.turnTupple()] = "Root board"


    #Loop as long as there are nodes in workingQueue
    while not workingQueue.empty():
        #Update maximum queue if queue has increased
        maxQueue = max(maxQueue, workingQueue.qsize())
        #Get Node at top of queue
        currNode = workingQueue.get()
        #Get puzzle state and depth of current Node
        currPuzzle = currNode[2].puzzle
        currDepth = currNode[2].depth

        #Node is expanded when off the queue, so print its g and h values, except for root node
        if (not workingQueue.empty()):
            nodesExpanded+= 1
            if(trace == "Y" or trace == "y"):
                print("The best state to expand with a g(n) = " + str(currDepth) + " and h(n) = " + str(currNode[2].cost - currDepth)  )
                printPuzzle(currPuzzle) 

        #if the current node is goal state then return it and print metrics
        if (currPuzzle == goal):
            print("Reached goal state!")
            if(solution == "Y" or solution == "y"):
                print("Here's the solution path:")
                solPath(currNode)
            print("Solution Depth: " + str(currNode[2].depth))
            print("Total Nodes Expanded: " + str(nodesExpanded))
            print("Max Queue Size: " + str(maxQueue))
            #Print out time elapsed
            endTime = time.time()
            totalTime = endTime - startTime
            if (totalTime >= 60):
                totalTime = totalTime / 60
                totalTime = round(totalTime, 1)
                print("Time elapsed: " + str(totalTime) + " minutes")
            elif (totalTime >= 1):
                totalTime = round(totalTime, 1)
                print("Time elapsed: " + str(totalTime) + " seconds")
            else:
                totalTime = totalTime * 1000
                totalTime = round(totalTime, 1)
                print("Time elapsed: " + str(totalTime) + " milliseconds")

            return currNode

        ##Expand children
        #Get possible puzzles and store them in list
        upPuzzle = goUp(currPuzzle)
        leftPuzzle = goLeft(currPuzzle)
        rightPuzzle = goRight(currPuzzle)
        downPuzzle = goDown(currPuzzle)
        possibleMoves = [rightPuzzle, leftPuzzle, upPuzzle, downPuzzle]

        #iterate over list
        for puzzle in possibleMoves:
            #if the move was valid, expand new child Node
            if puzzle:
                hVal = getCosts(puzzle, heuristic)
                #f(n) = g(n) + h(n)
                nodeCost = (currDepth + 1) + hVal
                newNode = Nodes(puzzle, currDepth+1, nodeCost, currNode)
                #turn 2D array puzzle into a tupple
                tupPuzzle = newNode.turnTupple()
                #if puzzle is found in dict, it's a duplicate so delete node that was created
                if (tupPuzzle in repeatDict):
                    del newNode
                else:
                    #if puzzle is unseen one, add it to dictionary and put Node in queue
                    repeatDict[tupPuzzle] = "Unseen puzzle"
                    workingQueue.put((newNode.cost, newNode.depth, newNode))

    #Queue empty, out of loop, thus no solution
    print("Failure, no solution found.")
    return None  

#####Function to get heuristic cost h(n)
def getCosts(puzzle, heuristic):
    #This is for a 3x3 puzzle. This var can be changed for different nXn puzzles. 
    puzzleDimension = 3

    if (heuristic == 1):
        #iterate over each row and column to check all positions
        hVal = 0
        for i in range(puzzleDimension):
            for j in range(puzzleDimension):
                #If values differ, there's a misplaced tile so increase count, except for the blank
                if (puzzle[i][j] != goal[i][j] and goal[i][j] != 0):
                    hVal += 1
    
        return hVal

    if (heuristic == 2):
        #iterate over each row and column to check all positions
        hVal = 0
        for i in range(puzzleDimension):
            for j in range(puzzleDimension):
                #If values differ, there's a misplaced tile so calculate distance
                if (puzzle[i][j] != goal[i][j] and puzzle[i][j] != 0):
                    number = puzzle[i][j]
                    numPos = positionDict[number]
                    hDist = abs(numPos[0] - i)
                    vDist = abs(numPos[1] - j)
                    manDist = hDist + vDist
                    hVal += manDist
    
        return hVal
        

###RUN program
main()
