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

    def handle_attack(self, attacker, verbose=True):
        """
        Attacker attacks their target and applies damage if they hit.
        :param attacker: Entity attacking.
        :return:
        """
        attacker.select_target(self.order) # Error Raised if not target.
        msg = f"{attacker.name} misses {attacker.target.name}."
        to_hit = roll(20)
        is_crit = True if to_hit == 20 else False
        attack_roll = to_hit + attacker.str.mod + attacker.prof_bonus
        if attack_roll >= attacker.target.ac:
            damage = attacker.attack.get_damage(is_crit)
            hit_type = "CRITS" if is_crit else "hits"
            msg = f"{attacker.name} {hit_type} {attacker.target.name} with {attacker.attack.name} and does {damage} damage."
            attacker.target.hp.add_damage(damage)
            if attacker.target.hp.current == 0:
                msg = msg + f" {attacker.target.name} dies."
                attacker.target.hp.is_alive = False
                self.order.remove(attacker.target)
                attacker.target = None
        if verbose:
            print(msg)

    def handle_round(self):
        """
        Iterate through combatants and run their turn sequence.

        :return:
        """
        self.current = self.current + 1 # increment the round count
        for actor in self.order: # Get next live combatant
            self.handle_attack(actor) # Handle attack
            actor.end_turn()  # end turn


class Battle:

    def __init__(self, combatants=[]):
        self.combatants = combatants # To be a list of entities.
        self.started = False
        self.round = None

    def start_fight(self):
        self.started = True
        self.round = RoundHandler(self.combatants)

    def end_fight(self):
        self.round = None
        self.started = False




