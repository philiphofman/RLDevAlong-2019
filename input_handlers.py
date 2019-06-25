import tcod as libtcod # Import tcod library


def handle_keys(key): # Define a new fuction called handle_keys with one input (the key that has been pressed, if any)
	# Movement Keys
	if key. vk == libtcod.KEY_UP: # If the Up arrow key has been pressed
		return {'move': (0, -1)} # Return dictionary Move as X = 0 and Y = -1
	elif key.vk == libtcod.KEY_DOWN: # If the Down arrow key has been pressed
		return {'move': (0, 1)} # Return dictionary Move as X = 0 and Y = 1
	elif key.vk == libtcod.KEY_LEFT: # If the Left arrow key has been pressed
		return {'move': (-1, 0)} # Return dictionary Move as X = -1 and Y = 0
	elif key.vk == libtcod.KEY_RIGHT: # If the Right arrow key has been pressed
		return {'move': (1, 0)} # Return dictionary Move as X = 1 and Y = 0
		
	if key.vk == libtcod.KEY_ENTER and key.lalt: # If both the Enter and Left Alt key have been pressed together
		# Alt+Enter: toggle full screen
		return {'fullscreen': True} # Return dictionary Fullscreen as True
		
	elif key.vk == libtcod.KEY_ESCAPE: # If the Escape key has been pressed
		# Exit the game
		return {'exit': True} # Return dictionary Exit as True
		
	# No key was pressed
	return {} # Return empty dictionary, because something still has to be returned