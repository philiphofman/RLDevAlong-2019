import tcod as libtcod

from game_states import GameStates


def handle_keys(key, game_state):
	"""Handles key presses during different game states.
	
	Args:
		key: An integer denoting a keycode (vk)
		game_state: An Enum denoting what game state it is.
		
	Returns:
		A dictionary key name.
	"""
	
	if game_state == GameStates.PLAYERS_TURN:
		return handle_player_turn_keys(key)
		
	elif game_state == GameStates.PLAYER_DEAD:
		return handle_player_dead_keys(key)
		
	elif game_state == GameStates.TARGETING:
		return handle_targeting_keys(key)
		
	elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
		return handle_inventory_keys(key)
	
	return {}


def handle_targeting_keys(key):
	"""Handles key presses during targeting.
	
	Args:
		key: An integer denoting a keycode (vk)
		
	Returns:
		A dictionary key name.
	"""

	if key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}
		
	return {}

	
def handle_inventory_keys(key):
	"""Handles key presses in the inventory.
	
	Args:
		key: An integer denoting a keycode (vk)
		
	Returns:
		A dictionary key name.
	"""
	
	index = key.c - ord('a')
	
	if index >= 0:
		return {'inventory_index': index}
		
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		# Alt+Enter: Toggle full screen
		return {'fullscreen': True}
	elif key.vk == libtcod.KEY_ESCAPE:
		# Exit the menu
		return {'exit': True}
		
		
	return {}
	
	
	
def handle_player_turn_keys(key):
	"""Checks if a key has been pressed on the player's turn.
	
	Args:
		key: An integer denoting a keycode (vk)
		
	Returns:
		A dictionary key name. Currently either coordinates in the
		(x, y) format, or a boolean value.
	"""
	
	# TODO: Replace with tcod.event. Check if Event code is complete first.
	key_char = chr(key.c)
	
	if key.vk == libtcod.KEY_UP or key_char == 'h':
		return {'move': (0, -1)}
	elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
		return {'move': (0, 1)}
	elif key.vk == libtcod.KEY_LEFT or key_char == 'k':
		return {'move': (-1, 0)}
	elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
		return {'move': (1, 0)}
	elif key_char == 'y':
		return {'move': (-1, -1)}
	elif key_char == 'u':
		return {'move': (1, -1)}
	elif key_char == 'b':
		return {'move': (-1, 1)}
	elif key_char == 'n':
		return {'move': (1, 1)}
		
	elif key_char == 'g':
		return {'pickup': True}
		
	elif key_char == 'i':
		return {'show_inventory': True}
	
	elif key_char == 'd':
		return {'drop_inventory': True}
		
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		# Alt+Enter: toggle full screen
		return {'fullscreen': True}
		
	elif key.vk == libtcod.KEY_ESCAPE:
		# Exit the game
		return {'exit': True}
		
	# No key was pressed
	return {}
	
	
def handle_player_dead_keys(key):
	"""Handles key presses during player's death.
	
	Args:
		key: An integer denoting a keycode (vk)
		
	Returns:
		A dictionary key name.
	"""
	
	key_char = chr(key.c)
	
	if key_char == 'i':
		return {'show_inventory': True}
		
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		# Alt+Enter: Toggle full screen
		return {'fullscreen': True}
	elif key.vk == libtcod.KEY_ESCAPE:
		# Exit the menu
		return {'exit': True}
		
	return {}
	
	
def handle_mouse(mouse):
	"""Returns which coordinates the left or right mouse button clicked on.
	
	Args:
		mouse: tcod Mouse object.
	
	Returns:
		A dictionary key name.
	"""
	
	(x, y) = (mouse.cx, mouse.cy)
	
	if mouse.lbutton_pressed:
		return {'left_click': (x, y)}
	elif mouse.rbutton_pressed:
		return {'right_click': (x, y)}
		
	return {}