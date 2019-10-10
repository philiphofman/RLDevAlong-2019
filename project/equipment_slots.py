from enum import Enum, auto


class EquipmentSlots(Enum):
	"""Defines number and type of player equipment slots."""

	MAIN_HAND = auto()
	OFF_HAND = auto()  # TODO: Add more equipment slots to player. Armor, rings, etc.
