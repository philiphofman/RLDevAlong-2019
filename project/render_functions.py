import tcod as libtcod # Import tcod library


def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors): # Define function render_all with specific console, list, game map, screen width, height, and colors dictionary.
	"""Draw everything that is currently visible to the player."""
	

# NOTE: Tiles don't have any color and therefore aren't visible if
# they're not explored. render_all cycles through every tile in the
# current game map, and only gives them a color if they're visible
# and/or explored. But once they're explored, they stay that way,
# giving us a growing map.

	if fov_recompute: # If the FOV needs to be recalculated, i.e. because the player moved (If fov_recompute is equal to TRUE)...
		for y in range(game_map.height): # For each Y coordinate in the game map's height...
			for x in range(game_map.width): # For each X coordinate in that row in the game map's width...
				visible = libtcod.map_is_in_fov(fov_map, x, y) # Flag each tile as visible or not visible with Boolean value (TRUE or FALSE), by running function map_is_in_fov, passing the fov_map and coordinates of the tile.
				wall = game_map.tiles[x][y].block_sight # If tile is a wall, block_sight will return TRUE for this wall variable.
				
				if visible: # If the tile is currently visible as determined by the map_is_in_fov function...
					if wall: # If it's a wall as determined by the wall boolean variable...
						libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET) # Set the color of the tile to 'light_wall'.
					else: # Else, since it's not a wall and therefore ground...
						libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET) # Set the color of the tile to 'light_ground'.
					
					game_map.tiles[x][y].explored = True # Set the tile's explored value to TRUE. (Doesn't matter if it was explored before, it was explored now and therefore is still TRUE)
					
				elif game_map.tiles[x][y].explored: # Else if the tile has already been explored (explored = TRUE), but ISN'T visible...
					if wall: # If it's a wall...
						libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET) # Set the color of the tile to 'dark_wall'.
					else: # Else, since it's not a wall and therefore ground...
						libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET) # Set the color of the tile to 'dark_ground'.
						
	# Draw all entities in the list
	for entity in entities: # For every item that's in the list
		draw_entity(con, entity, fov_map) # Call draw_entity function with specific console and current item in the list
		
	libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0) # Draw/combine stuff on screen ???
	
	
def clear_all(con, entities): # Define function clear_all with specific console and list
	"""Erase all items contained within a list in a specific console"""
	
	for entity in entities: # For every item that's in the list
		clear_entity(con, entity) # Call clear_entity function with specific console and current item in the list
		
		
def draw_entity(con, entity, fov_map): # Define function draw_entity with specific console and item in list
	"""Draw the character that represents this object ONLY if it's currently visible to the player."""
	
	if libtcod.map_is_in_fov(fov_map, entity.x, entity.y): # If the current entity is visible to the player...
		libtcod.console_set_default_foreground(con, entity.color) # Send it to specific console with specific color
		libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE) # Draw entity in specific console at x and y coordinates, with its defined ASCII character and no background
	
	
def clear_entity(con, entity): # Define function clear_entity with specific console and item in list
	"""Erase the character that represents this object"""
	
	libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE) # Draw empty space in specific console at x and y coordinates, with an ASCII space and no background