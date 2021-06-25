import random
import unittest

from util import roll
from exceptions import TargetException
from entity import Entity, Size, HitPoints, Ability, AbilityType, Attack, DamageType
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

class RoundHandlerTest(unittest.TestCase):

    def setUp(self):
        combatants = [Entity(**COMMONER) for _ in range(15)]
        combatants.extend(Entity(**BUGBEAR) for _ in range(5))
        for c in combatants:
            c.dex.value = roll(6, 3)
        self.round_mass = RoundHandler(combatants)

    def test_round_handler(self):
        prev = self.round_mass.order[0]
        for c in self.round_mass.order[1:]:
            self.assertGreaterEqual(prev.initiative, c.initiative)
            if prev.initiative == c.initiative:
                self.assertGreaterEqual(prev.dex.value, c.dex.value)
            prev = c

    def test_handle_attack(self):
        commoner = Entity(**COMMONER)
        commoner.attack.d = 1
        bugbear = Entity(**BUGBEAR)
        bugbear.ac = 1
        commoner.target = bugbear
        bugbear.target = commoner
        rh = RoundHandler([commoner, bugbear])
        rh.handle_attack(commoner)
        self.assertLess(bugbear.hp.current, BUGBEAR['max_hp'], "Bugbear should take 1 or 2 damage.")
        while commoner.hp.is_alive:
            rh.handle_attack(bugbear)
        self.assertEqual(commoner.hp.current, 0, "Commoner should be at zero hp")
        self.assertFalse(commoner.hp.is_alive, "Commoner should be dead")
        self.assertEqual(len(rh.order), 1, "Commoner should not be in order")
        self.assertIsNone(bugbear.target, "Bugbear should have no target")
        self.assertRaises(TargetException, rh.handle_attack, bugbear)