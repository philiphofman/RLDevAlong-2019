#  Coded by Philip Hofman, Copyright (c) 2020.

from random import randint


def from_dungeon_level(table, dungeon_level):
    """Returns int from table based on dungeon level."""

    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value

    return 0


def random_choice_index(chances):
    """Returns a random index of an iterable.

    Args:
        chances: The iterable to randomly choose from.

    Returns:
        Index of random position in iterable.
    """

    # Choose a random number within the weight sum of all choices.
    random_chance = randint(1, sum(chances))

    running_sum = 0
    choice = 0
    for w in chances:
        # Add item weight to total.
        running_sum += w

        # If our random chance becomes less than the running sum
        # of item weights, return current choice index.
        if random_chance <= running_sum:
            return choice
        choice += 1


def random_choice_from_dict(choice_dict):
    """Return random key from dictionary.

    Args:
        choice_dict(dict): Dictionary to choose from.

    Returns:
        Randomly chosen dictionary key.
    """

    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    return choices[random_choice_index(chances)]
