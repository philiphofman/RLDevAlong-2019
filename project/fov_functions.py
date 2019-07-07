import tcod as libtcod # Import tcod library as libtcod


def initialize_fov(game_map): # Define function initialize_fov and pass it an arbitrary game_map
	fov_map = libtcod.map_new(game_map.width, game_map.height) # Create a new map called fov_map that's the same size as the passed game_map variable
	
	for y in range(game_map.height): # For each Y coordinate that's within our game_map height
		for x in range(game_map.width): # And for each x coordinate within that y coordinate that's within our game_map width
			libtcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight, not game_map.tiles[x][y].blocked)
	
	
	return fov_map # Return this new fov libtcod map
	
def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0): # Define function recompute_fov, passing it an fov_map, perspective x and y coordinates, radius of vision, lighting up the walls, and what algorithm to use
	libtcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm) # Compute the FOV based on the parameters passed to recompute_fov