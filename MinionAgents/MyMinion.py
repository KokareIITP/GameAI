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
from moba import *


class MyMinion(Minion):
	
	def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
		Minion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)
		self.states = [Idle]
		### Add your states to self.states (but don't remove Idle)
		### YOUR CODE GOES BELOW HERE ###
		self.states.append(MoveToTower)
		self.states.append(MoveToBase)
		self.states.append(AttackTower)
		self.states.append(AttackBase)
		self.states.append(Taunt)
		### YOUR CODE GOES ABOVE HERE ###

	def start(self):
		Minion.start(self)
		self.changeState(Idle)



############################
### Idle
###
### This is the default state of MyMinion. The main purpose of the Idle state is to figure out what state to change to and do that immediately.

class Idle(State):
	
	def enter(self, oldstate):
		State.enter(self, oldstate)
		# stop moving
		self.agent.stopMoving()
	
	def execute(self, delta = 0):
		State.execute(self, delta)
		### YOUR CODE GOES BELOW HERE ###
		base = self.agent.world.getEnemyBases(self.agent.getTeam())
		print "Aready Spawned: " + str(base[0].numSpawned)
		towers = self.agent.world.getEnemyTowers(self.agent.getTeam())

		if towers is not None and len(towers) > 0: 
				self.agent.changeState(MoveToTower, towers, base)
		elif len(base) > 0: 
			self.agent.changeState(MoveToBase, base)
		else: 
			self.agent.stopMoving()

		### YOUR CODE GOES ABOVE HERE ###
		return None

##############################
### Taunt
###
### This is a state given as an example of how to pass arbitrary parameters into a State.
### To taunt someome, Agent.changeState(Taunt, enemyagent)

class Taunt(State):

	def parseArgs(self, args):
		self.victim = args[0]

	def execute(self, delta = 0):
		if self.victim is not None:
			print "Hey " + str(self.victim) + ", I don't like you!"
		self.agent.changeState(Idle)

##############################
### YOUR STATES GO HERE:

##############################
### MoveToTower
###
### This is a state to make an agent move to the nearest tower.

class MoveToTower(State):

	def enter(self, oldstate):
		State.enter(self, oldstate)
		if (self.towers is not None):
			if (self.towers[0] is not None):
				self.agent.navigateTo(self.towers[0].position)
		elif (self.base is not None):
			self.agent.navigateTo(self.base[0].position)

	def parseArgs(self, args):
		self.towers = args[0]
		self.base = args[1]

	def execute(self, delta = 0):
		self.agent.shoot()
		# REPLANNING 
		# Get Minion Locations	
		currentPosition = self.agent.getLocation()
		destinationPosition = self.agent.getMoveTarget()

		self.towers = self.agent.world.getEnemyTowers(self.agent.getTeam())

		if currentPosition == destinationPosition:
			if (self.towers is not None):
				if (len(self.towers) > 0):
					self.agent.navigateTo(self.towers[0].position)
			elif (self.base is not None):
				self.agent.navigateTo(self.base[0].position)
		elif destinationPosition is None:
			if (self.towers is not None):
				if (len(self.towers) > 0):
					self.agent.navigateTo(self.towers[0].position)
			elif (self.base is not None):
				self.agent.navigateTo(self.base[0].position)
		elif (rayTraceWorld(currentPosition, destinationPosition, self.agent.world.getGates()) is not None):
			if (self.towers is not None):
				if (len(self.towers) > 0):
					self.agent.navigateTo(self.towers[0].position)
			elif (self.base is not None):
				self.agent.navigateTo(self.base[0].position)

		if self.towers is not None:
			if len(self.towers) > 0:
				if distance(self.agent.getLocation(), self.towers[0].position) <= 150:
					self.agent.changeState(AttackTower, self.towers)
		elif self.base is not None:
			if len(self.base) > 0: 
				if distance(self.agent.getLocation(), self.base[0].position) <= 150:
					self.agent.changeState(AttackBase, self.base)


##############################
### AttackTower
###
### This is a state where the agent attacks the tower until it is destroyed.

class AttackTower(State):

	def parseArgs(self, args):
		self.towers = args[0]

	def execute(self, delta = 0):
		newTowers = self.agent.world.getEnemyTowers(self.agent.getTeam())
		if self.towers <> newTowers:
			self.agent.changeState(Idle)

		if self.towers is not None and len(self.towers) > 0:
			self.agent.turnToFace(self.towers[0].position)
			self.agent.shoot()
			if (random.randint(0,20) <= 4):
				self.agent.stopMoving()
		if len(self.towers) == 0: 
			self.agent.changeState(Idle)


##############################
### MoveToBase
###
### This is a state to make an agent move to the base.

class MoveToBase(State):

	def enter(self, oldstate):
		State.enter(self, oldstate)
		if (self.base is not None):
			self.agent.navigateTo(self.base[0].position)

	def parseArgs(self, args):
		self.base = args[0]

	def execute(self, delta = 0):
		# REPLANNING 
		self.base = self.agent.world.getEnemyBases(self.agent.getTeam())

		# Get Minion Locations	
		currentPosition = self.agent.getLocation()
		destinationPosition = self.agent.getMoveTarget()

		if currentPosition == destinationPosition:
			if (self.base is not None):
				if len(base) > 0:
					self.agent.navigateTo(self.base[0].position)
		elif destinationPosition is None:
			if (self.base is not None):
				if len(base) > 0:
					self.agent.navigateTo(self.base[0].position)
		elif (rayTraceWorld(currentPosition, destinationPosition, self.agent.world.getGates()) is not None):
			if (self.base is not None):
				if len(base) > 0:
					self.agent.navigateTo(self.base[0].position)

		if self.base is not None:
			if len(self.base) > 0:
				if distance(self.agent.getLocation(), self.base[0].position) <= 150:
					self.agent.changeState(AttackBase, self.base)
		elif self.agent.world.getEnemyNPCs(self.agent.getTeam()) is not None:
			for npc in self.agent.world.getEnemyNPCs(self.agent.getTeam()):
				if (distance(self.agent.position, npc.position) <= 150):
					self.agent.changeState(AttackMinion, npc.position)
					break		


##############################
### AttackBase
###
### This is a state where the agent attacks the base until it is destroyed.

class AttackBase(State):

	def parseArgs(self, args):
		self.Base = args[0]

	def execute(self, delta = 0):
		self.agent.turnToFace(self.Base[0].position)
		self.agent.shoot()
		if (random.randint(0,20) <= 4):
			self.agent.stopMoving()


