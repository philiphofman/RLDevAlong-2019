#  Coded by Philip Hofman, Copyright (c) 2020.

class Stairs:
    """Marks something to act as stairs."""

    def __init__(self, floor):
        """Inits values for stairs class.

        Args:
            floor(int): Indicates which floor these stairs go to.
        """
        self.floor = floor
