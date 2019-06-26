# An 'Enum' is a set of named values that won't change, so it's perfect for things like game states. The numbers don't really mean anything so the auto() helper just numbers them automatically.

from enum import Enum, auto

class GameStates(Enum):
	PLAYERS_TURN = auto()
	ENEMY_TURN = auto()