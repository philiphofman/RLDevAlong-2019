#  Coded by Philip Hofman, Copyright (c) 2020.

import tcod as libtcod
import math
from project.components.item import Item
from project.render_functions import RenderOrder


class Entity:
    """A generic object to represent players, enemies, items, etc.

    Attributes:
        x(int): x coordinate.
        y(int): y coordinate.
        char(str): The ASCII character representing this Entity object.
        color(str): The color we want this Entity to be.
        name(str): A string with the name we want this Entity to use.
        blocks(bool): A boolean indicating if this Entity blocks movement.
        render_order(int): An Enum value indicating the rendering priority of this Entity.
            Default is lowest priority, CORPSE.
        fighter(Fighter): A Fighter component.
        ai(AI): An AI component.
        item(Item): Item component object flagging if this entity is an Item.
        inventory(Inventory): Inventory component object giving this entity an
            inventory.
        stairs(Stairs): Stairs component object marking this entity as stairs.
        level(int): Current Experience Level of player.
        equipment(Equipment): An Equipment object.
        equippable(Equippable): An Equippable component.
    """

    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None,
                 item=None, inventory=None, stairs=None, level=None, equipment=None, equippable=None):
        """Inits Entity class with a couple of variables.

        Args:
            x(int): x coordinate.
            y(int): y coordinate.
            char(str): The ASCII character representing this Entity object.
            color(str): The color we want this Entity to be.
            name(str): A string with the name we want this Entity to use.
            blocks(bool): A boolean indicating if this Entity blocks movement.
            render_order(int): An Enum value indicating the rendering priority of this Entity.
                Default is lowest priority, CORPSE.
            fighter(Fighter): A Fighter component.
            ai(AI): An AI component.
            item(Item): Item component object flagging if this entity is an Item.
            inventory(Inventory): Inventory component object giving this entity an
                inventory.
            stairs(Stairs): Stairs component object marking this entity as stairs.
            level(int): Current Experience Level of player.
            equipment(Equipment): An Equipment object.
            equippable(Equippable): An Equippable component.
        """

        # Set up all the initial variables and their values.
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        self.equipment = equipment
        self.equippable = equippable

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.level:
            self.level.owner = self

        if self.equipment:
            self.equipment.owner = self

        if self.equippable:
            self.equippable.owner = self

            # If the entity is not an item but is equippable,
            # then we turn it into an item because all
            # equipment is also an item.
            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

    def move(self, dx, dy):
        """Moves this Entity by specified x & y amount.

        Moves Entity by using x & y coordinates that indicate how far to move
        in a given direction, rather than being the actual new coordinates
        the Entity will occupy. Positive numbers add to coordinates, negative
        numbers subtract from coordinates.

        EXAMPLE:
        Entity troll is at (1, 1). Using troll.move(-1, 1) will result in new
        coordinates equaling (0, 2) rather than (-1, 1).

        See input_handlers.py for move Dictionary.

        Args:
            dx(int): Amount to move on x plane.
            dy(int): Amount to move on y plane.
        """

        # Move the entity by a given amount.
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        """Moves this Entity towards a given spot.

        Uses the formula for the distance between two points to
        calculate a straight path to a given target point.

        Distance Formula:
            sqrt((target_x - self.x)^2 + (target_y - self.y)^2)

        Dividing dx and dy by the distance will always yield
        numbers between -1 and 1. Rounding ensures an int between
        -1 and 1. Once the movement is calculated, move_towards
        checks if there's anything blocking the tile it wants to
        move to. If not, it moves, otherwise nothing happens.

        Args:
            target_x(int): x coordinate of the spot we want to get to.
            target_y(int): y coordinate of the spot we want to get to.
            game_map(Map): The Map object that's being used for movement.
            entities(list): A list of Entity objects.
        """

        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def distance(self, x, y):
        """Returns the distance between the Entity and another point.

        Args:
            x(int): x coordinate of arbitrary point.
            y(int): y coordinate of arbitrary point.

        Returns:
            (float): Distance between Entity and the other point.
        """

        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move_astar(self, target, entities, game_map):
        """Moves towards a target using the A* algorithm.

        TODO: Refactor this method to use new TCOD functions.
        TODO: Rewrite docstring to better document A* algorithm.
        TODO: Study and pick apart A* to understand how it works.

        Args:
            target(Entity): The Entity object to plot a path to.
            entities(list): A list of Entities.
            game_map(Map): The Map object used for displaying the game.
        """

        # Create a FOV map that has the dimensions of the map
        fov = libtcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                # libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight, not game_map.tiles[x1][y1].blocked)
                fov.transparent[y1, x1] = not game_map.tiles[x1][y1].block_sight
                fov.walkable[y1, x1] = not game_map.tiles[x1][y1].blocked

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                # libtcod.map_set_properties(fov, entity.x, entity.y, True, False)
                fov.transparent[entity.y, entity.x] = True
                fov.walkable[entity.y, entity.x] = False

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y, game_map, entities)

        # Delete the path to free memory
        libtcod.path_delete(my_path)

    def distance_to(self, other):
        """Returns the distance to a particular Entity.

        Args:
            other(Entity): The Entity object we want to measure distance to.

        Returns:
            (float): Distance between this Entity and another Entity.
        """

        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    """Returns Entity, if any, that is blocking movement to specified coordinates.

    Returns any Entity whose 'blocks' boolean equals TRUE at specified coordinates.
    Iterates through the entire passed list checking for blocking entities.

    Args:
        entities(list): A list containing the Entities to check.
        destination_x(int): x coordinate.
        destination_y(int): y coordinate.

    Returns:
        entity(Entity): An Entity object if one exists at the coordinates
            that blocks movement. If no blocking Entity exists, the
            function returns None.
    """

    # Check if there are any blocking entities in the specified coordinates.
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
