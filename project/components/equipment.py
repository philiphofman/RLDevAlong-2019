from equipment_slots import EquipmentSlots


class Equipment:
	"""Class which tracks bonuses from equipment and
	what's equipped in each slot. It also handles
	equipping and dequipping stuff and returns a
	dictionary with the results.
	"""

	def __init__(self, main_hand=None, off_hand=None):
		"""Inits default values for equipment."""

		self.main_hand = main_hand
		self.off_hand = off_hand

	@property  # Means it can be accessed like a regular variable.
	def max_hp_bonus(self):
		"""Returns total HP bonus from all equipment."""

		bonus = 0

		if self.main_hand and self.main_hand.equippable:
			bonus += self.main_hand.equippable.max_hp_bonus

		if self.off_hand and self.off_hand.equippable:
			bonus += self.off_hand.equippable.max_hp_bonus

		return bonus

	@property
	def power_bonus(self):
		"""Returns total Power bonus from all equipment."""

		bonus = 0

		if self.main_hand and self.main_hand.equippable:
			bonus += self.main_hand.equippable.power_bonus

		if self.off_hand and self.off_hand.equippable:
			bonus += self.off_hand.equippable.power_bonus

		return bonus

	@property
	def defense_bonus(self):
		"""Returns total Defense bonus from all equipment."""

		bonus = 0

		if self.main_hand and self.main_hand.equippable:
			bonus += self.main_hand.equippable.defense_bonus

		if self.off_hand and self.off_hand.equippable:
			bonus += self.main_hand.equippable.defense_bonus

		return bonus

	def toggle_equip(self, equippable_entity):
		"""Equips and dequips equipment.

		If the item's not equipped, it'll be equipped,
		removing any items already in its slot. If the
		equipment is already equipped, the function assumes
		it's trying to be dequipped and will do so, leaving
		nothing behind in the equipment slot.

		Args:
			equippable_entity: Entity to be equipped.

		Returns:
			A dictionary with the results. Either dequipped - entityName
			or equipped - entityName.
		"""

		results = []

		slot = equippable_entity.equippable.slot

		if slot == EquipmentSlots.MAIN_HAND:
			if self.main_hand == equippable_entity:
				self.main_hand = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.main_hand:
					results.append({'dequipped': self.main_hand})

				self.main_hand = equippable_entity
				results.append({'equipped': equippable_entity})

		elif slot == EquipmentSlots.OFF_HAND:
			if self.off_hand == equippable_entity:
				self.off_hand = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.off_hand:
					results.append({'dequipped': self.off_hand})

				self.off_hand = equippable_entity
				results.append({'equipped': equippable_entity})

		return results