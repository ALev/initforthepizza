#PathPlanner.py - convert the map_list to a map of danger values in [0,1]
from Enums import *
from Direction import *

class PathPlanner:
	
	def __init__(self):
		pass

	def query_accessible_squares(self, map_list, bombers, player_index):
		x_max = len(map_list)
		y_max = len(map_list[0])

		my_pos = bombers[player_index]['position']

		accessible_squares = self.query_accessibility(map_list, [], my_pos, x_max, y_max)

		print accessible_squares

		return accessible_squares 
			
	def query_accessibility(self, map_list, accessible_squares, curr_pos, x_max, y_max):
		accessible_squares.append(curr_pos)		
		
		for move in Directions.values():
			if move.name == 'still': pass
			x = min(max(curr_pos[0] + move.dx,0),x_max)
			y = min(max(curr_pos[1] + move.dy,0),y_max)
			if (map_list[x][y] in WALKABLE) and ((x,y) not in accessible_squares):
				recurs_squares = self.query_accessibility(map_list, accessible_squares, (x,y), x_max, y_max)

		

		return accessible_squares
