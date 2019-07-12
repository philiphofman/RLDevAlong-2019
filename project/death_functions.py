import tcod as libtcod

from game_messages import Message
from game_states import GameStates
from render_functions import RenderOrder


def kill_player(player):
	"""Kills the player.
	
	Changes the player's ASCII character and color,
	and returns a string message and a Enum GameState.
	
	Args:
		player: The player Entity object to kill.
		
	Returns:
		A string death message and an Enum GameState.
	"""
	
	player.char = '%'
	player.color = libtcod.dark_red
	
	return Message('You died!', libtcod.red), GameStates.PLAYER_DEAD
	

def kill_monster(monster):
	"""Kills a monster.
	
	First creates a string death message based on the name
	of the monster, then changes the monster's ASCII character
	and color, stops it from blocking movement, removes the AI
	and Fighter components, changes the name to 'remains of
	(monster)', and changes RenderOrder to CORPSE.
	
	Args:
		monster: The monster Entity object to kill.
		
	Returns:
		A formatted string death message.
	"""
	
	death_message = Message('{0} is dead!'.format(monster.name.capitalize()), libtcod.orange)
	
	monster.char = '%'
	monster.color = libtcod.dark_red
	monster.blocks = False
	monster.fighter = None
	monster.ai = None
	monster.name = 'remains of ' + monster.name
	monster.render_order = RenderOrder.CORPSE
	
	return death_message