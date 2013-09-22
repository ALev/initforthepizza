#PathPlanner.py - convert the map_list to a map of danger values in [0,1]
from Enums import *
from Direction import *
from globalvars import *

class PathPlanner:
	
	def __init__(self):
		pass

	def query_accessible_squares(self, map_list, bombers, player_index):
		my_pos = bombers[player_index]['position']

		accessible_squares = self.query_accessibility(map_list, [], my_pos)

		print accessible_squares

		return accessible_squares 
			
	def query_accessibility(self, map_list, accessible_squares, curr_pos):
		accessible_squares.append(curr_pos)		
		
		for move in Directions.values():
			if move.name == 'still': pass
			x = min(max(curr_pos[0] + move.dx,0),MAP_SIZE)
			y = min(max(curr_pos[1] + move.dy,0),MAP_SIZE)
			if (map_list[x][y] in WALKABLE) and ((x,y) not in accessible_squares):
				recurs_squares = self.query_accessibility(map_list, accessible_squares, (x,y))

		return accessible_squares

	def locate_accessible_objects(self, map_list, accessibility, curr_pos, goal):
		options = {}
		# if we're searching for a walkable square, just iterate over accessible squares		
		for square in accessibility:
			if ((goal == 'FIREUP' or 'BOMBUP' or 'POWERUP') and (map_list[square[0]][square[1]] == goal)) or \
			   ((goal == 'BLOCK') and (check_adjacency(map_list, square, goal))):
					options[manhattan_distance(curr_pos, square)] = square
					
		return options

	def check_adjacency(self, map_list, from_xy, goal):
		for move in Directions.values():
			if move.name == 'still': pass
			x = min(max(from_xy[0] + move.dx,0),MAP_SIZE)
			y = min(max(from_xy[1] + move.dy,0),MAP_SIZE)
			if map_list[x][y] == goal:
				return True
		return False

	def manhattan_distance(start, end):
		return (abs(start[0]-end[0])+abs(start[1]-end[1]))

	def is_opponent_accessible(self, map_list, bombers):
		accessible_squares = self.query_accessible_squares(map_list, bombers, bombers[0])

