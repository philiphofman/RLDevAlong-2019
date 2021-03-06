"""
A tile on a map. It may or may not be blocked, and may or may not block sight.
"""


#  Coded by Philip Hofman, Copyright (c) 2020.

class Tile:
    """This is the Tile class. It tells you if it's blocked, blocks sight, or explored."""

    def __init__(self, blocked, block_sight=None):
        """Inits default values for this Tile.

        Sets 'blocked' to its passed value. If 'block_sight' isn't set to a value,
        it's automatically set to the same value as 'blocked'. Explored is always
        set to false.

        Args:
            blocked(bool): Indicates if this tile blocks movement.
            block_sight(bool): Indicates if this tile blocks sight.
        """

        self.blocked = blocked

        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        self.explored = False
