class Item:
	"""An item class to denote what can be picked up."""
	
	def __init__(self, use_function=None, **kwargs):
		"""Inits some values for the Item.
		
		Args:
			use_function: Function for the item to use.
			kwargs: Any arguments needed for the item function.
		"""
		
		self.use_function = use_function
		self.function_kwargs = kwargs