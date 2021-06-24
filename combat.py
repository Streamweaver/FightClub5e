from entity import AbilityType
from util import roll
import numpy as np
# This is a simple set of classes to run a basic combat between entities.



class RoundHandler:

    def __init__(self, combatants):
        self.current = 0
        for combatant in combatants:
            combatant.initiative = roll(20) + combatant.dex.mod
        self.order = sorted(combatants, key=lambda c: (c.initiative, c.dex.value), reverse=True)

    def handle_attack(self, attacker):
        """
        Attacker attacks their target and applies damage if they hit.
        :param attacker: Entity attacking.
        :return:
        """
        to_hit = roll(20)
        is_crit = True if to_hit == 20 else False
        attack_roll = to_hit + attacker.str.mod + attacker.prof_bonus
        if attack_roll >= attacker.target.ac:
            damage = attacker.attack.get_damage(is_crit)
            attacker.target.hp.add_damage(damage)
            if attacker.target.hp.current == 0:
                attacker.target.hp.is_alive = False
                self.order.remove(attacker.target)
                attacker.target = None

    def handle_round(self):
        """
        Iterate through combatants and run their turn sequence.

        :return:
        """
        self.current = self.current + 1 # increment the round count
        for c in self.order: # Get next live combatant
            c.select_target(self.order) # Get a target.
            # TODO raise error here if no targets left.
            self.handle_attack(c) # Handle attack
            c.end_turn()  # end turn


class Battle:

    def __init__(self, combatants=[]):
        self.combatants = combatants # To be a list of entities.
        self.started = False
        self.round = None

    def start_fight(self):
        self.started = True
        self.round = RoundHandler(self.combatants)




