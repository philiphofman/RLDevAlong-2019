import tcod as libtcod

from loader_functions.initialize_new_game import get_constants, get_game_variables

from game_messages import Message
from death_functions import kill_monster, kill_player
from entity import get_blocking_entities_at_location
from input_handlers import handle_keys, handle_mouse
from render_functions import clear_all, render_all
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates


def main():
	"""The only function of the engine. It sets up everything needed for the game and contains the game loop."""
	
	constants = get_constants()
	
	player, entities, game_map, message_log, game_state = get_game_variables(constants)
	
	# Sets custom ASCII character PNG image to use.
	libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

	# Creates the window, window size, window title, and sets fullscreen.
	libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)
	
	con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
	panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])
	
	key = libtcod.Key()
	mouse = libtcod.Mouse()
	
	previous_game_state = game_state

	fov_recompute = True
	fov_map = initialize_fov(game_map)
	
	targeting_item = None

	
	
	################
	#MAIN GAME LOOP#
	################
	
	while not libtcod.console_is_window_closed():
		
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
		
		if fov_recompute:
			recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'], constants['fov_algorithm'])
		
		render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, constants['screen_width'], constants['screen_height'], constants['bar_width'], constants['panel_height'], constants['panel_y'], mouse, constants['colors'], game_state)
		
		fov_recompute = False
		
		# Refresh scene (?)
		libtcod.console_flush()
		
		clear_all(con, entities)
		
		# Get any keys that have been pressed and execute their associated action(s).
		action = handle_keys(key, game_state)
		mouse_action = handle_mouse(mouse)
		
		move = action.get('move')
		pickup = action.get('pickup')
		show_inventory = action.get('show_inventory')
		drop_inventory = action.get('drop_inventory')
		inventory_index = action.get('inventory_index')
		exit = action.get('exit')
		fullscreen = action.get('fullscreen')
		
		left_click = mouse_action.get('left_click')
		right_click = mouse_action.get('right_click')
		
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
				
		elif pickup and game_state == GameStates.PLAYERS_TURN:
			for entity in entities:
				if entity.item and entity.x == player.x and entity.y == player.y:
					pickup_results = player.inventory.add_item(entity)
					player_turn_results.extend(pickup_results)
					
					break
			else:
				message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))
				
		if show_inventory:
			previous_game_state = game_state
			game_state = GameStates.SHOW_INVENTORY
			
		if drop_inventory:
			previous_game_state = game_state
			game_state = GameStates.DROP_INVENTORY
			
		if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(player.inventory.items):
			item = player.inventory.items[inventory_index]
			
			if game_state == GameStates.SHOW_INVENTORY:
				player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
			elif game_state == GameStates.DROP_INVENTORY:
				player_turn_results.extend(player.inventory.drop_item(item))
				
		if game_state == GameStates.TARGETING:
			if left_click:
				target_x, target_y = left_click
				
				item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y)
				player_turn_results.extend(item_use_results)
			elif right_click:
				player_turn_results.append({'targeting_cancelled': True})

		if exit:
			if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
				game_state = previous_game_state
			elif game_state == GameStates.TARGETING:
				player_turn_results.append({'targeting_cancelled': True})
			else:
				return True
			
		if fullscreen:
			# Toggle fullscreen by making the set_fullscreen variable equal to the opposite of itself.
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
			
			
		# Check what happened on the player's turn and react accordingly.	
		for player_turn_results in player_turn_results:
			message = player_turn_results.get('message')
			dead_entity = player_turn_results.get('dead')
			item_added = player_turn_results.get('item_added')
			item_consumed = player_turn_results.get('consumed')
			item_dropped = player_turn_results.get('item_dropped')
			targeting = player_turn_results.get('targeting')
			targeting_cancelled = player_turn_results.get('targeting_cancelled')
			
			if message:
				message_log.add_message(message)
			
			if dead_entity:
				if dead_entity == player:
					message, game_state = kill_player(dead_entity)
				else:
					message = kill_monster(dead_entity)
					
				message_log.add_message(message)
				
			if item_added:
				entities.remove(item_added)
				
				game_state: GameStates.ENEMY_TURN
				
			if item_consumed:
				game_state: GameStates.ENEMY_TURN
				
			if targeting:
				previous_game_state = GameStates.PLAYERS_TURN
				game_state = GameStates.TARGETING
				
				targeting_item = targeting
				
				message_log.add_message(targeting_item.item.targeting_message)
				
			if targeting_cancelled:
				game_state = previous_game_state
				
				message_log.add_message(Message('Targeting cancelled.'))
				
			if item_dropped:
				entities.append(item_dropped)
				
				game_state: GameStates.ENEMY_TURN
				
			
		if game_state == GameStates.ENEMY_TURN:
			for entity in entities:
				
				# Checking for AI skips the player and any items/other stuff we implement later.
				if entity.ai:
					enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)
					
					for enemy_turn_results in enemy_turn_results:
						message = enemy_turn_results.get('message')
						dead_entity = enemy_turn_results.get('dead')
						
						if message:
							message_log.add_message(message)
						
						if dead_entity:
							if dead_entity == player:
								message, game_state = kill_player(dead_entity)
							else:
								message = kill_monster(dead_entity)
								
							message_log.add_message(message)
							
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
