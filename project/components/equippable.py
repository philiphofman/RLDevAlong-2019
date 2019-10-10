class Equippable:
	"""Component class defining stuff for equippable items."""

	def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
		"""Inits some default values for equippable items.

		Args:
			slot: What int equipment slot this item goes into.
			power_bonus: Int power boost to player.
			defense_bonus: Int defense boost to player.
			max_hp_bonus: Int hp bonus to player.
		"""

		self.slot = slot
		self.power_bonus = power_bonus
		self.defense_bonus = defense_bonus
		self.max_hp_bonus = max_hp_bonus
