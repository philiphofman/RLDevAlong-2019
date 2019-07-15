from random import randint
import tcod as libtcod

from entity import Entity
from render_functions import RenderOrder
from item_functions import heal

from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item

from map_objects.tile import Tile
from map_objects.rectangle import Rect

class GameMap:
	"""GameMap handles creation of a random map by creating rooms, tunnels, and placing entities."""
	
	def __init__(self, width, height):
		"""__init__ creates a map of the passed width and height.
		
		Args:
			width: An integer defining the width of the map.
			height: An integer defining the height of the map.
		"""
		
		self.width = width
		self.height = height
		self.tiles = self.initialize_tiles()
	
	def initialize_tiles(self):
		"""Creates a 2D array of tiles with own width and height.
		
		Returns:
			A 2D array of tiles with the dimensions of the GameMap object.
		"""
		
		tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

		return tiles
		
	def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room):
		"""Creates a a random map and populates it with monsters and the player.
		
		Starts by creating a random room somewhere in the map,
		plopping the player in the center of it, then creating
		new rooms, connecting them with tunnels, and spawning
		monsters in them.
		
		Args:
			max_rooms: An integer defining the max amount of rooms in this map.
			room_min_size: An integer defining how small a room can be.
			room_max_size: An integer defining how big a room can be.
			map_width: An integer defining the width of the map.
			map_height: An integer defining the height of a map.
			player: An Entity object that represents the player.
			entities: A list containing Entity objects.
			max_monsters_per_room: An integer defining the max amount of
				monsters to be spawned in one room.
			max_items_per_room: An integer number of the max number of items
				per room.
		"""
		
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
					
					if randint(0, 1) == 1:
						# First move horizontally, then vertically
						self.create_h_tunnel(prev_x, new_x, prev_y)
						self.create_v_tunnel(prev_y, new_y, new_x)
					else:
						# First move vertically, then horizontally
						self.create_v_tunnel(prev_y, new_y, prev_x)
						self.create_h_tunnel(prev_x, new_x, new_y)
				
				self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)
				
				# Finally, append the new room to the list
				rooms.append(new_room)
				num_rooms += 1
		
	def create_room(self, room):
		"""Goes through the tiles in the rectangle, makes them passable, and doesn't block sight.
		
		Args:
			room: A Rect object representing the room.
		"""
		
		for x in range(room.x1 + 1, room.x2):
			for y in range(room.y1 + 1, room.y2):
				self.tiles[x][y].blocked = False
				self.tiles[x][y].block_sight = False
				
	def create_h_tunnel(self, x1, x2, y):
		"""Creates a horizontal tunnel.
		
		Args:
			x1: An integer representing the starting point.
			x2: An integer representing the ending point.
			y: An integer telling us which row to use.
		"""
		
		for x in range(min(x1, x2), max(x1, x2) + 1):
			self.tiles[x][y].blocked = False
			self.tiles[x][y].block_sight = False
			
	def create_v_tunnel(self, y1, y2, x):
		"""Creates a vertical tunnel.
		
		Args:
			y1: An integer representing the starting point.
			y2: An integer representing the ending point.
			x: An integer telling us which column to use.
		"""
		
		for y in range(min(y1, y2), max(y1, y2) + 1):
			self.tiles[x][y].blocked = False
			self.tiles[x][y].block_sight = False
			
	def place_entities(self, room, entities, max_monsters_per_room, max_items_per_room):
		"""Get a random number of monsters.
		
		Args:
			room: A Rect object that represents the room.
			entities: A list of Entity objects.
			max_monsters_per_room: An integer specifying the max number of
				monsters to be spawned in this room.
			max_items_per_room: An integer number of the max number of items
				per room.
		"""
		
		number_of_monsters = randint(0, max_monsters_per_room)
		number_of_items = randint(0, max_items_per_room)
		
		for i in range(number_of_monsters):
			# Choose a random location in the room
			x = randint(room.x1 + 1, room.x2 - 1)
			y = randint(room.y1 + 1, room.y2 - 1)
			
			# If nothing's there, create a monster.
			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				if randint(0, 100) < 80:
					fighter_component = Fighter(hp=10, defense=0, power=3)
					ai_component = BasicMonster()
					
					monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
				else:
					fighter_component = Fighter(hp=16, defense=1, power=4)
					ai_component = BasicMonster()
					
					monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
					
				entities.append(monster)
				
		
		for i in range(number_of_items):
			# Choose a random location in the room
			x = randint(room.x1 + 1, room.x2 - 1)
			y = randint(room.y1 + 1, room.y2 - 1)
			
			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				item_component = Item(use_function=heal, amount=4)
				item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM, item=item_component)
				
				entities.append(item)
	
	def is_blocked(self, x, y):
		"""Returns boolean about whether a tile is blocked.
		
		Args:
			x: An integer representing the x coordinate.
			y: An integer representing the y coordinate.
		
		Returns:
			A boolean value describing whether the tile
			specified in this object's 2D tile array
			blocks movement.
		"""
		
		if self.tiles[x][y].blocked:
			return True
		
		return False