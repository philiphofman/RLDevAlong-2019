#  Coded by Philip Hofman, Copyright (c) 2020.

import tcod as libtcod

from project.game_messages import Message


class Inventory:
    """An Inventory class for dealing with various inventories.

    Attributes:
        See init function.
    """

    def __init__(self, capacity):
        """Inits some default values for an inventory.

        Inits the max capacity for the inventory and
        sets up a blank list to hold items in.

        Args:
            capacity(int): Amount of stuff the inventory can hold.
        """

        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        """Puts an item in the inventory.

        Args:
            item(Item): The item to add.

        Returns:
            results(list): A list containing a dictionary with the
                results of adding an item.
        """

        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full.', libtcod.yellow)
            })

        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0}!'.format(item.name), libtcod.light_blue)
            })

            self.items.append(item)

        return results

    def use(self, item_entity, **kwargs):
        """Uses an item.

        Args:
            item_entity(Entity): The item to be used.
            **kwargs: Any arguments needed for the item to be used.

        Returns:
            results(list): A list containing a dictionary with
                the results of using the item.
        """

        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            equippable_component = item_entity.equippable

            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append({'message': Message('The {0} cannot be used.'.format(item_entity.name), libtcod.yellow)})
        else:
            if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.function_kwargs, **kwargs}
                item_use_results = item_component.use_function(self.owner, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)

                results.extend(item_use_results)

        return results

    def remove_item(self, item):
        """Removes an item from the inventory.

        Args:
            item(Item): Item to remove.
        """

        self.items.remove(item)

    def drop_item(self, item):
        """Drops an item in the inventory onto the ground.

        Args:
            item(Item): Item to drop.

        Returns:
            results(list): A list containing a dictionary with
                the results of dropping an item on the ground.
        """

        results = []

        if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item:
            self.owner.equipment.toggle_equip(item)

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append(
            {'item_dropped': item, 'message': Message('You dropped the {0}.'.format(item.name), libtcod.yellow)})

        return results
