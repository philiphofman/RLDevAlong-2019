import tcod as libtcod

from game_messages import Message


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
			capacity: Integer amount of stuff the inventory can hold.
		"""
		
		self.capacity = capacity
		self.items = []
		
		
	def add_item(self, item):
		"""A function that puts an item in the inventory.
		
		Args:
			item: The Item object to pick up.
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
		"""Use an item.
		
		Args:
			item_entity: Entity object using item. ???
			**kwargs: Arguments for the function used.
		"""
		
		results = []
		
		item_component = item_entity.item
		
		if item_component.use_function is None:
			results.append({'message': Message('The {0} cannot be used.'.format(item_entity.name), libtcod.yellow)})
		else:
			kwargs = {**item_component.function_kwargs, **kwargs}
			item_use_results = item_component.use_function(self.owner, **kwargs)
			
			for item_use_result in item_use_results:
				if item_use_result.get('consumed'):
					self.remove_item(item_entity)
					
					
			results.extend(item_use_results)
			
		return results
		
		
	def remove_item(self, item):
		"""Remove an item from the inventory.
		
		Args:
			item: Item to remove.
		"""
		
		self.items.remove(item)
		

	def drop_item(self, item):
		"""Drops an item in the inventory onto the ground.
		
		Args:
			item: Item to drop.
		"""
		
		results = []
		
		item.x = self.owner.x
		item.y = self.owner.y
		
		self.remove_item(item)
		results.append({'item_dropped': item, 'message': Message('You dropped the {0}.'.format(item.name), libtcod.yellow)})
		
		return results