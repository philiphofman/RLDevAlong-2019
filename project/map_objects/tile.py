"""
A tile on a map. It may or may not be blocked, and may or may not block sight.
"""

class Tile: # Create a new class called Tile
	"""This is the Tile class. It tells you if it's blocked, blocks sight, or explored."""
	
	def __init__(self, blocked, block_sight=None): # Default values for tile class when created
		"""The Tile __init__ sets the blocked, block_sight, and explored variables. block_sight is set to None by default."""
		
		self.blocked = blocked # Tile is automantically flagged as blocked
		
		# By default, if a tile is blocked, it also blocks sight
		if block_sight is None: # If a tile has no value for block_sight variable
			block_sight = blocked # Then block_sight is set to blocked as default
			
		self.block_sight = block_sight # Set own block_sight variable to block_sight
		
		self.explored = False # Set up explored variable and set it to False.