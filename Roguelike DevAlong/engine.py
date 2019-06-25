import tcod as libtcod # Import tcod library

from entity import Entity # Import Entity class from the entity.py script
from input_handlers import handle_keys # Import a function (handle_keys) from the input_handlers.py script
from map_objects.game_map import GameMap # Import GameMap class from game_map.py script in map_objects folder
from render_functions import clear_all, render_all # Import functions from the render_functions.py script
from fov_functions import initialize_fov, recompute_fov


def main():
	screen_width = 80 # Create variable and set Screen Width
	screen_height = 50 # Create variable and set Screen Height
	map_width = 80 # Create variable and set Map Width
	map_height = 45 # Create variable and set Map Height
	
	room_max_size = 10
	room_min_size = 6
	max_rooms = 30
	
	fov_algorithm = 0
	fov_light_walls = True
	fov_radius = 10
	fov_recompute = True
	
	colors = { # Create new dictionary for colors
		'dark_wall': libtcod.Color(0, 0, 100), # Don't forget commas between separate entries in a dictionary, even if they're above and below each other!
		'dark_ground': libtcod.Color(50, 50, 150),
		'light_wall': libtcod.Color(130, 110, 50),
		'light_ground': libtcod.Color(200, 180, 50)
	}
	
	
	player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white) # Define the player variable as a new entity with coordinates x, y, ASCII symbol, and color
	npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow) # Define the NPC variable as a new entity with coordinates x, y, ASCII symbol, and color
	entities = [npc, player] # Create a list entities that holds all defined entities

	libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD) # Set custom ASCII character PNG image to use

	libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False) # Create the window, window size, window title, and set fullscreen
	
	con = libtcod.console_new(screen_width, screen_height) # Create a new console that has the dimensions defined in screen_width and screen_height
	
	game_map = GameMap(map_width, map_height) # Create a new game map
	game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)
	
	key = libtcod.Key() # Create variable to store keyboard input
	mouse = libtcod.Mouse() # Create variable to store mouse input

	fov_map = initialize_fov(game_map)
	
	"""
	MAIN GAME LOOP
	"""
	while not libtcod.console_is_window_closed(): # Main Game Loop
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse) # See if the mouse or a key has been pressed, and update variables accordingly
		
		if fov_recompute:
			recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
		
		render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors) # Print everything passed to render_all to the screen.
		
		fov_recompute = False
		
		libtcod.console_flush() # Refresh scene (?)
		
		libtcod.console_put_char(con, player.x, player.y, ' ', libtcod.BKGND_NONE) # Put a blank space where @ character was

		action = handle_keys(key) # Action variable equals the output of handle_keys with the key press stored in the key variable
		
		move = action.get('move') # Move variable equals move Dictionary
		exit = action.get('exit') # Exit variable equals exit Dictionary
		fullscreen = action.get('fullscreen') # Fullscreen variable equals fullscreen Dictionary
		
		if move: # If action contains the move dictionary
			dx, dy = move # Store move dictionary coordinates in dx and dy, respectively
			if not game_map.is_blocked(player.x + dx, player.y + dy): # If the space the player is trying to enter is not flagged as "Blocked"
				player.move(dx, dy) # Call the Entity move function and pass it the dx and dy coordinates
				fov_recompute = True # The player moved, so we'll definitely need to recompute Field of Vision

		if exit: # If action contains the exit dictionary
			return True # Quit the game by returning True to the While game loop
			
		if fullscreen: # If action contains the fullscreen dictionary
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen()) # Set game to fullscreen by making the set_fullscreen variable equal to the opposite of itself.


if __name__ == '__main__':
	main()