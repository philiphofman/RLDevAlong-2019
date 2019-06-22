"""
A generic object to represent players, enemies, items, etc.
"""
	
class Entity: # Create a new class called Entity
	def __init__(self, x, y, char, color): # Define init function with self, x and y coordinates, ASCII character to use, and color of the ASCII character
		self.x = x # Self x coordinate is set to input x
		self.y = y # Self y coordinate is set to input y
		self.char = char # Self ASCII character is set to input ASCII character
		self.color = color # Self color is set to input color
		
	def move(self, dx, dy): # Define move function with self, and x and y coordinates
		# Move the entity by a given amount
		self.x += dx # Add input x coordinate to current self x coordinate
		self.y += dy # Add input y coordinate to current self y coordinate