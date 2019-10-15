import tcod as libtcod

from game_states import GameStates


def handle_keys(key, game_state):
    """Checks current game state and chooses key handler function.

    Args:
        key(int): A keycode (vk)
        game_state(Enum): An Enum denoting what game state it is.

    Returns:
        (dict): A dictionary key name.
    """

    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)

    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)

    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)

    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)

    elif game_state == GameStates.LEVEL_UP:
        return handle_level_up_menu(key)

    elif game_state == GameStates.CHARACTER_SCREEN:
        return handle_character_screen(key)

    return {}


def handle_targeting_keys(key):
    """Handles key presses during targeting.

    Args:
        key(int): A keycode (vk)

    Returns:
        (dict): A dictionary key name.
    """

    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_inventory_keys(key):
    """Handles key presses in the inventory.

    Args:
        key(int): A keycode (vk)

    Returns:
        (dict): A dictionary key name.
    """

    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: Toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}


def handle_player_turn_keys(key):
    """Checks if a key has been pressed on the player's turn.

    Args:
        key(int): A keycode (vk)

    Returns:
        (dict): A dictionary key name. Currently either coordinates in the
        (x, y) format, or a boolean value.
    """

    # TODO: Replace with tcod.event. Check if Event code is complete first.
    key_char = chr(key.c)

    if key.vk == libtcod.KEY_UP or key_char == 'h':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'k':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
        return {'move': (1, 0)}
    elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == 'n':
        return {'move': (1, 1)}
    elif key_char == 'z':
        return {'wait': True}

    elif key_char == 'g':
        return {'pickup': True}

    elif key_char == 'i':
        return {'show_inventory': True}

    elif key_char == 'd':
        return {'drop_inventory': True}
    # TODO: Fix code to let '>' work instead of Enter.
    elif key.vk == libtcod.KEY_ENTER:
        return {'take_stairs': True}

    elif key_char == 'c':
        return {'show_character_screen': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}


def handle_player_dead_keys(key):
    """Handles key presses during player's death.

    Args:
        key(int): A keycode (vk)

    Returns:
        (dict): A dictionary key name.
    """

    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: Toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}


def handle_mouse(mouse):
    """Returns which coordinates the left or right mouse button clicked on.

    Args:
        mouse(Mouse): tcod Mouse object.

    Returns:
        (dict): A dictionary key name.
    """

    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}


def handle_main_menu(key):
    """Handles key presses in the main menu.

    Args:
        key(int): A keycode (VK)

    Returns:
        (dict): A dictionary key name.
    """

    key_char = chr(key.c)

    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c' or key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_level_up_menu(key):
    """Handles key presses in the Level Up menu.

    Args:
        key(int): A keycode (VK)

    Returns:
        (dict): A dictionary key name.
    """

    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            return {'level_up': 'hp'}
        if key_char == 'b':
            return {'level_up': 'str'}
        if key_char == 'c':
            return {'level_up': 'def'}

    return {}


def handle_character_screen(key):
    """Handles key presses in Character screen.

    Args:
        key(int): A keycode (VK)

    Returns:
        (dict): A dictionary key name.
    """

    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}
