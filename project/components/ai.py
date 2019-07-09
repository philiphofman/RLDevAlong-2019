"""
This is where all of our different monster AIs will go, presumably.
"""

class BasicMonster:
	"""Defines our basic monster behaviour."""
	
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