import tcod as libtcod # Import tcod library


def render_all(con, entities, game_map, screen_width, screen_height, colors): # Define function render_all with specific console, list, game map, screen width, height, and colors dictionary
	# Draw all tiles in the game map
	for y in range(game_map.height):
		for x in range(game_map.width):
			wall = game_map.tiles[x][y].block_sight
			
			if wall:
				libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
			else:
				libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)
	# Draw all entities in the list
	for entity in entities: # For every item that's in the list
		draw_entity(con, entity) # Call draw_entity function with specific console and current item in the list
		
	libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0) # Draw/combine stuff on screen ???
	
	
def clear_all(con, entities): # Define function clear_all with specific console and list
	for entity in entities: # For every item that's in the list
		clear_entity(con, entity) # Call clear_entity function with specific console and current item in the list
		
		
def draw_entity(con, entity): # Define function draw_entity with specific console and item in list
	libtcod.console_set_default_foreground(con, entity.color) # Send it to specific console with specific color
	libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE) # Draw entity in specific console at x and y coordinates, with its defined ASCII character and no background
	
	
def clear_entity(con, entity): # Define function clear_entity with specific console and item in list
	# Erase the character that represents this object
	libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE) # Draw empty space in specific console at x and y coordinates, with an ASCII space and no background