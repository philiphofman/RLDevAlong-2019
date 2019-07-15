import tcod as libtcod

from enum import Enum

from game_states import GameStates

from menus import inventory_menu


# TODO: Test auto() to see if order will hold true, or if
# manually assigned values are needed to ensure order integrity.
class RenderOrder(Enum):
	"""Defines the render order of Entity objects."""
	
	CORPSE = 1
	ITEM = 2
	ACTOR = 3
	

def get_names_under_mouse(mouse, entities, fov_map):
	"""Displayes names of entities under mouse pointer.
	
	Args:
		entities: List of entities to check names of.
		fov_map: tcod Map object used for calculating FOV.
	"""
	
	(x, y) = (mouse.cx, mouse.cy)
	
	names = [entity.name for entity in entities
					if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
	
	names = ', '.join(names)
	
	return names.capitalize()
	

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
	"""Renders a bar on the screen.
	
	Args:
		panel: The Console object the bar will be rendered in.
		x: Integer width of the bar.
		y: Integer height of the bar.
		total_width: Integer total width of the bar on the screen.
		name: The name of the bar (e.g. Health).
		value: Current integer value of the quantity the bar represents.
		maximum: Max integer value of the quantity the bar represents.
		bar_color: The libtcod.Color of the bar.
		back_color: The libtcod.Color of the background.
	"""
	
	bar_width = int(float(value) / maximum * total_width)
	
	libtcod.console_set_default_background(panel, back_color)
	libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
	
	libtcod.console_set_default_background(panel, bar_color)
	if bar_width > - 0:
		libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
		
	libtcod.console_set_default_foreground(panel, libtcod.white)
	libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER, '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state):
	"""Draw everything that is currently visible to the player.
	
	Draws everything the player currently sees as well as explored
	terrain. Also draws a health bar in the lower left corner.
	
	Args:
		con: A Console object used for the map.
		panel: A Console object used for Stats (i.e. Health).
		entities: The list containing everything to be drawn.
		player: The player Entity object.
		game_map: The Map object used for the actual game.
		fov_map: The Map object used to calculate FOV.
		fov_recompute: A boolean value that indicates if we need to recalculate the FOV.
		message_log: A Message Log object that holds game messages to be displayed.
		screen_width: An integer indicating how wide the screen is.
		screen_height: An integer indicating how tall the screen is.
		bar_width: Integer actual width of bar.
		panel_height: Integer height of panel Console.
		panel_y: Integer position of bar on panel in the y-axis.
		mouse: Mouse Event.
		colors: A dictionary containing all the colors we can use in the game.
		game_state: A Enum representing the current game state.
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
		
		
	libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0) # Draw/combine stuff on screen ???
	
	if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
		if game_state == GameStates.SHOW_INVENTORY:
			inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
		else:
			inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'
			
		inventory_menu(con, inventory_title, player.inventory, 50, screen_width, screen_height)
	
	libtcod.console_set_default_background(panel, libtcod.black)
	libtcod.console_clear(panel)
	
	# Print the game messages, one line at a time
	y = 1
	for message in message_log.messages:
		libtcod.console_set_default_foreground(panel, message.color)
		libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
		y += 1
	
	render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)
	
	libtcod.console_set_default_foreground(panel, libtcod.light_gray)
	libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse(mouse, entities, fov_map))
	
	libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)
	
	
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