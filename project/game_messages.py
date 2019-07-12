import tcod as libtcod

import textwrap


class Message:
	"""Class for text messages.
	
	
	Attributes:
		text: String of message text.
		color: Color of message.
	"""
	
	def __init__(self, text, color=libtcod.white):
		"""Inits some message values.
		
		Args:
			text: String containing text of message.
			color: tcod Color of message.
		"""
		
		self.text = text
		self.color = color
		
		
		
class MessageLog:
	"""Log for messages."""
	
	def __init__(self, x, width, height):
		"""Inits some values for message log.
		
		Args:
			x: Integer x coordinate.
			width: Integer width.
			height: Integer height.
		"""
		
		self.messages = []
		self.x = x
		self.width = width
		self.height = height
		
	def add_message(self, message):
		"""Adds a message to the log.
		
		Args:
			message: A Message object message.
		"""
		
		# Split the message if necessary, among multiple lines.
		new_msg_lines = textwrap.wrap(message.text, self.width)
		
		for line in new_msg_lines:
			# If the buffer is full, remove the first line to make room for the new one.
			if len(self.messages) == self.height:
				del self.messages[0]
				
			# Add the new line as a message object, with the text and the color
			self.messages.append(Message(line, message.color))