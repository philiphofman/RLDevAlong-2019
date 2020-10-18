#  Coded by Philip Hofman, Copyright (c) 2020.

import shelve
import os


def save_game(player, entities, game_map, message_log, game_state):
    """Saves the game in one external file using shelve.

    Args:
        player(Entity): The player's Entity object.
        entities(list): The list of entities on the map.
        game_map(Map): The TCOD map used as the game map.
        message_log(MessageLog): The MessageLog object that stores the in-game messages.
        game_state(int): The current Enum game state, e.g. PLAYERS_TURN.
    """

    with shelve.open('savegame', 'n') as data_file:
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state


def load_game():
    """Loads a previously saved game from one external shelve file.

    Returns:
        player(Entity): The player's Entity object.
        entities(list): The list of entities on the map.
        game_map(Map): The TCOD map used as the game map.
        message_log(MessageLog): The MessageLog object that stores the in-game messages.
        game_state(int): The current Enum game state, e.g. PLAYERS_TURN.
    """

    if not os.path.isfile('savegame.dat'):
        raise FileNotFoundError

    with shelve.open('savegame', 'r') as data_file:
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']

    player = entities[player_index]

    return player, entities, game_map, message_log, game_state
