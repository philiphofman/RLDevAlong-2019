"""
In order to make “killable” Entities, rather than attaching hit points to each Entity we create, we’ll create a component,
called Fighter, which will hold information related to combat, like HP, max HP, attack, and defense.
If an Entity can fight, it will have this component attached to it, and if not, it won’t.
This way of doing things is called composition, and it’s an alternative to your typical inheritance-based programming model.
"""

class Fighter:
	"""A component class that holds information about combat."""
	
	def __init__(self, hp, defense, power):
		"""Inits some inital combat values.
		
		Args:
			hp: An integer defining hit points.
			defense: An integer defense value.
			power: An integer power value.
		"""
		
		self.max_hp = hp
		self.hp = hp
		self.defense = defense
		self.power = power