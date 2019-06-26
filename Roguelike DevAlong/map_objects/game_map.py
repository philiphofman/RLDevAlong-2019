from random import randint
import tcod as libtcod

from entity import Entity
from map_objects.tile import Tile # Import Tile class from Tile.py script in map_objects folder
from map_objects.rectangle import Rect # Import Rect class from rectangle.py script in map_objects folder

class GameMap: # Create new class called GameMap that on initialization creates a 2D array of solid tiles of custom dimensions.
	def __init__(self, width, height): # Initialization function, containing width and height.
		self.width = width # Own width variable is equal to input width
		self.height = height # Own height variable is equal to input height
		self.tiles = self.initialize_tiles() # Tiles variable is equal to initialize_tiles function output
	
	def initialize_tiles(self): # Define function initialize_tiles, that creates a 2D array of tiles of custom dimensions.
		tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)] # Create 2D array that creates a Tile object for each y and x coordinate within defined width and height of game map.

		return tiles # Return 2D array called tiles
		
	def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room): # Define function make_map that takes a max amount of rooms, max and min room dimentions, map width and height, and player, and creates a random with those parameters.
		
		rooms = []
		num_rooms = 0
		
		for r in range(max_rooms):
			# Random width and height
			w = randint(room_min_size, room_max_size)
			h = randint(room_min_size, room_max_size)
			# Random position without going out of the boundaries of the map
			x = randint(0, map_width - w - 1)
			y = randint(0, map_height - h - 1)
			
			# "Rect" class makes rectangles easier to work with
			new_room = Rect(x, y, w, h)
			
			# Run through the other rooms and see if they intersect with this one
			for other_room in rooms:
				if new_room.intersect(other_room):
					break
			else:
				# This means there are no intersections, so this room is valid
				
				# "Paint" it to the map's tiles
				self.create_room(new_room)
				
				# Center coordinates of new room, will be useful later
				(new_x, new_y) = new_room.center()
				
				if num_rooms == 0:
					# This is the first room, where the player starts at
					player.x = new_x
					player.y = new_y
				else:
					# All rooms after the first:
					# Connect it to the previous room with a tunnel
					
					# Center coordinates of previous room
					(prev_x, prev_y) = rooms[num_rooms - 1].center()
					
					# Flip a coin (random number that is either a 1 or a 0
					if randint(0, 1) == 1:
						# First move horizontally, then vertically
						self.create_h_tunnel(prev_x, new_x, prev_y)
						self.create_v_tunnel(prev_y, new_y, new_x)
					else:
						# First move vertically, then horizontally
						self.create_v_tunnel(prev_y, new_y, prev_x)
						self.create_h_tunnel(prev_x, new_x, new_y)
				
				self.place_entities(new_room, entities, max_monsters_per_room)
				
				# Finally, append the new room to the list
				rooms.append(new_room)
				num_rooms += 1
		
	def create_room(self, room): # Define function create_room
		# Go through the tiles in the rectangle and make them passable
		for x in range(room.x1 + 1, room.x2): # For each tile in x array corresponding to coordinates x1 + 1 and x2
			for y in range(room.y1 + 1, room.y2): # For each tile in y array corresponding to coordinates y1 + 1 and y2
				self.tiles[x][y].blocked = False # Make the tile unblocked (i.e. able to be moved through)
				self.tiles[x][y].block_sight = False # Make the tile not block line of sight
				
	def create_h_tunnel(self, x1, x2, y): # Define funtion create_h_tunnel, which creates a horizontal tunnel
		for x in range(min(x1, x2), max(x1, x2) + 1): # For each tile in array within specified coordinates, plus one to actually breach the walls of a room
			self.tiles[x][y].blocked = False # Make tile passable
			self.tiles[x][y].block_sight = False # Make tile see-through
			
	def create_v_tunnel(self, y1, y2, x): # Define funtion create_v_tunnel, which creates a vertical tunnel
		for y in range(min(y1, y2), max(y1, y2) + 1): # For each tile in array within specified coordinates, plus one to actually breach the walls of a room
			self.tiles[x][y].blocked = False # Make tile passable
			self.tiles[x][y].block_sight = False # Make tile see-through
			
	def place_entities(self, room, entities, max_monsters_per_room):
		# Get a random number of monsters
		number_of_monsters = randint(0, max_monsters_per_room)
		
		for i in range(number_of_monsters):
			# Choose a random location in the room
			x = randint(room.x1 + 1, room.x2 - 1)
			y = randint(room.y1 + 1, room.y2 - 1)
			
			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				if randint(0, 100) < 80:
					monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True)
				else:
					monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True)
					
				entities.append(monster)
	
	def is_blocked(self, x, y): # Define function is_blocked that is passed x and y coordinates
		if self.tiles[x][y].blocked: # If the tiles at the coordinates stored in your(self) list are blocked
			return True # Return true
		
		return False # Else return false