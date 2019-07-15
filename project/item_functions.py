import tcod as libtcod

from game_messages import Message


def heal(*args, **kwargs):
	"""Heal entity by some amount and display message.
	
	Args:
		*args: Entity object that's using the item.
		**kwargs: Int extracted amount from kwargs.
		
	Returns:
		List with dictionaries.
	"""
	
	entity = args[0]
	amount = kwargs.get('amount')
	
	results = []
	
	if entity.fighter.hp == entity.fighter.max_hp:
		results.append({'consumed': False, 'message': Message('You are already at full health.', libtcod.yellow)})
	
	else:
		entity.fighter.heal(amount)
		results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', libtcod.green)})
		
		
	return results