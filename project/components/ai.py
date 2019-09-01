"""
This is where all of our different monster AIs go.
"""

import tcod as libtcod

from random import randint

from game_messages import Message



class BasicMonster:
	"""Contains everything for Basic monster AI behaviour."""
	
	def take_turn(self, target, fov_map, game_map, entities):
		"""Defines what the monster will do on its turn.
		
		We extend the attack results and damage results to ensure
		one list of items is returned, rather than a list comprised
		of many small lists, which would make iterating through it
		much harder.
		
		Args:
			target: The Entity object the monster will move towards.
			fov_map: The Map object used to calculate FOV.
			game_map: The Map object used to actually display the game.
			entities: The list containing Entity objects.
			
		Returns:
			A list containing the attack results.
		"""
		
		results = []
		
		monster = self.owner
		
		if fov_map.fov[monster.y, monster.x]:
			
			if monster.distance_to(target) >= 2:
				monster.move_astar(target, entities, game_map)
				
			elif target.fighter.hp > 0:
				attack_results = monster.fighter.attack(target)
				results.extend(attack_results)
				
		return results
		
		
class ConfusedMonster:
	"""Contains everything for Confused monster AI behaviour.	"""
	
	def __init__(self, previous_ai, number_of_turns=10):
		"""Inits some values for the Confused AI.
		
		Args:
			previous_ai: What AI the monster was using last.
			number_of_turns: How long Confusion lasts.
		"""
		self.previous_ai = previous_ai
		self.number_of_turns = number_of_turns
		
		
	def take_turn(self, target, fov_map, game_map, entities):
		"""Runs one turn of Confused AI.
		
			Makes the monster Confused for a set number of
			turns. It wanders around in a random direction or
			stays put.
		
		Args:
			target: 
			fov_map: TCOD map used for FOV calculations.
			game_map: TCOD map used as the game map.
			entities: List of entities present on the map.
		"""
		
		results = []
		
		if self.number_of_turns > 0:
			random_x = self.owner.x + randint(0,2) - 1
			random_y = self.owner.y + randint(0,2) - 1
			
			if random_x != self.owner.x and random_y != self.owner.y:
				self.owner.move_towards(random_x, random_y, game_map, entities)
				
			self.number_of_turns -= 1
			
		else:
			self.owner.ai = self.previous_ai
			results.append({'message': Message('The {0} is no longer confused!'.format(self.owner.name), libtcod.red)})
			
		return results