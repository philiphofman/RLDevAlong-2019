import tcod as libtcod

from game_messages import Message

"""
In order to make “killable” Entities, rather than attaching hit points to each Entity we create, we’ll create a component,
called Fighter, which will hold information related to combat, like HP, max HP, attack, and defense.
If an Entity can fight, it will have this component attached to it, and if not, it won’t.
This way of doing things is called composition, and it’s an alternative to your typical inheritance-based programming model.
"""


class Fighter:
	"""A component class that holds information about combat."""

	def __init__(self, hp, defense, power, xp=0):
		"""Inits some inital combat values.
		
		Args:
			hp: An integer defining hit points.
			defense: An integer defense value.
			power: An integer power value.
			xp: Integer value of xp gained when killing an enemy.
		"""

		self.base_max_hp = hp
		self.hp = hp
		self.base_defense = defense
		self.base_power = power
		self.xp = xp

	@property
	def max_hp(self):
		"""Returns total of base max HP and any bonuses from equipment."""

		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.max_hp_bonus
		else:
			bonus = 0

		return self.base_max_hp + bonus

	@property
	def power(self):
		"""Returns total of base power and any bonuses from equipment."""

		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.power_bonus
		else:
			bonus = 0

		return self.base_power + bonus

	@property
	def defense(self):
		"""Returns total of base defense and any bonuses from equipment."""

		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.defense_bonus
		else:
			bonus = 0

		return self.base_defense + bonus

	def take_damage(self, amount):
		"""Subtracts damage taken from HP.
		
		Args:
			amount: An integer amount of HP to lose.
			
		Returns:
			A list containing a dictionary that has
			several different outcomes possible.
		"""

		results = []

		self.hp -= amount

		if self.hp <= 0:
			results.append({'dead': self.owner, 'xp': self.xp})

		return results

	def heal(self, amount):
		"""Increase HP by specified integer amount.
		
		Args:
			amount: Int amount to heal.
		"""

		self.hp += amount

		if self.hp > self.max_hp:
			self.hp = self.max_hp

	def attack(self, target):
		"""Calculates the damage to inflict upon an enemy.
		
		First calculates damage by subtracting target's defense
		from your power. Then adds a message and damage to a list
		called results, and returns the list.
		
		Args:
			target: The Entity object being attacked.
		"""

		results = []

		damage = self.power - target.fighter.defense

		if damage > 0:
			results.append({'message': Message(
				'{0} attacks {1} for {2} hit points.'.format(self.owner.name.capitalize(), target.name, str(damage)),
				libtcod.white)})
			results.extend(target.fighter.take_damage(damage))
		else:
			results.append({'message': Message(
				'{0} attacks {1} but does no damage.'.format(self.owner.name.capitalize(), target.name),
				libtcod.white)})

		return results
