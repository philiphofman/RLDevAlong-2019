import tcod as libtcod


def initialize_fov(game_map): # Define function initialize_fov and pass it an arbitrary game_map
	"""Creates a new map that stores sight-line info for FOV calculations.
	
	Creates a seperate map identical to the actual game map. Iterates
	through each tile and sets whether it is transparent and blocks
	movement.
	
	Args:
		game_map: A tcod Map that is being used as the visible game map.
		
	Returns:
		A new Map that contains FOV information about each tile,
		specifically whether it's transparent (i.e. a floor) and
		whether it blocks other stuff (i.e. a wall).
	"""

	fov_map = libtcod.map.Map(game_map.width, game_map.height)
	
	for y in range(game_map.height):
		for x in range(game_map.width):
			fov_map.transparent[y,x] = not game_map.tiles[x][y].block_sight
			fov_map.walkable[y,x] = not game_map.tiles[x][y].blocked
	
	
	return fov_map
	
def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
	"""Recalculates the FOV.
	
	Args:
		fov_map: A tcod Map being used for FOV calculations.
		x: An integer x coordinate.
		y: An integer y coordinate.
		radius: An integer representing how far the player can see in tiles.
		light_walls: A boolean that decides if visible obstacles will be returned.
		algorithm: An integer that decides which FOV algorithm to run.
	"""
	
	fov_map.compute_fov(x, y, radius, light_walls, algorithm)