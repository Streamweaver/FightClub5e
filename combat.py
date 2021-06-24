from entity import AbilityType
import roll
import numpy as np
# This is a simple set of classes to run a basic combat between entities.

def handle_attack(attacker):
    """
    Attacker attacks thier target and applies damage if they hit.
    :param combatant: Entity attacking.
    :return:
    """
    to_hit = roll(20)
    is_crit = True if to_hit == 20 else False
    attack_roll = to_hit + attacker.str.mod + attacker.prof_bonus
    if attack_roll >= attacker.target.ac:
        damage = attacker.attack.get_damage(is_crit)
        attacker.target.hp.add_damage(damage)

class RoundHandler:

    def __init__(self, combatants):
        self.current = 0
        for combatant in combatants:
            combatant.initiative = sum(dice.roll('1d20')) + combatant.dex.mod
        self.order = sorted(combatants, key=lambda c: (c.initiative, c.dex.value), reverse=True)

    def run_round(self):
        """
        Iterate through combatants and run their turn sequence.

        :return:
        """
        self.current = self.current + 1
        # Get next live combatant
            # Get target
            # Handle attack
            # Apply results
            # end turn
        # End round

    def end_round(self):
        self.current = self.current + 1


class Battle:

    def __init__(self, combatants=[]):
        self.combatants = combatants # To be a list of entities.
        self.started = False
        self.round = None

    def start_fight(self):
        self.started = True
        self.round = RoundHandler(self.combatants)




