class Level:
    """Defines player's leveling experience and functions."""

    # TODO: Move lvl base and lvl factor to constants.
    def __init__(self, current_level=1, current_xp=0, level_up_base=200, level_up_factor=150):
        """Inits values needed for leveling up.

        Player starts at Experience Level 1 with no XP.
        Leveling base is the amount of XP needed to reach
        the next level. Leveling factor increases amount of
        XP needed to gain a level.

        Args:
            current_level(int): Player's current level.
            current_xp(int): Player's current XP total.
            level_up_base(int): Base XP needed to level up.
            level_up_factor(int): Additional XP needed to level up.
        """

        self.current_level = current_level
        self.current_xp = current_xp
        self.level_up_base = level_up_base
        self.level_up_factor = level_up_factor

    @property
    def experience_to_next_level(self):
        """Returns total XP needed to level up based on current level."""

        return self.level_up_base + self.current_level * self.level_up_factor

    def add_xp(self, xp):
        """Adds XP amount to XP total.

        Adds earned XP to XP total. Then checks if
        it's time to level up (adjusting current XP,
        XP to level up, and current level if it is)
        and returns a boolean.

        Args:
            xp(int): Amount of XP to add.

        Returns:
            (bool): Has performing this function resulted in a Level Up?
        """

        self.current_xp += xp

        if self.current_xp > self.experience_to_next_level:
            self.current_xp -= self.experience_to_next_level
            self.current_level += 1

            return True
        else:
            return False
