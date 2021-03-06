#  Coded by Philip Hofman, Copyright (c) 2020.

import tcod as libtcod
from project.loader_functions.initialize_new_game import get_constants, get_game_variables
from project.loader_functions.data_loaders import load_game, save_game
from project.game_messages import Message
from project.death_functions import kill_monster, kill_player
from project.entity import get_blocking_entities_at_location
from project.input_handlers import handle_keys, handle_mouse, handle_main_menu
from project.render_functions import clear_all, render_all
from project.fov_functions import initialize_fov, recompute_fov
from project.game_states import GameStates
from project.menus import main_menu, message_box


def play_game(player, entities, game_map, message_log, game_state, con, panel, constants):
    """Main game loop.

    Args:
        player(Entity): Player Entity object.
        entities(list): List of entities on map.
        game_map(Map): TCOD map object used as game map.
        message_log(MessageLog): MessageLog object list of messages.
        game_state(Enum): Enum GameState (e.g. PLAYERS_TURN)
        con(Console): Console used to display whole game.
        panel(Console): Console used to display messages and UI info.
        constants(dict): Dictionary of constant game variables.
    """

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    previous_game_state = game_state

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    targeting_item = None

    while not libtcod.console_is_window_closed():

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'],
                          constants['fov_algorithm'])

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants['screen_width'], constants['screen_height'], constants['bar_width'],
                   constants['panel_height'], constants['panel_y'], mouse, constants['colors'], game_state)

        fov_recompute = False

        # Refresh scene (?)
        libtcod.console_flush()

        clear_all(con, entities)

        # Get any keys that have been pressed and execute their associated action(s).
        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        move = action.get('move')
        wait = action.get('wait')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        take_stairs = action.get('take_stairs')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        elif wait:
            game_state = GameStates.ENEMY_TURN
            if player.fighter.hp < player.fighter.max_hp:
                player.fighter.hp += 1

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        if take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    entities = game_map.next_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    con.clear()

                    break
            else:
                message_log.add_message(Message('There are no stairs here.', libtcod.yellow))

        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            elif level_up == 'str':
                player.fighter.base_power += 1
            elif level_up == 'def':
                player.fighter.base_defense += 1

            game_state = previous_game_state

        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(player, entities, game_map, message_log, game_state)

                return True

        if fullscreen:
            # Toggle fullscreen by making the set_fullscreen variable equal to the opposite of itself.
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # Check what happened on the player's turn and react accordingly.
        for player_turn_results in player_turn_results:
            message = player_turn_results.get('message')
            dead_entity = player_turn_results.get('dead')
            item_added = player_turn_results.get('item_added')
            item_consumed = player_turn_results.get('consumed')
            item_dropped = player_turn_results.get('item_dropped')
            equip = player_turn_results.get('equip')
            targeting = player_turn_results.get('targeting')
            targeting_cancelled = player_turn_results.get('targeting_cancelled')
            xp = player_turn_results.get('xp')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

                game_state: GameStates.ENEMY_TURN

            if item_consumed:
                game_state: GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('Targeting cancelled.'))

            if xp:
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(Message('You gain {0} XP.'.format(xp)))

                if leveled_up:
                    message_log.add_message(Message('Your fighting skills improve! You reached level {0}'.format(
                        player.level.current_level) + '!', libtcod.yellow))
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP

            if item_dropped:
                entities.append(item_dropped)

                game_state: GameStates.ENEMY_TURN

            if equip:
                equip_results = player.equipment.toggle_equip(equip)

                for equip_results in equip_results:
                    equipped = equip_results.get('equipped')
                    dequipped = equip_results.get('unequipped')

                    if equipped:
                        message_log.add_message(Message('You equip the {0}'.format(equipped.name)))

                    if dequipped:
                        message_log.add_message(Message('You unequip the {0}'.format(dequipped.name)))

                game_state = GameStates.ENEMY_TURN

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:

                # Checking for AI skips the player and any items/other stuff we implement later.
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_results in enemy_turn_results:
                        message = enemy_turn_results.get('message')
                        dead_entity = enemy_turn_results.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN


def main():
    """The main function of the engine. It sets up everything needed for the game and contains the main game loop function."""

    constants = get_constants()

    # Sets custom ASCII character PNG image to use.
    libtcod.console_set_custom_font('dejavu10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # Creates the window, window size, window title, and sets fullscreen.
    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)

    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False

    main_menu_background_image = libtcod.image_load('menu_background.png')

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if show_main_menu:
            main_menu(con, main_menu_background_image, constants['screen_width'], constants['screen_height'])

            if show_load_error_message:
                message_box(con, 'No save game to load!', 50, constants['screen_width'], constants['screen_height'])

            libtcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN

                show_main_menu = False
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break

        else:
            con.clear()
            play_game(player, entities, game_map, message_log, game_state, con, panel, constants)

            show_main_menu = True


# If this script is being run directly rather than imported, run main.
# It's a safety check to ensure the game doesn't start when, for example,
# Sphinx imports it to look for docstrings.
if __name__ == '__main__':
    main()
