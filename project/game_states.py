"""
An 'Enum' is a set of named values that won't change, so it's perfect for things like game states.
The numbers don't really mean anything so the auto() helper just numbers them automatically.

In computer programming, an enumerated type (also called enumeration or enum) is a data type consisting of a set of named values called elements,
members, enumeral, or enumerators of the type. The enumerator names are usually identifiers that behave as constants in the language.
An enumerated type can be seen as a degenerate tagged union of unit type. A variable that has been declared as having an enumerated type can be
assigned any of the enumerators as a value. In other words, an enumerated type has values that are different from each other, and that can be compared
and assigned, but are not specified by the programmer as having any particular concrete representation in the computer's memory; compilers and interpreters
can represent them arbitrarily. 
"""

#  Coded by Philip Hofman, Copyright (c) 2020.

from enum import Enum, auto


class GameStates(Enum):
    """Defines all the different Game States in the game with Enums."""

    PLAYERS_TURN = auto()
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()
    SHOW_INVENTORY = auto()
    DROP_INVENTORY = auto()
    TARGETING = auto()
    LEVEL_UP = auto()
    CHARACTER_SCREEN = auto()
