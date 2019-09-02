import shelve

import os


def save_game(player, entities, game_map, message_log, game_state):
	"""Saves the game in one external file using shelve.
	
	Args:
		player: Player's Entity object.
		entities: List of entities on the map.
		game_map: TCOD map used as the game map.
		message_log: MessageLog object that stores a list of messages.
		game_state: The current Enum gamestate, e.g. PLAYERS_TURN.
	"""
	
	with shelve.open('savegame.dat', 'n') as data_file:
		data_file['player_index'] = entities.index(player)
		data_file['entities'] = entities
		data_file['game_map'] = game_map
		data_file['message_log'] = message_log
		data_file['game_state'] = game_state
		
		
def load_game():
	"""Loads a previously saved game from one external shelve file.
	
	Returns:
		player: Player's Entity object.
		entities: List of entities on the map.
		game_map: TCOD map used as the game map.
		message_log: MessageLog object that stores a list of messages.
		game_state: The current Enum gamestate, e.g. PLAYERS_TURN.
	"""
	
	if not os.path.isfile('savegame.dat'):
		raise FileNotFoundError
		
	with shelve.open('savegame.dat', 'r') as data_file:
		player_index = data_file['player_index']
		entities = data_file['entities']
		game_map = data_file['game_map']
		message_log = data_file['message_log']
		game_state = data_file['game_state']
		
	player = entities[player_index]
	
	return player, entities, game_map, message_log, game_state