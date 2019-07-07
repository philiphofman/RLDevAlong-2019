"""
In order to make “killable” Entities, rather than attaching hit points to each Entity we create, we’ll create a component,
called Fighter, which will hold information related to combat, like HP, max HP, attack, and defense.
If an Entity can fight, it will have this component attached to it, and if not, it won’t.
This way of doing things is called composition, and it’s an alternative to your typical inheritance-based programming model.
"""

class Fighter: # Define class Fighter
	def __init__(self, hp, defense, power): # Defin init function that initializes HP, Defense, and Power
		self.max_hp = hp # Set Max HP variable to the HP value passed to init. We assume that this is the max HP of the monster, since it's very likely we're creating monsters at full health.
		self.hp = hp # Set HP variable to the HP value passed to init. This is the variable that will track actual HP and any damage done to the monster.
		self.defense = defense # Set Defense variable to the defense value passed to init.
		self.power = power # Set Power variable to the power value passed to init.