import random
import math
from graphics import *

NumberOfPoints = 50
NumberOfTreesToGenerate = 40
NumberOfPointsToMutateForTrainingData = 30
TreeDepth = 5

DataPointCircleSize = 7
TreeGridCircleSize = 3
ScaleFactor = 7
GridWidth = 50
GridHeight = 50
WindowWidth = GridWidth * ScaleFactor
WindowHeight = GridHeight * ScaleFactor

class dataPoint:
    def __init__(self,X,Y,colorNumber):
        self.x = X
        self.y = Y
        self.colorNumber = colorNumber
    def toString(self):
        return str(self.x) + " " + str(self.y)

class splitDecision:
    def __init__(self,sides,number,isX):
        self.sides = sides
        self.number = number
        self.isX = isX

class sidesOfGraph:
    def __init__(self,firstSide,secondSide,isHorizontal):
        self.firstSide = firstSide
        self.secondSide = secondSide
        self.isHorizontal =isHorizontal
    def getDifferenceInEntrophy(self,li):
        oldEntropy = calculateCurrentEntrophy(li)
        newEntropy1 = calculateCurrentEntrophy(self.firstSide)
        newEntropy2 = calculateCurrentEntrophy(self.secondSide)
        oddsOfFirstSide = len(self.firstSide)/len(li)
        oddsOfSecondSide = len(self.secondSide)/len(li)
        return oddsOfFirstSide * (oldEntropy-newEntropy1) + oddsOfSecondSide * (oldEntropy-newEntropy2)

def getColorFromColorNumber(colorNumber):
    if (colorNumber == 0):
        return color_rgb(255, 0, 0)
    if (colorNumber == 1):
        return color_rgb(0, 255, 0)
    if (colorNumber == 2):
        return color_rgb(0, 0, 255)

def getFrequencyOfColorNumber(li,colorNumber):
    if(len(li)==0):
        return 0
    count = 0
    for point in li:
        if(point.colorNumber==colorNumber):
            count+=1
    return count/(len(li))

def getMostFrequentColor(li):
    if(len(li)==0):
        return -1
    freqReds = getFrequencyOfColorNumber(li,0)
    freqGreens = getFrequencyOfColorNumber(li,1)
    freqBlues = getFrequencyOfColorNumber(li,2)
    if((freqReds>freqGreens) & (freqReds>freqBlues)):
        return 0
    elif(freqGreens>freqBlues):
        return 1
    else:
        return 2

def calculateCurrentEntrophy(li):
    if(len(li)==0):
        return 0
    freqReds = getFrequencyOfColorNumber(li,0)
    freqGreens = getFrequencyOfColorNumber(li,1)
    freqBlues = getFrequencyOfColorNumber(li,2)

    total = 0
    if(freqReds>0):
        total+=(freqReds * math.log2(1/(freqReds)))
    if (freqGreens > 0):
        total += (freqGreens * math.log2(1 / (freqGreens)))
    if(freqBlues>0):
        total+=(freqBlues * math.log2(1/(freqBlues)))
    return total

def drawGrid(win):
    for i in range(1,GridHeight):
        win.create_line(0,i*ScaleFactor,WindowWidth,i*ScaleFactor)
    for i in range(1, GridWidth):
        win.create_line(i*ScaleFactor,0,i*ScaleFactor,WindowHeight)

def drawPoints(win,points):
    for point in points:
        c = Circle(Point(point.x * ScaleFactor, point.y * ScaleFactor), DataPointCircleSize)
        c.setFill(getColorFromColorNumber(point.colorNumber))
        c.draw(win)

def splitX(li,number):
    firstSide = list()
    secondSide = list()
    for point in li:
        if(point.x < number):
            firstSide.append(point)
        else:
            secondSide.append(point)
    return sidesOfGraph(firstSide,secondSide,True)

def splitY(li,number):
    firstSide = list()
    secondSide = list()
    for point in li:
        if(point.y < number):
            firstSide.append(point)
        else:
            secondSide.append(point)
    return sidesOfGraph(firstSide,secondSide,False)

class treeNode:
    def __init__(self,leftNode,rightNode,numberToCompare,isX):
        self.isEnd = False
        self.leftNode = leftNode
        self.rightNode = rightNode
        self.numberToCompare = numberToCompare
        self.isX = isX
class treeEndNode:
    def __init__(self,colorToGoTo):
        self.colorToGoTo = colorToGoTo
        self.isEnd = True


