#  Coded by Philip Hofman, Copyright (c) 2020.

from random import randint
import tcod as libtcod

from project.entity import Entity
from project.game_messages import Message
from project.render_functions import RenderOrder
from project.item_functions import heal, cast_lightning, cast_fireball, cast_confuse
from project.random_utils import random_choice_from_dict, from_dungeon_level

from project.components.ai import BasicMonster
from project.components.fighter import Fighter
from project.components.item import Item
from project.components.stairs import Stairs
from project.components.equipment import EquipmentSlots
from project.components.equippable import Equippable

from project.map_objects.tile import Tile
from project.map_objects.rectangle import Rect


class GameMap:
    """GameMap handles the creation of a random map by creating rooms, tunnels, and placing entities."""

    def __init__(self, width, height, dungeon_level=1):
        """Inits values for the game map.

        Args:
            width(int): An integer defining the width of the map.
            height(int): An integer defining the height of the map.
            dungeon_level(int): The current dungeon level.
        """

        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        """Creates a 2D array of tiles with own width and height.

        By default every tile blocks movement, since a different function
        (make_map) is responsible for "digging out" the rooms and tunnels.

        Returns:
            tiles(list): A 2D array of tiles with the dimensions of the GameMap object.
        """

        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        """Creates a a random map and populates it with monsters and the player.

        Starts by creating a random room somewhere in the map,
        plopping the player in the center of it, then creating
        new rooms, connecting them with tunnels, and spawning
        monsters in them.

        Args:
            max_rooms(int): Max amount of rooms in this map.
            room_min_size(int): How small a room can be.
            room_max_size(int): How big a room can be.
            map_width(int): Width of the map.
            map_height(int): Height of a map.
            player(Entity): The player's Entity object.
            entities(list): A list containing all the objects on the map.
        """

        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

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

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

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

                self.place_entities(new_room, entities)

                # Finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        # Once the last room has been created, put stairs in it leading down.
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    def create_room(self, room):
        """Goes through the tiles in the rectangle and makes them passable.

        Args:
            room(Rect): A Rect object representing the room.
        """

        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        """Creates a horizontal tunnel.

        Args:
            x1(int): The starting point.
            x2(int): The end point.
            y(int): Which row to use.
        """

        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        """Creates a vertical tunnel.

        Args:
            y1(int): The starting point.
            y2(int): The end point.
            x(int): Which column to use.
        """

        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities):
        """Gets a random number of monsters and items, and spawns them in the room.

        First decides how many monsters and items can be in a room at once based
        on dungeon level. Then chooses a random number of items and monsters to
        spawn in this particular room. Iterates through the number of monsters
        and randomly spawns monsters based on their chances to appear. Does the
        same thing for items. Appends each spawned item to the entities list.

        Args:
            room(Rect): A Rect object that represents the room.
            entities(list): A list of Entity objects.
        """

        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)

        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        monster_chances = {
            'orc': 80,
            'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
        }

        item_chances = {
            'healing_potion': 70,
            'sword': from_dungeon_level([[5, 4]], self.dungeon_level),
            'shield': from_dungeon_level([[15, 8]], self.dungeon_level),
            'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.dungeon_level),
            'confusion_scroll': from_dungeon_level([[10, 2]], self.dungeon_level)
        }

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # If nothing's there, create a monster.
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == 'orc':
                    fighter_component = Fighter(hp=20, defense=0, power=4, xp=35)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                elif monster_choice == 'troll':
                    fighter_component = Fighter(hp=30, defense=2, power=8, xp=100)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                entities.append(monster)

        for i in range(number_of_items):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=40)
                    item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'sword':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
                    item = Entity(x, y, '/', libtcod.sky, 'Sword', equippable=equippable_component)

                elif item_choice == 'shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
                    item = Entity(x, y, '[', libtcod.darker_orange, 'Shield', equippable=equippable_component)

                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan),
                                          damage=25, radius=3)
                    item = Entity(x, y, '#', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan))
                    item = Entity(x, y, '#', libtcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'lightning_scroll':
                    item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
                    item = Entity(x, y, '#', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)

                entities.append(item)

    def is_blocked(self, x, y):
        """Returns boolean about whether a tile is blocked.

        Args:
            x(int): The tile's x coordinate.
            y(int): The tile's y coordinate.

        Returns:
            (bool): A boolean value describing whether the tile
                specified in this object's 2D tile array
                blocks movement.
        """

        if self.tiles[x][y].blocked:
            return True

        return False

    def next_floor(self, player, message_log, constants):
        """Moves the player down one floor of the dungeon.

        Increases dungeon level by one, clears the entities
        list except for the player, and creates a new map.
        Also heals the player for half their max HP.

        Args:
            player(Entity): Entity object representing the player.
            message_log(MessageLog): MessageLog object containing game messages.
            constants(dict): Dictionary containing game's constant variables.

        Returns:
            entities(list): New entities list containing only the player.
        """

        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

        player.fighter.heal(player.fighter.max_hp // 2)  # '//' is integer division (e.g. 5 // 2 = 2, 5 / 2 = 2.5)

        message_log.add_message(Message('You take a moment to rest and recover your strength.', libtcod.light_violet))

        return entities
