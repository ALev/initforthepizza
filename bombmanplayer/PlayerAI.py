#Player.py ai
import random

from bombmanclient.Client import *
from Enums import *
from Direction import *

class PlayerAI():

	def __init__(self):
		self.blocks = []

	def new_game(self, map_list, blocks_list, bombers, player_index):
		self.blocks = blocks_list[:]

	def get_move(self, map_list, bombs, powerups, bombers, explosion_list, player_index, move_number):
		bombMove = False
		my_position = bombers[player_index]['position']

		# updating the list of blocks
		for explosion in explosion_list:
			if explosion in self.blocks: 
				self.blocks.remove(explosion)

		validmoves = []
		neighbour_blocks = [] 

		# find out which directions Bomber can move to.
		for move in Directions.values():
			x = my_position[0] + move.dx
			y = my_position[1] + move.dy

			# Checks to see if neighbours are walkable, and stores the neighbours which are blocks
			if map_list[x][y] in WALKABLE:
				# walkable is a list in enums.py which indicates what type of tiles are walkable
				validmoves.append(move)
			elif (x, y) in self.blocks: 
				neighbour_blocks.append((x, y))

		# place a bomb if there are blocks that can be destroyed
		if len(neighbour_blocks) > 0:
			bombMove = True

		# there's no where to move to
		if len(validmoves) == 0: 
			return Directions['still'].action

		# can move somewhere, so choose a tile randomly
		move = validmoves[random.randrange(0, len(validmoves))]

		if bombMove: 
			return move.bombaction
		else: 
			return move.action

	def path_exists(start, end, map_list):
		open_list = [start]
		visited = []

		while len(open_list) != 0:
			current = open_list.pop(0)

			for direction in Directions.values():
				x = current[0] + direction.dx
				y = current[1] + direction.dy

				if (x, y) == end: 
					return True

				if (x, y) in visited: 
					continue

				if map_list[x][y] in walkable: 
					open_list.append((x, y))

				visited.append((x, y))

		return False

	def manhattan_distance(start, end):
		return (abs(start[0]-end[0])+abs(start[1]-end[1]))
		
