from Enums import *
from Direction import *

"""Behaviours are combinations of conditions which trigger the behaviour and actions to take"""
class Avoid_Death_Behaviour(object):

	def __init__(self, priority):
		self.priority = priority
		
	def check_conditions(self):
		if 1 == 1:
			print("Conditions Met: Avoiding Death")
			return True
		else:
			return False
	
	def take_action(self):
		print("Action: Avoiding Death")
		

class Drop_Bomb_Behaviour(object):

	def __init__(self, priority):
		self.priority = priority
		
	def check_conditions(self):
		if 1 == 1:
			print("Conditions Met: Drop Bomb")
			return True
		else:
			return False
			
	def take_action(self):
		print("Action: Dropping Bomb")
		
		
class Random_Move_Behaviour(object):
	
	def __init__(self, priority):
		self.priority = priority
		pass
		
	def check_conditions(self):
		if 1 == 1:
			print("Conditions Met: Random Move")
			return True
		else:
			return False
		
	def take_action(self):
		print("Action: Random Move")
		return Directions['up'].bombaction
		

class Do_Nothing_Behaviour(object):
	
	def __init__(self):
		self.priority = 0.0
		
	def take_action(self):
		print("Action: Doing Nothing")		