#Player.py ai
import random

from bombmanclient.Client import *
from Enums import *
from Direction import *

from Behaviours import *
from DangerMap import *
from PathPlanner import *

"""The Decider chooses which behaviour to do next"""		
class Decider(object):

	def __init__(self):
		
		print("******Setting Up Behaviours and Weighting Them!******")
		self.avoid_death = Avoid_Death_Behaviour(1.0)
		self.bomb_a_block = Bomb_A_Block_Behaviour(0.75)
		self.random_move = Random_Move_Behaviour(0.5)
		self.behaviours = [self.avoid_death, self.bomb_a_block, self.random_move]
		self.map_converter = DangerMap()
		self.path_planner = PathPlanner()
		
	def decide(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number):
		
		"""By default, we will do nothing"""
		self.action_to_take_next = Do_Nothing_Behaviour()
		
		"""Set up the DangerMap!"""
		danger_map = self.map_converter.convert_to_danger_map(map_list, bombs, explosion_list)

		"""Check accessible squares"""
		accessible_squares = self.path_planner.query_accessible_squares(map_list, bombers, player_index)

		print("******Decision Time!******")
		for behaviour in self.behaviours:
			if behaviour.check_conditions(map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares) == True and (behaviour.priority > self.action_to_take_next.priority):
				self.action_to_take_next = behaviour

		print("******Action Time!******")
		self.move = self.action_to_take_next.take_action(map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares)
		if self.move == None:
			self.move = self.random_move.take_action(map_list, bombs, powerups, bombers, explosion_list, player_index, move_number, danger_map, accessible_squares)
		return self.move


class PlayerAI():

	def __init__(self):
		self.blocks = []
		self.decider = Decider()

	def new_game(self, map_list, blocks_list, bombers, player_index):
		self.blocks = blocks_list[:]

	def get_move(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number):
		
		move = self.decider.decide(map_list, bombs, powerups, bombers, explosion_list, player_index, move_number)		
		return move
