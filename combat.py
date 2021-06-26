import numpy as np
from collections import defaultdict

from util import roll
from exceptions import BattleException, TargetException

class RoundHandler:

    def __init__(self, combatants, verbose=True):
        self.current = 0
        self.stats = None
        self.verbose = verbose
        self.combatants = combatants
        for combatant in combatants:
            combatant.initiative = roll(20) + combatant.dex.mod
        self.order = sorted(combatants, key=lambda c: (c.initiative, c.dex.value), reverse=True)

    def get_factions(self):
        """
        Returns a set of the combatant factions.
        :return:
        """
        # TODO move this into a round handler to track who is active (since that is the order)
        return {e.faction for e in self.order}

    def handle_attack(self, attacker, targets):
        """
        Attacker attacks their target and applies damage if they hit.
        :param attacker: Entity attacking.
        :param targets: list of possible targets
        :return:
        """
        target = self.get_target(attacker)
        attacker.last_target = target
        msg = f"{attacker.title()} misses {target.title()}."
        to_hit = roll(20)
        is_crit = True if to_hit == 20 else False
        attack_roll = to_hit + attacker.str.mod + attacker.prof_bonus
        if attack_roll >= target.ac:
            damage = attacker.attack.get_damage(is_crit)
            hit_type = "CRITS" if is_crit else "hits"
            msg = f"{attacker.title()} {hit_type} {target.title()} with {attacker.attack.name} and does {damage} damage."
            target.hp.add_damage(damage)
            if not target.hp.is_alive:
                msg = msg + f" {target.name} dies."
                self.order.remove(target)
                attacker.last_target = None
        if self.verbose:
            print(msg)

    def get_possible_targets(self, attacker):
        possible_targets = [e for e in self.combatants if e.hp.is_alive and e.faction != attacker.faction]
        if not possible_targets:
            raise TargetException('No valid targets.')
        return possible_targets

    def get_target(self, attacker):
        """
        Returns a target
        :param attacker:
        :return:
        """
        if attacker.last_target and attacker.last_target.hp.is_alive:
            return attacker.last_target
        return np.random.choice(self.get_possible_targets(attacker))

    def combatant_count(self):
        d = defaultdict(int)
        for e in self.order:
            d[e.faction] += 1
        return d

    def handle_round(self):
        """
        Iterate through combatants and run their turn sequence.

        :return:
        """
        self.current = self.current + 1 # increment the round count
        if self.verbose:
            count = ", ".join(f"{k}: {n}".title() for k, n in self.combatant_count().items())
            print(f"**** Round {self.current} - {count} ****")

        for actor in self.order: # Get next live combatant
            if not actor.hp.is_alive:
                continue
            try:
                self.handle_attack(actor, self.get_target(actor)) # Handle attack
                actor.end_turn()
            except TargetException:
                break # No targets left, break out.

        self.end_round()

    def end_round(self):
        pass

class Battle:

    def __init__(self, combatants=[], verbose=True):
        self.combatants = combatants # To be a list of entities.
        self.started = False
        self.round = None
        self.verbose = verbose

    def start_fight(self):
        self.started = True
        self.round = RoundHandler(self.combatants, verbose=self.verbose)
        factions = self.round.get_factions()
        if len(factions) > 2:
            raise BattleException("There are more than 2 factions.")
        if len(factions) < 2:
            raise BattleException("Not enough factions to run fight.")
        if self.verbose:
            f = list(self.round.get_factions())
            print(f"Fight starting between {f[0]} and {f[1]}")
        self.handle_rounds()
        self.end_fight()

    def handle_rounds(self):
        while len(self.round.get_factions()) == 2:
            self.round.handle_round()

    def end_fight(self):
        if self.verbose:
            print(f"Winner: {self.round.get_factions().pop()}, with {len(self.round.order)} alive")
        self.round = None
        self.started = False








