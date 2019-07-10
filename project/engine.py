import tcod as libtcod

from components.fighter import Fighter

from map_objects.game_map import GameMap

from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from input_handlers import handle_keys
from render_functions import clear_all, render_all, RenderOrder
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates


def main():
	"""The only function of the engine. It sets up everything needed for the game and contains the game loop."""
	
	screen_width = 80
	screen_height = 50
	
	# Some UI Variables
	bar_width = 20
	panel_height = 7
	panel_y = screen_height - panel_height
	
	# Size of the map
	map_width = 80
	map_height = 43
	
	# Some variables for the rooms in the map
	room_max_size = 10 
	room_min_size = 6
	max_rooms = 30
	
	fov_algorithm = 0
	fov_light_walls = True
	fov_radius = 10
	fov_recompute = True
	
	max_monsters_per_room = 3
	
	
	# Create new dictionary for colors. Lists use [], dictionaries use {}.
	# Don't forget commas between separate entries in a dictionary,
	# even if they're above and below each other!
	
	colors = {
		'dark_wall': libtcod.Color(0, 0, 100),
		'dark_ground': libtcod.Color(50, 50, 150),
		'light_wall': libtcod.Color(130, 110, 50),
		'light_ground': libtcod.Color(200, 180, 50)
	}
	
	
	fighter_component = Fighter(hp=30, defense=2, power=5)
	player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component)
	entities = [player]

	# Sets custom ASCII character PNG image to use.
	libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

	# Creates the window, window size, window title, and sets fullscreen.
	libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
	
	con = libtcod.console_new(screen_width, screen_height)
	panel = libtcod.console_new(screen_width, panel_height)
	
	game_map = GameMap(map_width, map_height)
	game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)
	
	key = libtcod.Key()
	mouse = libtcod.Mouse()
	
	game_state = GameStates.PLAYERS_TURN

	fov_map = initialize_fov(game_map)

	
	
	################
	#MAIN GAME LOOP#
	################
	
	while not libtcod.console_is_window_closed():
		
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
		
		if fov_recompute:
			recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
		
		render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, screen_width, screen_height, bar_width, panel_height, panel_y, colors)
		
		fov_recompute = False
		
		# Refresh scene (?)
		libtcod.console_flush()
		
		clear_all(con, entities)

		action = handle_keys(key)
		
		move = action.get('move')
		exit = action.get('exit')
		fullscreen = action.get('fullscreen')
		
		player_turn_results = []
		
		if move and game_state == GameStates.PLAYERS_TURN:
			dx, dy = move
			destination_x = player.x + dx
			destination_y = player.y + dy
			
			if not game_map.is_blocked(destination_x, destination_y):
				target = get_blocking_entities_at_location(entities, destination_x, destination_y)
				
				if target:
					attack_results = player.fighter.attack(target)
					player_turn_results.extend(attack_results)
				else:
					player.move(dx, dy)
					fov_recompute = True
				
				game_state = GameStates.ENEMY_TURN

		if exit:
			return True
			
		if fullscreen:
			# Set game to fullscreen by making the set_fullscreen variable equal to the opposite of itself.
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
			
		for player_turn_results in player_turn_results:
			message = player_turn_results.get('message')
			dead_entity = player_turn_results.get('dead')
			
			if message:
				print(message)
			
			if dead_entity:
				if dead_entity == player:
					message, game_state = kill_player(dead_entity)
				else:
					message = kill_monster(dead_entity)
					
				print(message)
			
		if game_state == GameStates.ENEMY_TURN:
			for entity in entities:
				
				# Checking for AI skips the player and any items/other stuff we implement later.
				if entity.ai:
					enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)
					
					for enemy_turn_results in enemy_turn_results:
						message = enemy_turn_results.get('message')
						dead_entity = enemy_turn_results.get('dead')
						
						if message:
							print(message)
						
						if dead_entity:
							if dead_entity == player:
								message, game_state = kill_player(dead_entity)
							else:
								message = kill_monster(dead_entity)
								
							print(message)
							
							if game_state == GameStates.PLAYER_DEAD:
								break
								
					if game_state == GameStates.PLAYER_DEAD:
						break
		
			else:
				game_state = GameStates.PLAYERS_TURN


# If this script is being run directly rather than imported, run main.
# It's a safety check to ensure the game doesn't start when, for example,
# Sphinx imports it to look for docstrings.
if __name__ == '__main__':
	main()