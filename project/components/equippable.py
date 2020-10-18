#  Coded by Philip Hofman, Copyright (c) 2020.

class Equippable:
    """Component class defining stuff for equippable items.

    Tracks what slot this equipment goes into, and any bonuses
    it has.

    Attributes:
        slot(int): What equipment slot this item goes into.
        power_bonus(int): Power boost to player.
        defense_bonus(int): Defense boost to player.
        max_hp_bonus(int): HP bonus to player.
    """

    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        """Inits some default values for equippable items.

        Args:
            slot(int): What equipment slot this item goes into.
            power_bonus(int): Power boost to player.
            defense_bonus(int): Defense boost to player.
            max_hp_bonus(int): HP bonus to player.
        """

        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
