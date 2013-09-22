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
			if danger_map[possible_x][possible_y] > 0.8:
				print("Conditions Met: Avoid Death")
				return True

					
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		print("Action: Avoid Death")
		
		our_position = bombers[player_index]['position']
		
		for possible_move in Directions.values():
			possible_x = our_position[0] + possible_move.dx
			possible_y = our_position[1] + possible_move.dy
			
			if (danger_map[possible_x][possible_y] < 0.8) and (map_list[possible_x][possible_y] in WALKABLE):
				return possible_move.action
		
		

class Bomb_A_Block_Behaviour(object):

	def __init__(self, priority):
		self.priority = priority
		
	def check_conditions(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		# print("Check: Bomb A Block")

		path_planner = PathPlanner()
		if path_planner.check_adjacency(map_list, bombers[player_index]['position'], 'BLOCK'):
			if (move_number < 40) and (len(bombs) == 0):
				print("Conditions Met: Bomb A Block")
				return True
			elif (move_number > 40):
				print("Conditions Met: Bomb A Block")
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
		
		valid_moves = []
		our_position = bombers[player_index]['position']
		
		for possible_move in Directions.values():
			if (possible_move.name != 'still'):
				possible_x = our_position[0] + possible_move.dx
				possible_y = our_position[1] + possible_move.dy

				if map_list[possible_x][possible_y] in WALKABLE:
					valid_moves.append(possible_move)
		
		print("Action: Random Move")
		if len(valid_moves) > 0:
			return valid_moves[random.randrange(0, len(valid_moves))].action
		
		# return Directions.values()[random.randrange(0, len(Directions))].action
		# return Directions['up'].action
		

class Do_Nothing_Behaviour(object):
	
	def __init__(self):
		self.priority = 0.0
		
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		print("Action: Doing Nothing")
		return Directions['still'].action	
