"""
Coordinate system starts at top right corner of map. Going right increases x, going down increases y:

				0 1 2 3 4
				1 . . . .
				2 . . . .
				3 . . . .
				4 . . . .

"""

class Rect:
	"""A helper class for working with rectangles."""
	
	def __init__(self, x, y, w, h):
		"""Inits top left corner and bottom right corner coordinates.
		
		Args:
			x: An integer x coordinate.
			y: An integer y coordinate.
			w: An integer width.
			h: An integer height.
		"""
		
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h
		
	def center(self):
		"""Return the center coordinates of this rectangle."""
		
		center_x = int((self.x1 + self.x2) / 2)
		center_y = int((self.y1 + self.y2) / 2)
		return (center_x, center_y)
		
	def intersect(self, other):
		"""Returns true if this rectangle intersects with another one.
		
		Args:
			other: A Rect object representing the other room.
		"""
		
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
				self.y1 <= other.y2 and self.y2 >= other.y1)