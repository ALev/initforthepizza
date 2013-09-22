import random
from Enums import *
from Direction import *
from PathPlanner import *

"""Behaviours are combinations of conditions which trigger the behaviour and actions to take"""
class Avoid_Death_Behaviour(object):

	def __init__(self, priority):
		self.priority = priority
		
	def check_conditions(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		# print("Check: Avoid Death")
		
		our_position = bombers[player_index]['position']
		
		for possible_move in Directions.values():
			possible_x = our_position[0] + possible_move.dx
			possible_y = our_position[1] + possible_move.dy
			if danger_map[possible_x][possible_y] > 0.7:
				print("Conditions Met: Avoid Death")
				return True

					
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		print("Action: Avoid Death")
		
		our_position = bombers[player_index]['position']
		
		for possible_move in Directions.values():
			possible_x = our_position[0] + possible_move.dx
			possible_y = our_position[1] + possible_move.dy
			
			if (danger_map[possible_x][possible_y] < 0.7) and (map_list[possible_x][possible_y] in WALKABLE):
				return possible_move.action
		
		

class Bomb_A_Block_Behaviour(object):

	def __init__(self, priority):
		self.priority = priority
		
	def check_conditions(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		# print("Check: Bomb A Block")
		
		our_position = bombers[player_index]['position']
		current_ambient_danger_level = 0
		ambient_danger_threshold = 0.1 #This regulates how trigger happy and dense block bombs will be
		
		for i in range(-5,6):
			square_x = our_position[0] + i
			square_y = our_position[1] + i
			if (0 <= square_x <= 16) and (0 <= square_y <= 16):
				print(danger_map[square_x][square_y])
				current_ambient_danger_level += danger_map[square_x][square_y]
		
		print("Ambient danger:")
		print(current_ambient_danger_level)
		print("Less than threshold?")
		print(current_ambient_danger_level < ambient_danger_threshold)
		
		path_planner = PathPlanner()
		if path_planner.check_adjacency(map_list, bombers[player_index]['position'], 'BLOCK') & (current_ambient_danger_level < ambient_danger_threshold):
			# if (move_number < 40) and (len(bombs) == 0):
			# 	print("Conditions Met: Bomb A Block")
			# 	return True
			# elif (move_number > 40):
			# 	print("Conditions Met: Bomb A Block")
				return True
		return False
			
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		valid_moves = []
		our_position = bombers[player_index]['position']
		
		for possible_move in Directions.values():
			if (possible_move.name != 'still'):
				possible_x = our_position[0] + possible_move.dx
				possible_y = our_position[1] + possible_move.dy

				if map_list[possible_x][possible_y] in WALKABLE:
					adjacency_accumulator = 0 
					for adjacent_square in Directions.values():
						adjacent_square_x = possible_x + adjacent_square.dx
						adjacent_square_y = possible_y + adjacent_square.dy
						if map_list[adjacent_square_x][adjacent_square_y] not in WALKABLE:
							adjacency_accumulator += 1
					if adjacency_accumulator < 3:	
						valid_moves.append(possible_move)
		
		print("Action: Bomb A Block")
		if len(valid_moves) > 0:
			return valid_moves[random.randrange(0, len(valid_moves))].bombaction


class Open_Space_Bombing_Behaviour(object):

	def __init__(self, priority):
		self.priority = priority
		self.path_planner = PathPlanner()
		
	def check_conditions(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		# print("Check: Open Space Bombing")

		our_position = bombers[player_index]['position']
		adjacency_accumulator = 0
		
		for adjacent_square in Directions.values():
			if (adjacent_square.name != 'still'):
				adjacent_x = our_position[0] + adjacent_square.dx
				adjacent_y = our_position[1] + adjacent_square.dy

				if map_list[adjacent_x][adjacent_y] in WALKABLE:
					adjacency_accumulator += 1
		
		if adjacency_accumulator == 4 and self.path_planner.is_opponent_accessible(map_list, bombers):
			print("Conditions Met: Open Space Bombing")
			return True
		else:
			return False
		
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		
		valid_moves = []
		our_position = bombers[player_index]['position']

		
		for possible_move in Directions.values():
			adjacency_accumulator = 0
			if (possible_move.name != 'still'):
				possible_x = our_position[0] + possible_move.dx
				possible_y = our_position[1] + possible_move.dy
				
				for adjacent_square in Directions.values():
					adjacent_square_x = possible_x + adjacent_square.dx
					adjacent_square_y = possible_y + adjacent_square.dy
					if map_list[adjacent_square_x][adjacent_square_y] not in WALKABLE:
						adjacency_accumulator += 1
				if adjacency_accumulator < 3:	
					valid_moves.append(possible_move)
		
		print("Action: Open Space Bombing")
		if len(valid_moves) > 0:
			return valid_moves[random.randrange(0, len(valid_moves))].bombaction
				
		
class Seek_Block_Behaviour(object):
	
	def __init__(self, priority):
		self.priority = priority
		pass
		
	def check_conditions(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):

		if True:
			print("Conditions Met: Seek Block")
			return True
		else:
			return False
		
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		
		print("Action: Seek Block")

class Random_Move_Behaviour(object):
	
	def __init__(self, priority):
		self.priority = priority
		pass
		
	def check_conditions(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		# print("Check: Random Move")

		if True:
			print("Conditions Met: Random Move")
			return True
		else:
			return False
		
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		
		print("Action: Random Move")
		
		best_moves = []
		our_position = bombers[player_index]['position']
		lowest_danger_value = 1
		
		for possible_move in Directions.values():
			destination_x = our_position[0] + possible_move.dx
			destination_y = our_position[1] + possible_move.dy
			if map_list[destination_x][destination_y] in WALKABLE:
				if danger_map[destination_x][destination_y] < lowest_danger_value:
					best_moves = []
					best_moves.append(possible_move)
					lowest_danger_value = danger_map[destination_x][destination_y]
				elif danger_map[destination_x][destination_y] == lowest_danger_value:
					best_moves.append(possible_move)
			
		if len(best_moves) > 1:
			for move in best_moves:
				if move.name == 'still':
					best_moves.remove(move)
		
		if len(best_moves) > 0:
			return best_moves[random.randrange(0, len(best_moves))].action
		

class Do_Nothing_Behaviour(object):
	
	def __init__(self):
		self.priority = 0.0
		
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		print("Action: Doing Nothing")
		return Directions['still'].action	
