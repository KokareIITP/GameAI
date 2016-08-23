'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import *

from constants import *
from utils import *
from core import *

# Creates a grid as a 2D array of True/False values (True =  traversable). 
# Also returns the dimensions of the grid as a (columns, rows) list.
# world: reference to the GameWorld 
# cellsize: the cell size, which indicates the width and height of each cell
def myCreateGrid(world, cellsize):
    grid = None
    dimensions = (0, 0)
    worldWidth = world.dimensions[0]
    worldHeight = world.dimensions[1]
    lines = world.getLinesWithoutBorders()
    worldObstacles = world.getObstacles()
    numOfColumns = int(worldWidth/cellsize)
    numOfRows = int(worldHeight/cellsize)

    dimensions = (numOfColumns, numOfRows)
    grid = [[False for i in range(0, numOfRows + 1)] for j in range(0, numOfColumns + 1)]

    def isValidCell(cellBounds):
        cellPointTopLeft = (cellBounds[0], cellBounds[1])
        cellPointBottomLeft = (cellBounds[0], cellBounds[1] + cellsize)
        cellPointTopRight = (cellBounds[0] + cellsize, cellBounds[1])
        cellPointBottomRight = (cellBounds[0] + cellsize, cellBounds[1] + cellsize)

        for obstacle in worldObstacles:
            if obstacle.pointInside(cellPointTopLeft):
                return False

        for line in lines:
            if (calculateIntersectPoint(cellPointTopLeft, cellPointTopRight, line[0], line[1]) or
                    calculateIntersectPoint(cellPointTopLeft, cellPointBottomLeft, line[0], line[1]) or
                    calculateIntersectPoint(cellPointBottomLeft, cellPointBottomRight, line[0], line[1]) or
                    calculateIntersectPoint(cellPointTopRight, cellPointBottomRight, line[0], line[1])):
                return False

        return True

    j = -1
    for pointY in range(0, worldHeight, int(cellsize)):
        j += 1
        i = 0
        for pointX in range(0, worldWidth, int(cellsize)):
            cellBounds = (pointX, pointY)
            grid[i][j] = isValidCell(cellBounds)
            i += 1

    return grid, dimensions