"""
A generic object to represent players, enemies, items, etc.
"""
	
class Entity: # Create a new class called Entity
	def __init__(self, x, y, char, color, name, blocks=False): # Define init function with self, x and y coordinates, ASCII character to use, and color of the ASCII character.
		"""Sets up and populates all variables with respective passed values when new Entity is created."""
		
		self.x = x # Self x coordinate is set to passed x
		self.y = y # Self y coordinate is set to passed y
		self.char = char # Self ASCII character is set to passed ASCII character
		self.color = color # Self color is set to passed color
		self.name = name # Self name is set to passed name
		self.blocks = blocks # Self blocks flag is set to passed blocks (False by default if no value passed)
		
	def move(self, dx, dy): # Define move function with self, and x and y coordinates.
		"""Updates coordinates for Entity as it moves."""
		
		# Move the entity by a given amount
		self.x += dx # Add passed x coordinate to current self x coordinate
		self.y += dy # Add passed y coordinate to current self y coordinate
		
		
		

def get_blocking_entities_at_location(entities, destination_x, destination_y): # Define get_blocking_entities_at_location function that is passed a list, and destination x & y coordinates.
	"""Returns any Entity that has the Blocks flag set to True in the passed coordinates, otherwise returns None."""
	
	for entity in entities: # For every entity in the entities list...
		if entity.blocks and entity.x == destination_x and entity.y == destination_y: # If the entity Blocks flag is True and it's in the destination coordinates passed to the function...
			return entity # Return the entity that is occupying those coordinates.
			
	return None # Else, return None. You're free to move!