def getColorNumberFor(tree,x,y):
    if(tree.isEnd):
        return tree.colorToGoTo
    else:
        if(tree.isX):
            if(x<tree.numberToCompare):
                return getColorNumberFor(tree.leftNode,x,y)
            else:
                return getColorNumberFor(tree.rightNode,x,y)
        else:
            if(y<tree.numberToCompare):
                return getColorNumberFor(tree.leftNode,x,y)
            else:
                return getColorNumberFor(tree.rightNode,x,y)

def getBestSplits(list):
    bestDifference = 0
    number = 0
    sides = sidesOfGraph(list,list,False)
    isX = False
    for point in list:
        splitsX = splitX(list,point.x)
        splitsY = splitY(list,point.y)
        bestDifferenceForX = splitsX.getDifferenceInEntrophy(list)
        bestDifferenceForY = splitsY.getDifferenceInEntrophy(list)

        if(bestDifferenceForY>bestDifference):
            bestDifference = bestDifferenceForX
            sides = splitsY
            number = point.y
            isX = False

        if(bestDifferenceForX>bestDifference):
            bestDifference = bestDifferenceForY
            sides = splitsX
            number = point.x
            isX = True

    return splitDecision(sides,number,isX)

def buildDecisionTree(depth,list):
    if(depth>TreeDepth):
        return treeEndNode(getMostFrequentColor(list))
    else:
        splits = getBestSplits(list)
        leftNode = buildDecisionTree(depth+1,splits.sides.firstSide)
        rightNode = buildDecisionTree(depth+1,splits.sides.secondSide)
        return treeNode(leftNode,rightNode,splits.number,splits.isX)

def drawTreeGrid(win,tree):
    for i in range(0, GridWidth):
        for j in range(0,GridHeight):
            color = getColorFromColorNumber(getColorNumberFor(tree,i,j))
            c = Circle(Point((i * ScaleFactor), (j * ScaleFactor)), TreeGridCircleSize)
            c.setFill(color)
            c.draw(win)

def drawTreeAverageGrid(win,treeAverage):
    for i in range(0, GridWidth):
        for j in range(0,GridHeight):
            color = getColorFromColorNumber(treeAverage[(i,j)])
            c = Circle(Point((i * ScaleFactor), (j * ScaleFactor)), TreeGridCircleSize)
            c.setFill(color)
            c.draw(win)

def getDeepCopy(points):
    newPoints = list()
    for point in points:
        newPoints.append(dataPoint(point.x,point.y,point.colorNumber))
    return newPoints

def addNoiseToGraph(points):
    newPoints = getDeepCopy(points)
    for i in range(0,NumberOfPointsToMutateForTrainingData):
        pointToChange = random.randint(0, NumberOfPoints-1)
        if(random.randint(0,1)==1):
            numberToChangeTo = random.randint(0, GridWidth - 1)
            newPoints[pointToChange].x = numberToChangeTo
        else:
            numberToChangeTo = random.randint(0, GridHeight - 1)
            newPoints[pointToChange].y = numberToChangeTo
    return newPoints

def getAverageOfTrees(listOfTrees):
    retval = dict()
    for i in range(0,GridWidth):
        for j in range (0,GridHeight):
            retval[(i,j)] = getAverageOfTreesForOnePoint(listOfTrees,i,j)
    return retval

def getAverageOfTreesForOnePoint(listOfTrees,x,y):
    numReds = 0
    numGreens = 0
    numBlues = 0
    for tree in listOfTrees:
        colorValue = getColorNumberFor(tree,x,y)
        if(colorValue==0):
            numReds+=1
        elif(colorValue==1):
            numGreens+=1
        else:
            numBlues+=1
    if((numReds>numGreens) & (numReds>numBlues)):
        return 0
    elif(numGreens>numBlues):
        return 1
    else:
        return 2



#---------------------------------------------
points = list()
for i in range(0,NumberOfPoints):
    points.append(dataPoint(random.randint(1,GridWidth-1),random.randint(1,GridHeight-1),random.randint(0,2)))

firstTree = buildDecisionTree(0,points)
win1 = GraphWin("Start", WindowWidth, WindowHeight)
drawGrid(win1)
drawTreeGrid(win1,firstTree)
drawPoints(win1,points)

trees = list()
for i in range(0,NumberOfTreesToGenerate):
    newPoints = addNoiseToGraph(points)
    tree = buildDecisionTree(0,newPoints)
    trees.append(tree)

trueTree = getAverageOfTrees(trees)
win2 = GraphWin("End", WindowWidth, WindowHeight)
drawGrid(win2)
drawTreeAverageGrid(win2,trueTree)
drawPoints(win2,points)

win2.getMouse()


