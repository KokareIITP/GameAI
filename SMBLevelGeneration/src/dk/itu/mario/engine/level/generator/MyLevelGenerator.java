package dk.itu.mario.engine.level.generator;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Random;

import dk.itu.mario.MarioInterface.Constraints;
import dk.itu.mario.MarioInterface.GamePlay;
import dk.itu.mario.MarioInterface.LevelGenerator;
import dk.itu.mario.MarioInterface.LevelInterface;
import dk.itu.mario.engine.level.Level;
import dk.itu.mario.engine.level.MyLevel;

import dk.itu.mario.engine.PlayerProfile;

import dk.itu.mario.engine.sprites.SpriteTemplate;
import dk.itu.mario.engine.sprites.Enemy;

public class MyLevelGenerator {
	public int mapWidth = 205;
	public int mapHeight = 15;
	public int n = 15;
	public int k = 7; 
	public int crossOverIterations = 7;
	
	ArrayList<MyLevel> popList = new ArrayList<MyLevel>();
	
	public Level generateLevel(PlayerProfile playerProfile) {
					
		//// YOUR CODE GOES BELOW HERE ////
		
		Comparator<MyLevel> levelComp = new Comparator<MyLevel>() {
			public int compare(MyLevel level1, MyLevel level2) {
				double firstScore = playerProfile.evaluateLevel(level1);
				double secondScore = playerProfile.evaluateLevel(level2);
				if (firstScore == secondScore) {
					return 0;
				}
	            return (firstScore > secondScore) ?  -1 : 1;
	        }
		};
		
		for (int i = 0; i < n; i++) {
			MyLevel level = new MyLevel(mapWidth, mapHeight, new Random().nextLong(), 1, LevelInterface.TYPE_OVERGROUND);
			popList.add(level);
		}
				
		// start level gen:
		
		boolean levelNotFound = true;
		
		while (levelNotFound) {
			 
			// see if there is a good enough level:

			MyLevel[] popArray =  popList.toArray(new MyLevel[popList.size()]);
			Arrays.sort(popArray, levelComp); 
			MyLevel bestLevel = popArray[0];
			double score = playerProfile.evaluateLevel(bestLevel);
			if (score > .8) {
				levelNotFound = false;
				return (Level) bestLevel;
			}			
			
			// asexual reprod phase:
			
			for (int i = 0; i < k; i++) {
				MyLevel parentClone = popArray[i].clone();
				MyLevel child = asexReprod(parentClone);
				popList.add(child);									
			}
			
			// cross-over phase:
	
			for (int j = 0; j < crossOverIterations; j++) {
				MyLevel[] parents = new MyLevel[2];
				int firstParentIndex = 0; 
				for (int m = 0; m < 2; m++) { 
					int index = 0;
					while (new Random().nextInt(5) > 0) {
						if (index == popArray.length-1) {
							break;
						}						
						index++;
					}
					
					if (m == 1 && index == firstParentIndex) {
						if (index != popArray.length-1) {
							index++;
						}
					}
					if (m == 0) {
						firstParentIndex = index;
					}	
					
					parents[m] = popArray[index].clone();
				}
				MyLevel child2 = crossOver(parents[0], parents[1]);
				
				popList.add(child2);	
			}

			popArray = (MyLevel[]) Arrays.copyOfRange(popArray, 0, n);
		}

		//// YOUR CODE GOES ABOVE HERE ////
		return (Level)popList.get(0);
	}

	// Helper Functions	
	
	private MyLevel asexReprod(MyLevel parent) {
		MyLevel.Case myCase = MyLevel.Case.values()[new Random().nextInt(MyLevel.Case.COUNT)];
		int columnNumber = getValidColumn(parent, myCase);
		MyLevel child = setCase(parent, columnNumber, myCase);
		return child;
	}
	
	private int getValidColumn(MyLevel parent, MyLevel.Case myCase) {
		int column = new Random().nextInt(mapWidth); 
		if (column == 2) {
			column = 0;
		}
		return column;
	}
	
	private MyLevel crossOver(MyLevel firstParent, MyLevel secondParent) {
		int startIndex = firstParent.map.length / 2;
		MyLevel.Case[] childMap = firstParent.map.clone();
		
		MyLevel child = firstParent.clone();
		for (int col = startIndex; col < secondParent.map.length; col++) {
			MyLevel.Case secondParentCase = secondParent.map[col];
			child = setCase(child, col, secondParentCase);
		}
		return child;
	}
		
	private void resetColumn(MyLevel level, int col) {
		level.map[col] = MyLevel.Case.DEFAULT;
		
		for (int y = 0; y <= 12; y++) {
			level.setBlock(col, y, Level.EMPTY);			
		}
		level.setBlock(col, 13, Level.HILL_TOP);
		level.setBlock(col, 14, Level.GROUND);
	}
	
	private MyLevel setCase(MyLevel level, int col, MyLevel.Case myCase) {		
		resetColumn(level, col);
		level.map[col] = myCase;
		
		if (myCase == MyLevel.Case.COIN) {
			level.setBlock(col, 8, Level.COIN);
			level.setBlock(col, 9, Level.COIN);
			level.setBlock(col, 10, Level.COIN);
			level.setBlock(col, 11, Level.COIN);
			level.setBlock(col, 12, Level.COIN);
		}
		else if (myCase == MyLevel.Case.ENEMY) {
			level.setSpriteTemplate(col, 12, new SpriteTemplate(Enemy.ENEMY_GREEN_KOOPA,false));
		}
		else if (myCase == MyLevel.Case.ROCK) {
			level.setBlock(col, 12, Level.ROCK);
		}
		else if (myCase == MyLevel.Case.CANNON) {
			level.setBlock(col, 12, Level.CANNON_TOP);
		}
		else if (myCase == MyLevel.Case.GAP) {
			level.setBlock(col, 13, Level.EMPTY);
			level.setBlock(col, 14, Level.EMPTY);
		}
		
		return level;
	}
}