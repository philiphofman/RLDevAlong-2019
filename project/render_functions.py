#  Coded by Philip Hofman, Copyright (c) 2020.

import tcod as libtcod
from enum import Enum, auto
from project.game_states import GameStates
from project.menus import character_screen, inventory_menu, level_up_menu


class RenderOrder(Enum):
    """Defines the render order of Entity objects with Enums."""

    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def get_names_under_mouse(mouse, entities, fov_map):
    """Displays names of entities under mouse pointer.

    Args:
        mouse(Mouse): TCOD Mouse object.
        entities(list): List of entities to check names of.
        fov_map(Map): TCOD Map object used for calculating FOV.
    """

    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]

    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    """Renders a bar on the screen.

    Args:
        panel(Console): The Console object the bar will be rendered in.
        x(int): Width of the bar.
        y(int): Height of the bar.
        total_width(int): Total width of the bar on the screen.
        name(str): The name of the bar (e.g. Health).
        value(int): Current value of the bar.
        maximum(int): Max value of the bar.
        bar_color(tcod.color): The libtcod.Color of the bar.
        back_color(tcod.color): The libtcod.Color of the background.
    """

    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > - 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
               bar_width, panel_height, panel_y, mouse, colors, game_state):
    """Draws everything that is currently visible to the player.

    Draws everything the player currently sees as well as explored
    terrain. Also draws a health bar in the lower left corner.

    Args:
        con(Console): A Console object used for the map.
        panel(Console): A Console object used for Stats (i.e. Health).
        entities(list): The list containing everything to be drawn.
        player(Entity): The player Entity object.
        game_map(Map): The Map object used for the actual game.
        fov_map(Map): The Map object used to calculate FOV.
        fov_recompute(bool): A boolean value that indicates if we need to recalculate the FOV.
        message_log(MessageLog): A Message Log object that holds game messages to be displayed.
        screen_width(int): Width of the screen.
        screen_height(int): Height of the screen.
        bar_width(int): Width of bar.
        panel_height(int): Height of panel Console.
        panel_y(int): Position of bar on panel in the y-axis.
        mouse: Mouse Event.
        colors(dict): A dictionary containing all the colors we can use in the game.
        game_state(Enum): A Enum representing the current game state.
    """

    # NOTE: Tiles don't have any color and therefore aren't visible if
    # they're not explored. render_all cycles through every tile in the
    # current game map, and only gives them a color if they're visible
    # and/or explored. But once they're explored, they stay that way,
    # giving us a growing map.

    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = fov_map.fov[y, x]
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)

                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    # Draw all entities in the list
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)

    # Draw stuff on screen.
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'

        inventory_menu(con, inventory_title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, 'Level up! Choose a stat to raise:', player, 40, screen_width, screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.light_red,
               libtcod.darker_red)
    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Dungeon Level: {0}'.format(game_map.dungeon_level))

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_under_mouse(mouse, entities, fov_map))

    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)


def clear_all(con, entities):
    """Erases all items contained within a list in a specific console.

    Args:
        con(Console): A Console object from tcod.
        entities(list): A list containing everything to be cleared.
    """

    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map, game_map):
    """Draws the Entity object ONLY if it's currently visible to the player.

    The one exception to the visibility rule is stairs; once they're found,
    they stay visible to the player even if they're not within the FOV, so
    the player always knows exactly where the exit is on the map.

    Args:
        con(Console): A Console object from TCOD.
        entity(Entity): An Entity object that will be drawn.
        fov_map(Map): A TCOD Map object that's used for FOV calculations.
        game_map(Map): A TCOD Map object used to represent the game map.
    """
    # Check if tile is within FOV or is an explored stairs tile.
    if fov_map.fov[entity.y, entity.x] or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    """Erases the Entity object.

    Args:
        con(Console): A Console object from tcod.
        entity(Entity): An Entity object.
    """

    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
