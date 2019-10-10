import tcod as libtcod

from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment
from components.equippable import Equippable

from equipment_slots import EquipmentSlots

from entity import Entity

from game_messages import MessageLog

from game_states import GameStates

from map_objects.game_map import GameMap

from render_functions import RenderOrder


def get_constants():
	"""Function that holds all the constant game variables.

	These technically can be changed by the game, but
	they serve as READ ONLY variables.

	Returns:
		A dictionary containing all the defined constants.
	"""

	window_title = 'Roguelike Tutorial Revised'

	screen_width = 80
	screen_height = 50

	# Some UI Variables.
	bar_width = 20
	panel_height = 7
	panel_y = screen_height - panel_height

	message_x = bar_width + 2
	message_width = screen_width - bar_width - 2
	message_height = panel_height - 1

	# Size of the map.
	map_width = 80
	map_height = 43

	# Some variables for the rooms in the map.
	room_max_size = 10
	room_min_size = 6
	max_rooms = 30

	# Variables for the FOV algorithm options.
	fov_algorithm = 0
	fov_light_walls = True
	fov_radius = 10

	# Lists use [], dictionaries use {}.
	# Don't forget commas between separate entries in a dictionary,
	# even if they're above and below each other!

	colors = {
		'dark_wall': libtcod.Color(0, 0, 100),
		'dark_ground': libtcod.Color(50, 50, 150),
		'light_wall': libtcod.Color(130, 110, 50),
		'light_ground': libtcod.Color(200, 180, 50)
	}

	constants = {
		'window_title': window_title,
		'screen_width': screen_width,
		'screen_height': screen_height,
		'bar_width': bar_width,
		'panel_height': panel_height,
		'panel_y': panel_y,
		'message_x': message_x,
		'message_width': message_width,
		'message_height': message_height,
		'map_width': map_width,
		'map_height': map_height,
		'room_max_size': room_max_size,
		'room_min_size': room_min_size,
		'max_rooms': max_rooms,
		'fov_algorithm': fov_algorithm,
		'fov_light_walls': fov_light_walls,
		'fov_radius': fov_radius,
		'colors': colors
	}

	return constants


def get_game_variables(constants):
	"""Initializes a new game's variables.

	Returns:
		player: The player's Entity object.
		entities: List of Entity object on the map.
		game_map: TCOD map object used as the game map.
		message_log: Message log object showing in-game messages.
		game_state: Which part of a game turn it is (PLAYERS_TURN, etc.)
	"""

	fighter_component = Fighter(hp=100, defense=1, power=2)
	inventory_component = Inventory(26)
	level_component = Level()
	equipment_component = Equipment()

	player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
					fighter=fighter_component, inventory=inventory_component, level=level_component,
					equipment=equipment_component)
	entities = [player]

	equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2)
	dagger = Entity(0, 0, '-', libtcod.sky, 'Dagger', equippable=equippable_component)
	player.inventory.add_item(dagger)
	player.equipment.toggle_equip(dagger)

	game_map = GameMap(constants['map_width'], constants['map_height'])
	game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
				  constants['map_width'], constants['map_height'], player, entities)

	message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

	game_state = GameStates.PLAYERS_TURN

	return player, entities, game_map, message_log, game_state
