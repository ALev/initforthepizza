#DangerMap.py - convert the map_list to a map of danger values in [0,1]
from Enums import *
from Direction import *
from globalvars import *

class DangerMap:

	def __init__(self):
		pass

	def convert_to_danger_map(self, map_list, bombs, explosion_list):
		danger_map = [[0 for y in range(0,MAP_SIZE)] for x in range(0,MAP_SIZE)]
	
		bomb_clusters = []
		square_clusters = []

		for bomb_xy in bombs:
			skip_bomb = False
			for existing_cluster in bomb_clusters:
				if bomb_xy in existing_cluster:
					skip_bomb = True
					break
			if skip_bomb: pass
			
			new_bomb_clus, new_square_clus = self.query_bomb_cluster(map_list, bombs, [], [], bomb_xy)
			bomb_clusters.append(new_bomb_clus)
			square_clusters.append(new_square_clus)

		for bomb_cluster, square_cluster in zip(bomb_clusters, square_clusters):
			time_to_explode = min([bombs[bomb_xy]['time_left'] for bomb_xy in bomb_cluster])
			for square in square_cluster:
				danger_map[square[0]][square[1]] = self.danger_function(time_to_explode)

		for square in explosion_list:
			danger_map[square[0]][square[1]] = 1

		# self.print_map(danger_map)

		return danger_map 

	def danger_function(self,time_left):
		return 1 - time_left/15.0
			
	def query_bomb_cluster(self,map_list, bombs, bomb_cluster, square_cluster, bomb_xy):
		bomb_cluster.append(bomb_xy)
		square_cluster.append(bomb_xy)

		bomb_range = bombs[bomb_xy]['range']
		
		for move in Directions.values():
			if move.name == 'still': pass
			for range_inc in range(1,bomb_range+1):
				x = min(max(bomb_xy[0] + move.dx * range_inc,0),MAP_SIZE)
				y = min(max(bomb_xy[1] + move.dy * range_inc,0),MAP_SIZE)
				if (map_list[x][y] == Enums.MapItems.BOMB) and ((x,y) not in bomb_cluster):
					recurs_bombs, recurs_squares = self.query_bomb_cluster(map_list, bombs, bomb_cluster, square_cluster, (x,y))
					square_cluster.extend(recurs_squares)
					bomb_cluster.extend(recurs_bombs)
					break  #explosions won't go past 
				elif (map_list[x][y] in WALKABLE) and ((x,y) not in square_cluster):
					square_cluster.append((x,y))
				else:
					# can't keep going in this direction
					break

		return bomb_cluster, square_cluster

	def print_map(self, danger_map):
		# ok fuck. because we get the format in map[col][row], we have to transpose the whole thing in order to print.
		new_danger_map = [[0 for x in range(0,MAP_SIZE)] for y in range(0,MAP_SIZE)]
		for x in range(0,MAP_SIZE):
			for y in range(0,MAP_SIZE):
				new_danger_map[x][y] = danger_map[y][x]

		output_str = ""
		#new_file = open('home/anton/cogniteam/bomberman/initforthepizza/logs/danger_map','w')
		for col in new_danger_map:
			for value in col:
				output_str += "{:5.2f}".format(value)
			output_str += "\n"
		print output_str		
