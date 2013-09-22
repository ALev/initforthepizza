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
	
		our_position = bombers[player_index]['position']
		
		path_planner = PathPlanner()
		if path_planner.check_adjacency(map_list, bombers[player_index]['position'], 'BLOCK'):
			
			self.moves_we_could_take = []
			for possible_move in Directions.values():
				possible_x = our_position[0] + possible_move.dx
				possible_y = our_position[1] + possible_move.dy
				if map_list[possible_x][possible_y] in WALKABLE:
					if (path_planner.query_safe_bomb_drop(map_list, bombs, bombers, explosion_list, possible_move, player_index) == True):
						self.moves_we_could_take.append(possible_move)
					
			if len(self.moves_we_could_take) > 0:
					return True

		return False
			
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		print("Action: Bomb A Block")

		if len(self.moves_we_could_take) > 0:
			return self.moves_we_could_take[random.randrange(0, len(self.moves_we_could_take))].bombaction


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
			
			self.moves_we_could_take = []
			for possible_move in Directions.values():
				possible_x = our_position[0] + possible_move.dx
				possible_y = our_position[1] + possible_move.dy
				if (self.path_planner.query_safe_bomb_drop(map_list, bombs, bombers, explosion_list, possible_move, player_index) == True):
					self.moves_we_could_take.append(possible_move)
				if len(self.moves_we_could_take) > 0:
					print("Conditions Met: Open Space Bombing")
					return True
		else:
			return False
		
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):		
		
		print("Action: Open Space Bombing")
		if len(self.moves_we_could_take) > 0:
			return self.moves_we_could_take[random.randrange(0, len(self.moves_we_could_take))].bombaction
				
		
class Seek_Powerup_Behaviour(object):
	
	def __init__(self, priority):
		self.priority = priority
		self.path_planner = PathPlanner()
		
		
	def check_conditions(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):

		self.options = self.path_planner.locate_accessible_objects(map_list, accessible_squares, bombers[player_index]['position'], 'POWERUP')

		if len(self.options)==0: return False

		print("Conditions Met: Seek Powerup")
		return True
		
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		
		if len(self.options)>0:
			goal = self.options[min(self.options)]
			my_pos = bombers[player_index]['position']
			path = self.path_planner.A_star(accessible_squares, my_pos, goal)
			
			if len(path) < 2:
				print("Error with the path planner for powerup search.")
				return

			next_action = path[1] 
			
			for move in Directions.values():
				if move.name == 'still': pass
				x = min(max(my_pos[0] + move.dx,0),MAP_SIZE)
				y = min(max(my_pos[1] + move.dy,0),MAP_SIZE)
				if (x,y) == next_action:
					print("Action: Seek Powerup")
					return move.action
					
class Seek_Block_Behaviour(object):
	
	def __init__(self, priority):
		self.priority = priority
		self.path_planner = PathPlanner()
		
		
	def check_conditions(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):

		self.options = self.path_planner.locate_accessible_objects(map_list, accessible_squares, bombers[player_index]['position'], 'BLOCK')

		if len(self.options)==0: return False

		print("Conditions Met: Seek Block")
		return True
		
	def take_action(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares):
		
		if len(self.options)>0:
			goal = self.options[min(self.options)]
			my_pos = bombers[player_index]['position']
			path = self.path_planner.A_star(accessible_squares, my_pos, goal)
			
			if len(path) < 2:
				print("Error with the path planner for block search.")
				return

			next_action = path[1] 
			
			for move in Directions.values():
				if move.name == 'still': pass
				x = min(max(my_pos[0] + move.dx,0),MAP_SIZE)
				y = min(max(my_pos[1] + move.dy,0),MAP_SIZE)
				if (x,y) == next_action:
					print("Action: Seek Block")
					return move.action

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
