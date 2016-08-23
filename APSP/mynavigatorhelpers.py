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



def shortcutPath(source, dest, path, world, agent):
	### YOUR CODE GOES BELOW HERE ###
	
	flag = True
	while flag:
		flag = False
		for i in range(len(path) - 2):
			if clearShot(path[i], dest, world.getLines(), world.getPoints(), agent):
				return path[:i + 1]

			if clearShot(path[i], path[i + 2], world.getLines(), world.getPoints(), agent):
				path.remove(path[i + 1])
				flag = True
				break

	### YOUR CODE GOES BELOW HERE ###
	return path

def clearShot(p1, p2, worldLines, worldPoints, agent):
	### YOUR CODE GOES BELOW HERE ###

	agentRadius = agent.maxradius / 2
	if rayTraceWorldNoEndPoints(p1, p2, worldLines) == None:
		for point in worldPoints:
			if minimumDistance((p1, p2), point) < agentRadius:
				return False
		return True

	### YOUR CODE GOES ABOVE HERE ###
	return False


def mySmooth(nav):
	### YOUR CODE GOES BELOW HERE ###
	
	current = nav.agent.getLocation()
	target = nav.agent.moveTarget

	if clearShot(current, target, nav.world.getLines(), nav.world.getPoints(), nav.agent):
		nav.agent.moveToTarget(target)
		return True


	### YOUR CODE GOES ABOVE HERE ###
	return False



