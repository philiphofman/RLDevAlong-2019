import tcod as libtcod

from enum import Enum


# TODO: Test auto() to see if order will hold true, or if
# manually assigned values are needed to ensure order integrity.
class RenderOrder(Enum):
	"""Defines the render order of Entity objects."""
	
	CORPSE = 1
	ITEM = 2
	ACTOR = 3


def render_all(con, entities, player, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
	"""Draw everything that is currently visible to the player.
	
	Draws everything the player currently sees as well as explored
	terrain. Also draws a health bar in the lower left corner.
	
	Args:
		con: A Console object from tcod.
		entities: The list containing everything to be drawn.
		player: The player Entity object.
		game_map: The Map object used for the actual game.
		fov_map: The Map object used to calculate FOV.
		fov_recompute: A boolean value that indicates if we need to recalculate the FOV.
		screen_width: An integer indicating how wide the screen is.
		screen_height: An integer indicating how tall the screen is.
		colors: A dictionary containing all the colors we can use in the game.
	"""
	

# NOTE: Tiles don't have any color and therefore aren't visible if
# they're not explored. render_all cycles through every tile in the
# current game map, and only gives them a color if they're visible
# and/or explored. But once they're explored, they stay that way,
# giving us a growing map.

	if fov_recompute:
		for y in range(game_map.height):
			for x in range(game_map.width):
				visible = fov_map.fov[y,x]
				wall = game_map.tiles[x][y].block_sight
				
				if visible:
					if wall:
						libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
					else:
						libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
					
					game_map.tiles[x][y].explored = True
					
				elif game_map.tiles[x][y].explored:
					if wall:
						libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
					else:
						libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)
						
	# Draw all entities in the list
	entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
	
	for entity in entities_in_render_order:
		draw_entity(con, entity, fov_map)
		
	libtcod.console_set_default_foreground(con, libtcod.white)
	libtcod.console_print_ex(con, 1, screen_height - 2, libtcod.BKGND_NONE, libtcod.LEFT, 'HP: {0:02}/{1:02}'.format(player.fighter.hp, player.fighter.max_hp))
		
	libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0) # Draw/combine stuff on screen ???
	
	
def clear_all(con, entities):
	"""Erase all items contained within a list in a specific console.
	
	Args:
		con: A Console object from tcod.
		entities: A list containing everything to be cleared.
	"""
	
	for entity in entities:
		clear_entity(con, entity)
		
		
def draw_entity(con, entity, fov_map):
	"""Draw the Entity object ONLY if it's currently visible to the player.
	
	Args:
		con: A Console object from tcod.
		entity: An Entity object that will be drawn.
		fov_map: A Map object that's used for FOV calculations.
	"""
	
	if fov_map.fov[entity.y, entity.x]:
		libtcod.console_set_default_foreground(con, entity.color)
		libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)
	
	
def clear_entity(con, entity):
	"""Erase the Entity object.
	
	Args:
		con: A Console object from tcod.
		entity: An Entity object.
	"""
	
	libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)