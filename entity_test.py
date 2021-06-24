import random
import unittest

from entity import Entity, Size, HitPoints, Ability, AbilityType, Attack, DamageType

BUGBEAR = {
    'ac': 16,
    'max_hp': 27,
    'size': Size.MEDIUM,
    'attack': Attack('Morningstar', 2, 8, 2, DamageType.PIERCING),
    'name': 'Bugbear'
}

COMMONER = {
    'ac': 10,
    'max_hp': 10,
    'size': Size.MEDIUM,
    'attack': Attack('Club', 1, 6, 0, DamageType.BLUDGEONING),
    'name': 'Commoner'
}


def get_commoner():
    return {
        'ac': 10,
        'max_hp': 4,
        'size': random.choice([Size.MEDIUM, Size.SMALL]),
        'attacks': []
    }


class HitPointstest(unittest.TestCase):

    def setUp(self):
        self.hp = HitPoints(BUGBEAR['max_hp'])

    def test_current_hp(self):
        self.assertEqual(BUGBEAR['max_hp'], self.hp.max_hp)

    def test_add_temp_hp(self):
        # It should start at zero
        self.assertEqual(0, self.hp.temp_hp)
        b, m, l = 3, 6, 2
        # It should set properly.
        self.hp.add_temp_hp(b)
        self.assertEqual(b, self.hp.temp_hp)
        # It should override with a higher value.
        self.hp.add_temp_hp(m)
        self.assertEqual(m, self.hp.temp_hp)
        # It should retain the value if lower value passed
        self.hp.add_temp_hp(l)
        self.assertEqual(m, self.hp.temp_hp)

    def test_remove_temp_hp(self):
        b, d, o = 6, 3, 6 # Base amount, damage, overflow
        self.hp.add_temp_hp(b)
        # It should remove a proper amount
        remain = self.hp.remove_temp_hp(d)
        self.assertEqual(b - d, self.hp.temp_hp)
        self.assertEqual(0, remain)
        # It should not go negative
        remain = self.hp.remove_temp_hp(o)
        self.assertEqual(0, self.hp.temp_hp, 'It should not go negative')
        self.assertEqual(3, remain, 'It should pass overflow damage back')

    def test_current(self):
        self.assertEqual(BUGBEAR['max_hp'], self.hp.current)

    def test_add_damage(self):
        # Normal HP
        hp = BUGBEAR['max_hp']
        d = 3
        crit_damage = hp * 2
        self.hp.add_damage(d)
        self.assertEqual(d, self.hp.damage, 'It should record the damage')
        self.assertEqual(hp - d, self.hp.current, 'It should return the right current hp')

        # With Temp HP
        self.hp.add_temp_hp(d)
        self.assertEqual(hp, self.hp.current, 'It should include temp hp')
        self.hp.add_damage(1)
        self.assertEqual(d - 1, self.hp.temp_hp, 'It should remove from temp hp')
        self.assertEqual(d, self.hp.damage, 'it should leave damage uneffected')
        self.assertEqual(hp - 1, self.hp.current, 'It display total damage properly')
        self.hp.add_damage(d)
        self.assertEqual(0, self.hp.temp_hp, 'It should set temp hp to zero')
        self.assertEqual(d + 1, self.hp.damage, 'It should apply overflow to damage')
        self.assertEqual(hp - d - 1, self.hp.current, 'It should total all damage correctly')

        # Send to zero.
        self.hp.add_damage(hp)
        self.assertEqual(0, self.hp.current, 'It should floor at zero hp')
        self.assertEqual(hp, self.hp.damage, 'Damage should be qual to max hp')

        self.assertTrue(self.hp.alive)

        # Massive Damage should kill them instantly.
        self.hp.add_damage(hp)
        self.assertFalse(self.hp.alive, 'Massive damage should kill the creature.')

    def test_heal(self):
        hp = BUGBEAR['max_hp']
        heal = 5
        self.hp.heal(hp)
        self.assertEqual(0, self.hp.damage, 'It should not effect damage if already zero')

        self.hp.add_damage(hp)
        self.hp.heal(heal)
        self.assertEqual(hp - heal, self.hp.damage, 'It should reduce damage')
        self.hp.heal(hp)
        self.assertEqual(0, self.hp.damage, 'It should not go negative')


class AbilityTest(unittest.TestCase):

    def setUp(self):
        self.abilities = {i: Ability('temp', i) for i in range(1, 19)}

    def test_mod(self):
        sample_values = {
            1: -5,
            2: -4, 3: -4,
            4: -3, 5: -3,
            6: -2, 7: -2,
            8: -1, 9: -1,
            10: 0, 11: 0,
            12: 1, 13: 1,
            14: 2, 15: 2,
            16: 3, 17: 3,
            18: 4
        }
        for k, a in self.abilities.items():
            self.assertEqual(sample_values[k], a.mod)

    def test_check(self):
        a = Ability('str', 20)
        for i in range(100):
            result = a.check(i)
            self.assertGreaterEqual(result, a.mod + i + 1)
            self.assertLessEqual(result, a.mod + i + 20)

class AttackTest(unittest.TestCase):

    def setUp(self):
        self.attack = Attack('club', 3, 6, 2, DamageType.BLUDGEONING, AbilityType.STR)

    def test_get_damage(self):
        for _ in range(100): # Tested in it's on module, I'm just confirming it works.
            damage = self.attack.get_damage()
            self.assertLessEqual(damage, 20, 'Damage is below 5 which is expected min.')
            self.assertGreaterEqual(damage, 5, 'Damage is above 20')
        for _ in range(100):
            damage = self.attack.get_damage(True)
            self.assertLessEqual(damage, 38)
            self.assertGreater(damage, 8)


class EntityTest(unittest.TestCase):

    def setUp(self):
        self.bugbear = Entity(**BUGBEAR)
        self.commoner = Entity(**COMMONER)
        self.commoner2 = Entity(**COMMONER)

    def test_entity(self):
        self.assertIsNotNone(self.bugbear, 'The Bugbear does not exist!')
        for a in AbilityType:
            self.assertEqual(10, getattr(self.bugbear, a.name.lower()).value, "Abilities not initialized to 10")

    def test_end_combat(self):
        self.bugbear.initiative = self.bugbear.dex.check()
        self.assertGreater(self.bugbear.initiative, 0)
        self.bugbear.target = self.commoner
        self.assertIsNotNone(self.bugbear.target)
        self.bugbear.end_combat()
        self.assertEqual(self.bugbear.initiative, 0)
        self.assertIsNone(self.bugbear.target)

    def test_select_target(self):
        combatants = [self.commoner, self.commoner2, self.bugbear]
        for c in combatants:
            self.assertIsNone(c.target)
            c.select_taget(combatants)
            self.assertIsNotNone(c.target)
            self.assertNotEqual(c.target.faction, c.faction)