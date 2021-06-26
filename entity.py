from enum import Enum, auto
from util import roll
from exceptions import TargetException
import numpy as np


class Size(Enum):
    TINY = 1
    SMALL = 2
    MEDIUM = 3
    LARGE = 4
    HUGE = 5
    GARGANTUAN = 6


class DamageType(Enum):
    SLASHING = 1
    PIERCING = 2
    BLUDGEONING = 3
    POISON = 4
    ACID = 5
    FIRE = 6
    COLD = 7
    RADIANT = 8
    NECROTIC = 9
    LIGHTNING = 10
    THUNDER = 11
    FORCE = 12
    PSYCHIC = 13

class AbilityType(Enum):
    STR = 1
    DEX = 2
    CON = 3
    INT = 4
    WIS = 5
    CHA = 6


def mob_factory(e_dict, num):
    """
    Returns a list of entities from the provided dict with unique names
    :param e_dict: dict to use to initiate an entity
    :param num: int of number of entities to produce.
    :return:
    """
    entities = []
    for i in range(num):
        e = Entity(**e_dict)
        _modify_zombie(e)
        e.name = f"{e.name}_{i + 1}"
        entities.append(e)
    return entities

def _modify_zombie(e):
    if e.name == 'Zombie':
        e.hp = UndeadForitude(e.hp.max_hp)

class HitPoints:

    def __init__(self, max_hp=0):
        self.max_hp = max_hp
        self.drain = 0
        self.temp_hp = 0
        self.damage = 0

    @property
    def is_alive(self):
        return self.current > 0

    def add_temp_hp(self, h):
        """
        Adds a particular amount of temporary hp. If the amount is more than the current value
        it replaces it, if less it leaves it as is.
        :param h: int of temp hps to try to set.
        :return:
        """
        if h > self.temp_hp:
            self.temp_hp = h

    def remove_temp_hp(self, d):
        """
        Applies d damage to temporary hp and returns any remainder.
        :param d:
        :return:
        """
        overflow = 0
        if self.temp_hp - d < 0:
            overflow = self.temp_hp - d
            self.temp_hp = 0
        else:
            self.temp_hp = self.temp_hp - d
        return abs(overflow)

    @property
    def current(self):
        """
        Returns the current hp of the character.
        :return:
        """
        return self.temp_hp + self.max_hp - self.damage

    def add_damage(self, d, is_critical=False, damage_type=None):
        """
        Adds specified amount of damage as needed.

        :param d: int of damage to apply
        :return:
        """
        # remove any temp hp
        # floor at zero hp
        d = self.remove_temp_hp(d)

        self.damage = self.damage + d
        if self.damage >= self.max_hp:
            self.damage = self.max_hp

    def heal(self, h):
        """
        Applies healing.

        :param h: int of healing to apply
        :return:
        """
        if self.damage - h < 0:
            self.damage = 0
        else:
            self.damage = self.damage - h

class UndeadForitude(HitPoints):

    def __init__(self, max_hp=0, con_mod=0):
        self.con_mod = con_mod
        super().__init__(max_hp)

    def add_damage(self, d, is_critical=False, damage_type=None):
        """
        Adds damage, if

        :param d: int of damage to apply
        :param is_critical: bool is the damage from a critical
        :param damage_type: Enum of damage type.
        :return:
        """
        # remove any temp hp
        # floor at zero hp
        d = self.remove_temp_hp(d)

        self.damage = self.damage + d
        if self.damage >= self.max_hp:
            self.damage = self.max_hp
            if not is_critical:
                if roll(20) + self.con_mod >= d:
                    self.damage = self.max_hp - 1
                    print("Just wont die!")

class Ability:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    @property
    def mod(self):
        """
        Returns the abilitiy modifier value for the ability value.
        :return: int of modifier
        """
        value = np.floor_divide((self.value - 10), 2)
        return value

    def check(self, bonus=0):
        """
        Rolls a d20 and adds the ability mod and any bonus provided.
        :param bonus: int of bonus to add to check.
        :return: int of check total
        """
        return roll(20, 1) + self.mod + bonus


class Attack:

    def __init__(self, name, num, d, bonus, damage_type, ability=AbilityType.STR):
        """
        Represents an individual attack.
        :param name: str of name of attack
        :param num: int of number of dice to roll
        :param d: int of die type to roll
        :param bonus: int of bonus to damage
        :param damage_type: Enum of damage type
        :param ability: enum of Ability used.
        """
        self.name = name
        self.num = num
        self.d = d
        self.bonus = bonus
        self.damage_type = damage_type

    def get_damage(self, is_crit=False):
        """
        Gets the total damage of the attack.

        :param is_crit: bool of crit status
        :return: int of total damage.
        """
        return roll(self.d, self.num, is_crit) + self.bonus # TODO Refactor this to let crits happen.


class Entity:

    def __init__(self, name='', ac=10, max_hp=0, size=Size.MEDIUM, attack=None, prof_bonus=2, faction=None, abilities={}):
        self.ac = ac
        self.hp = HitPoints(max_hp)
        self.size = size
        self.attack = attack
        self.prof_bonus = prof_bonus
        self._init_abilities(abilities)
        self.initiative = 0
        self.last_target = None
        self.name = name
        self.faction = faction if faction else self.name.lower()

    def _init_abilities(self, abilities):
        """
        This adds abilities to the entity as properties with the appropriate ability type
        string.  i.e. bugbear.str would return the Ability class assigned to str.
        :return:
        """
        for a in AbilityType:
            name = a.name.lower()
            value = 10 if name not in abilities else abilities[name]
            self.__setattr__(name, Ability(name, 10))

    def end_combat(self):
        """
        Any combat cleanup.
        :return: None
        """
        self.initiative = 0
        self.target = None

    def select_target(self, combatants, force_new=False):
        """
        Chooses a random target from an opposing faction.
        :param combatants: list of Entities to choose from.
        :param force_new: bool to force choosing a new target.
        :return:
        """
        if self.target is None or not self.target.hp.is_alive or force_new:
            enemies = [c for c in combatants if c.faction != self.faction]
            if not enemies or len(enemies) == 0:
                raise TargetException("No targets left alive")
            self.target = np.random.choice(enemies)

    def end_turn(self):
        """
        Hold method in case I need an end of turn handler.
        :return:
        """
        pass

    def title(self):
        return f"{self.name.title()} ({self.hp.current}/{self.hp.max_hp})"