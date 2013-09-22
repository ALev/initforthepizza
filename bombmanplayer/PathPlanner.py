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

		#print accessible_squares

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
			   ((goal == 'BLOCK') and (self.check_adjacency(map_list, square, goal))):
				new_dist = len(self.A_star(accessibility, curr_pos, square))
				options[new_dist] = square	
		return options

	def query_accessible_safezone(self, map_list, accessibility, curr_pos, danger_map):
		options = {}
		# if we're searching for a walkable square, just iterate over accessible squares		
		for square in accessibility:
			if danger_map[square[0]][square[1]] == 0: return True

		return False

	def check_adjacency(self, map_list, from_xy, goal):
		for move in Directions.values():
			if move.name == 'still': pass
			x = min(max(from_xy[0] + move.dx,0),MAP_SIZE)
			y = min(max(from_xy[1] + move.dy,0),MAP_SIZE)
			if map_list[x][y] == goal:
				return True
		return False

	def manhattan_distance(self,start, end):
		return (abs(start[0]-end[0])+abs(start[1]-end[1]))

	def is_opponent_accessible(self, map_list, bombers):
		accessible_squares = self.query_accessible_squares(map_list, bombers, 0)
		for square in accessible_squares:
			if (square[0],square[1]) == bombers[1]['position']: return True
		return False

	def A_star(self,accessibility, start, goal):
		closedset = []
		openset = [start]
		came_from = {}
		g_score = {}
		f_score = {}

		g_score[start] = 0
		f_score[start] = g_score[start] + self.manhattan_distance(start, goal)
	
		while len(openset) > 0:
			f_score_subset = {k: f_score[k] for k in openset}
			current = min(f_score_subset, key=f_score_subset.get)
			if current == goal:
				return self.reconstruct_path(came_from, goal)
		
			openset.remove(current)
			closedset.append(current)
		
			for move in Directions.values():
				if move.name == 'still': pass
				x = min(max(current[0] + move.dx,0),MAP_SIZE)
				y = min(max(current[1] + move.dy,0),MAP_SIZE)
				neighbor = (x,y)
			
				if neighbor in accessibility:
					tent_g_score = g_score[current] + 1
					if neighbor in closedset and (tent_g_score >= g_score[neighbor]): continue
			
					if (neighbor not in g_score) or tent_g_score < g_score[neighbor]:
						came_from[neighbor] = current
						g_score[neighbor] = tent_g_score
						f_score[neighbor] = g_score[neighbor] + self.manhattan_distance(neighbor, goal)
						if neighbor not in openset: openset.append(neighbor)
		return []

	def reconstruct_path(self, came_from, current_node):
		if current_node in came_from:
			path = self.reconstruct_path(came_from, came_from[current_node])
			path.append(current_node)
			return path
		else: 
			return [current_node]
