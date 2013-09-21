import random
from Enums import *
from Direction import *

"""Behaviours are combinations of conditions which trigger the behaviour and actions to take"""
class Avoid_Death_Behaviour(object):

	def __init__(self, priority):
		self.priority = priority
		
	def check_conditions(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number):
		print("Check: Avoid Death")
					
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number):
		print("Action: Avoid Death")
		

class Bomb_A_Block_Behaviour(object):

	def __init__(self, priority):
		self.priority = priority
		
	def check_conditions(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number):
		print("Check: Bomb A Block")
		our_position = bombers[player_index]['position']

		for possible_move in Directions.values():
			if (possible_move.name != 'still'):
				possible_x = our_position[0] + possible_move.dx
				possible_y = our_position[1] + possible_move.dy
				if map_list[possible_x][possible_y] == "BLOCK":
					print("Conditions Met: Bomb A Block")
					return True
		return False
			
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number):
		valid_moves = []
		our_position = bombers[player_index]['position']
		
		for possible_move in Directions.values():
			if (possible_move.name != 'still'):
				possible_x = our_position[0] + possible_move.dx
				possible_y = our_position[1] + possible_move.dy

				if map_list[possible_x][possible_y] in WALKABLE:
					valid_moves.append(possible_move)
		
		print("Action: Bomb A Block")
		return valid_moves[random.randrange(0, len(valid_moves))].bombaction
		
		
class Random_Move_Behaviour(object):
	
	def __init__(self, priority):
		self.priority = priority
		pass
		
	def check_conditions(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number):
		print("Check: Random Move")

		if True:
			print("Conditions Met: Random Move")
			return True
		else:
			return False
		
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number):
		
		valid_moves = []
		our_position = bombers[player_index]['position']
		
		for possible_move in Directions.values():
			if (possible_move.name != 'still'):
				possible_x = our_position[0] + possible_move.dx
				possible_y = our_position[1] + possible_move.dy

				if map_list[possible_x][possible_y] in WALKABLE:
					valid_moves.append(possible_move)
		
		print("Action: Random Move")
		return valid_moves[random.randrange(0, len(valid_moves))].action
		
		# return Directions.values()[random.randrange(0, len(Directions))].action
		# return Directions['up'].action
		

class Do_Nothing_Behaviour(object):
	
	def __init__(self):
		self.priority = 0.0
		
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number):
		print("Action: Doing Nothing")
		return Directions['still'].action	