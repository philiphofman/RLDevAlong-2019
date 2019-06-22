"""
Coordinate system starts at top right corner of map. Going right increases x, going down increases y:

				0 1 2 3 4
				1 . . . .
				2 . . . .
				3 . . . .
				4 . . . .

"""

class Rect: # Define class Rect (short for rectangle)
	def __init__(self, x, y, w, h): # Initialization function being passed x and y coordinates and a (w)idth and a (h)eight. Starts at top right corner of rectangle
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h
		
	def center(self): # Define function center that returns the coordinates of the center of the rectangle
		center_x = int((self.x1 + self.x2) / 2) # Center x coordinate is equal to integer average of coordinates x1 and x2 (left and right edges of rectangle)
		center_y = int((self.y1 + self.y2) / 2) # Center y coordinate is equal to integer average of coordinates y1 and y2 (top and bottom edges of rectangle)
		return (center_x, center_y) # Return the center coordinates in the format (x, y).
		
	def intersect(self, other):
		# Returns true if this rectangle intersects with another one
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
				self.y1 <= other.y2 and self.y2 >= other.y1) # Return true if any part of this rectangle intersects with the other rectangle