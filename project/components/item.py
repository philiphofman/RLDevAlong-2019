class Item:
	"""An item class to denote what can be picked up."""
	
	def __init__(self, use_function=None, targeting=False, targeting_message=None, **kwargs):
		"""Inits some values for the Item.
		
		Args:
			use_function: Function for the item to use.
			targeting: Sets a flag if the item can target stuff.
			targeting_message: A message to let the user know to target something.
			kwargs: Any arguments needed for the item function.
		"""
		
		self.use_function = use_function
		self.targeting = targeting
		self.targeting_message = targeting_message
		self.function_kwargs = kwargs