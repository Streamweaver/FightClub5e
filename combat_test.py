import random
import unittest
import dice

from entity import Entity, Size, HitPoints, Ability, AbilityType, Attack, DamageType
from combat import Battle, RoundHandler

BUGBEAR = {
    'name': 'Bugbear',
    'ac': 16,
    'max_hp': 27,
    'size': Size.MEDIUM,
    'attack': Attack('Morningstar', '2d8+2', DamageType.PIERCING)
}
COMMONER = {
    'name': 'Commoner',
    'ac': 10,
    'max_hp': 4,
    'size': random.choice([Size.MEDIUM, Size.SMALL]),
    'attack': Attack('Club', '1d4', DamageType.BLUDGEONING)
}

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
        combatants = [Entity(**COMMONER) for _ in range(50)]
        for c in combatants:
            c.dex.value = sum(dice.roll('3d6'))
        self.round = RoundHandler(combatants)

    def test_round_handler(self):
        prev = self.round.order[0]
        for c in self.round.order[1:]:
            self.assertGreaterEqual(prev.initiative, c.initiative)
            if prev.initiative == c.initiative:
                self.assertGreaterEqual(prev.dex.value, c.dex.value)
            prev = c

