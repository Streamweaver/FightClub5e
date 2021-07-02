import random
import unittest

from util import roll
from exceptions import TargetException, BattleException
from entity import Entity, mob_factory
from combat import Battle, RoundHandler
from mobs import BUGBEAR, COMMONER


class BattleTest(unittest.TestCase):

    def setUp(self):
        num_init = 9
        entities = [Entity(**BUGBEAR) for _ in range(num_init)]
        entities.extend([Entity(**COMMONER) for _ in range(num_init)])
        self.battle = Battle(entities)

    def test_battle(self):
        self.assertEqual(18, len(self.battle.combatants))

    def test_start_fight_exceptions(self):
        combatants = []
        battle = Battle(combatants, verbose=False)
        self.assertRaises(BattleException, battle.start_fight)
        for i in range(3):
            e = Entity(**COMMONER)
            e.faction = e.faction + f"_{i}"
            combatants.append(e)
        self.assertRaises(BattleException, battle.start_fight)

    def test_start_fight(self):
        c = mob_factory(BUGBEAR, 3)
        c.extend(mob_factory(COMMONER, 9))
        battle = Battle(c, verbose=False)
        result = battle.start_fight()
        self.assertTrue(result['winning_faction'] in [BUGBEAR['faction'], COMMONER['faction']])


class RoundHandlerTest(unittest.TestCase):

    def setUp(self):
        combatants = [Entity(**COMMONER) for _ in range(15)]
        combatants.extend(Entity(**BUGBEAR) for _ in range(5))
        for c in combatants:
            c.dex.value = roll(6, 3)
        self.round_mass = RoundHandler(combatants)

    def test_get_factions(self):
        # Make sure we have 2 to start
        factions = self.round_mass.get_factions()
        self.assertEqual(len(factions), 2)

        # Remove all of one faction
        remove_faction = factions.pop()
        for c in list(self.round_mass.order):
            if c.faction == remove_faction:
                self.round_mass.order.remove(c)
        self.assertEqual(len(self.round_mass.get_factions()), 1)

    def test_round_handler(self):
        prev = self.round_mass.order[0]
        for c in self.round_mass.order[1:]:
            self.assertGreaterEqual(prev.initiative, c.initiative)
            if prev.initiative == c.initiative:
                self.assertGreaterEqual(prev.dex.value, c.dex.value)
            prev = c

    def test_handle_attack(self):
        commoner = Entity(**COMMONER)
        commoner.attacks[0].d = 1
        bugbear = Entity(**BUGBEAR)
        bugbear.ac = 1
        commoner.last_target = bugbear
        bugbear.last_target = commoner
        rh = RoundHandler([commoner, bugbear], verbose=False)
        rh.handle_attack(commoner, bugbear, commoner.attacks[0])
        self.assertLess(bugbear.hp.current, BUGBEAR['max_hp'], "Bugbear should take 1 or 2 damage.")
        while commoner.hp.is_alive:
            rh.handle_attack(bugbear, commoner, bugbear.attacks[0])
        self.assertEqual(commoner.hp.current, 0, "Commoner should be at zero hp")
        self.assertFalse(commoner.hp.is_alive, "Commoner should be dead")
        self.assertEqual(len(rh.order), 1, "Commoner should not be in order")
