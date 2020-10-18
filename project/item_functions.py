#  Coded by Philip Hofman, Copyright (c) 2020.

import tcod as libtcod
from project.game_messages import Message
from project.components.ai import ConfusedMonster


def heal(*args, **kwargs):
    """Heals entity by x amount.

    Args:
        *args: Entity object that's using the item.
        **kwargs: Int amount extracted from kwargs.

    Returns:
        results(list): List with result dictionary.
    """

    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health.', libtcod.yellow)})

    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', libtcod.green)})

    return results


def cast_lightning(*args, **kwargs):
    """Casts lightning at the closest enemy.

    Args:
        *args: Entity object that is casting the spell.
        *kwargs: Gets list of entities, Map for fov calculations,
            int damage amount, and max range of spell.

    Returns:
        results(list): List with result dictionary.
    """

    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target, 'message': Message(
            'A lightning bolt strikes the {0} with a loud CRACK! The damage is {1}.'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append(
            {'consumed': False, 'target': None, 'message': Message('No enemy is close enough to strike.', libtcod.red)})

    return results


def cast_fireball(*args, **kwargs):
    """Casts a fireball at a chosen target.

    Args:
        *args:
        **kwargs: Gets list of entities, FOV map,
            int damage, int radius, int x coordinate,
            and int y coordinate.

    Returns:
        results(list): List with result dictionary.
    """

    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False,
                        'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    results.append({'consumed': True,
                    'message': Message('The fireball explodes, burning everything within {0} tiles!'.format(radius),
                                       libtcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append(
                {'message': Message('The {0} takes {1} burn damage!'.format(entity.name, damage), libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results


def cast_confuse(*args, **kwargs):
    """Casts the Confuse spell at a chosen target.

    Args:
        *args:
        **kwargs: Gets Entity list, FOV map, x coordinate,
            and y coordinate.

    Returns:
        results(list): List with result dictionary.
    """

    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False,
                        'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message(
                'The eyes of the {0} look vacant and it starts to stumble around!'.format(entity.name),
                libtcod.light_green)})

            break
    else:
        results.append(
            {'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

    return results
