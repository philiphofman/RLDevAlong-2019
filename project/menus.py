import tcod as libtcod


def menu(con, header, options, width, screen_width, screen_height):
	"""A generic menu function to create an options menu.
	
	Args:
		con: The Console object to display the menu on.
		header: String title of the menu.
		options: List of string options.
		width: Integer width of the menu.
		screen_width: Integer width of the screen.
		screen_height: Integer height of the screen.
	"""
	
	if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')
		
	# Calculate total height for the header (after auto-wrap) and one line per option.
	header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
	height = len(options) + header_height
	
	# Create an off-screen console that represents the menu's window
	window = libtcod.console_new(width, height)
	
	# Print the header, with auto-wrap
	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)
	
	# Print out all the options
	y = header_height
	letter_index = ord('a')
	for option_text in options:
		text = '(' + chr(letter_index) + ')' + option_text
		libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
		y += 1
		letter_index += 1
		
	# Blit the contents of "window" to the root console
	x = int(screen_width / 2 - width / 2)
	y = int(screen_height / 2 - height / 2)
	libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
	
	
	
def inventory_menu(con, header, inventory, inventory_width, screen_width, screen_height):
	"""Show a menu with each item of the inventory as an option.
	
	Args:
		con: The Console object the menu is displayed on.
		header: String title of the menu.
		inventory: List of items.
		inventory_width: Integer width of the inventory menu.
		screen_width: Integer width of the screen.
		screen_height: Integer height of the screen.
	"""
	
	if len(inventory.items) == 0:
		options = ['Inventory is empty.']
	else:
		options = [item.name for item in inventory.items]
		
	menu(con, header, options, inventory_width, screen_width, screen_height)
	
	
	
def main_menu(con, background_image, screen_width, screen_height):
	"""Creates a main menu for the game.
	
	Args:
		con: The Console object the menu is displayed on.
		background_image: PNG image used for menu background.
		screen_width: Integer width of screen.
		screen_height: Integer height of screen.
	"""
	
	libtcod.image_blit_2x(background_image, 0, 0, 0)
	
	libtcod.console_set_default_foreground(0, libtcod.light_yellow)
	libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER, 'Roguelike DevAlong 2019')
	libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER, 'By Philip Hofman')
	
	menu(con, '', ['Play a new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height)
	
	
def message_box(con, header, width, screen_width, screen_height):
	"""Displays a message box with a message.
	
	Args:
		con: Console object to display message box on.
		header: String title of the message box.
		width: Integer width of message box.
		screen_width: Integer width of screen.
		screen_height: Integer height of screen.
	"""
	
	menu(con, header, [], width, screen_width, screen_height)