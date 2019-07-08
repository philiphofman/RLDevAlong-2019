import tcod as libtcod

def handle_keys(key):
	"""Checks if a key (up, down, left, right, enter+leftalt, or escape) has been pressed.
	
	Args:
		key: An integer denoting a keycode (vk)
		
	Return:
		A dictionary key name. Currently either coordinates in the
		(x, y) format, or a boolean value.
	"""
	
	# TODO: Replace with tcod.event. Check if Event code is complete first.
	key_char = chr(key.c)
	
	if key.vk == libtcod.KEY_UP or key_char == 'i':
		return {'move': (0, -1)}
	elif key.vk == libtcod.KEY_DOWN or key_char == 'k':
		return {'move': (0, 1)}
	elif key.vk == libtcod.KEY_LEFT or key_char == 'j':
		return {'move': (-1, 0)}
	elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
		return {'move': (1, 0)}
	elif key_char == 'u':
		return {'move': (-1, -1)}
	elif key_char == 'o':
		return {'move': (1, -1)}
	elif key_char == 'm':
		return {'move': (-1, 1)}
	elif key_char == ',':
		return {'move': (1, 1)}
		
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		# Alt+Enter: toggle full screen
		return {'fullscreen': True}
		
	elif key.vk == libtcod.KEY_ESCAPE:
		# Exit the game
		return {'exit': True}
		
	# No key was pressed
	return {}