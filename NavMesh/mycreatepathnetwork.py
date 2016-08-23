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

import sys, pygame, math, numpy, random, time, copy, operator
from pygame.locals import *

from constants import *
from utils import *
from core import *
from random import shuffle

# Creates a pathnode network that connects the middlepoints of convex hulls together
def myCreatePathNetwork(world, agent = None):
	nodes = []
	edges = []
	polys = []

	polys = polygonCreating(world, polys) 
	
	flag = True
	while flag:
		flag = False
		for polygon1 in polys:
			for polygon2 in polys:
				if polygon1 == polygon2: continue

				if polygonsAdjacent(polygon1, polygon2):
					points = []
					polygon = []
					for point in polygon1:
						points.append(point)
					for point in polygon2:
						if point not in points:
							points.append(point)
					newpolygon = polyPointSorting(points)
					if isConvex(newpolygon):
						polys.remove(polygon1)
						polys.remove(polygon2)
						polys.append(newpolygon)
						flag = True
						break
			if flag: break

	for polygon in polys:
		polynodes = []
		for i in range(len(polygon)):
			obstacleCheck = False
			if i >= len(polygon) - 1:
				middlepoint = ((polygon[i][0]+polygon[0][0])/2, (polygon[i][1]+polygon[0][1])/2)
				for obstacle in world.obstacles:
					if (polygon[i], polygon[0]) in obstacle.getLines() or (polygon[0], polygon[i]) in obstacle.getLines():
						obstacleCheck = True
						break
				if not obstacleCheck:
					nodes.append(middlepoint)
					polynodes.append(middlepoint)
			else:
				middlepoint = ((polygon[i][0]+polygon[i+1][0])/2, (polygon[i][1]+polygon[i+1][1])/2)
				for obstacle in world.obstacles:
					if (polygon[i], polygon[i+1]) in obstacle.getLines() or (polygon[i+1], polygon[i]) in obstacle.getLines():
						obstacleCheck = True
						break
				if not obstacleCheck:
					nodes.append(middlepoint)
					polynodes.append(middlepoint)

		edges = addEdges(world, edges, polynodes)

	return nodes, edges, polys

def polygonCreating(world, polys):
	worldnodes = world.getPoints()
	shuffle(worldnodes) 
	for node1 in worldnodes:
		for node2 in worldnodes:
			for node3 in worldnodes:
				if node1 == node2 or node1 == node3 or node2 == node3: continue
				if not polygonCollision(node1, node2, node3, world, polys):
					if (node1, node2, node3) not in polys and (node1, node3, node2) not in polys and (node2, node1, node3) not in polys and (node2, node3, node1) not in polys and (node3, node1, node2) not in polys and (node3, node2, node1) not in polys:
						polys.append((node1, node2, node3))
	return polys

def polygonCollision(node1, node2, node3, world, polygons):
	worldlines = world.getLines()
	for (n1, n2, n3) in polygons:
		worldlines.extend(((n1, n2), (n1, n3), (n2, n3)))

	condition1 = (node1, node2) not in worldlines and (node2, node1) not in worldlines
	condition2 = (node1, node3) not in worldlines and (node3, node1) not in worldlines
	condition3 = (node2, node3) not in worldlines and (node3, node2) not in worldlines
	condition4 = condition1 and rayTraceWorldNoEndPoints(node1, node2, worldlines) != None
	condition5 = condition2 and rayTraceWorldNoEndPoints(node1, node3, worldlines) != None
	condition6 = condition3 and rayTraceWorldNoEndPoints(node2, node3, worldlines) != None

	if condition4 or condition5 or condition6:
		return True

	for obstacle in world.obstacles:
		if pointInsidePolygonLines(((node1[0]+node2[0])/2, (node1[1]+node2[1])/2), obstacle.getLines()) and condition1:
			return True
		elif pointInsidePolygonLines(((node1[0]+node3[0])/2, (node1[1]+node3[1])/2), obstacle.getLines()) and condition2:
			return True
		elif pointInsidePolygonLines(((node2[0]+node3[0])/2, (node2[1]+node3[1])/2), obstacle.getLines()) and condition3:
			return True

		middlepoint = [0,0]
		for point in obstacle.getPoints():
			middlepoint[0] += point[0]
			middlepoint[1] += point[1]
		middlepoint[0] /= len(obstacle.getPoints())
		middlepoint[1] /= len(obstacle.getPoints())
		if pointInsidePolygonPoints(middlepoint, (node1, node2, node3)):
			return True

	return False

def polyPointSorting(points):
	polygon = []
	middlepoint = [0,0]
	for point in points:
		middlepoint[0] += point[0]
		middlepoint[1] += point[1]
	middlepoint[0] /= len(points)
	middlepoint[1] /= len(points)

	def angleFinding(point):
		return math.atan2(middlepoint[1]-point[1], middlepoint[0]-point[0])*180/math.pi

	polygon = sorted(points, key = angleFinding)
	return polygon

def addEdges(world, edges, polynodes):
	for i in range(len(polynodes)):
			if i >= len(polynodes) - 1:
				if not tooclose(world.obstacles, (polynodes[i], polynodes[0]), world.movers[0].maxradius):
					edges.append((polynodes[i], polynodes[0]))
			else:
				if not tooclose(world.obstacles, (polynodes[i], polynodes[i+1]), world.movers[0].maxradius):
					edges.append((polynodes[i], polynodes[i+1]))
	return edges

def tooclose(obstacles, line, radius):
	for obstacle in obstacles:
		for point in obstacle.getPoints():
			if minimumDistance(line, point)<radius:
				return True
	return False

